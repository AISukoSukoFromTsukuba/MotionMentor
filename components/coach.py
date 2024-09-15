import streamlit as st
from streamlit_webrtc import webrtc_streamer
import os
import sys
import cv2
import av
import numpy as np
from ultralytics import YOLO
import threading
import time


tmp_count = 0
form_check_start = 0
form_check_cancel = 0
flag_check_start = 0
flag = 0
mindegreeRight = 0
mindegreeLeft = 0
test = ""


if "squatcount" not in st.session_state:
    st.session_state.count = 0
    st.session_state.inner_thigh = ""
    st.session_state.leg_degree = ""

lock = threading.Lock()

class Keypoints:
  def __init__(self, keypoints_list):
    self.keypoints_list = keypoints_list
    self.keypoint_mapping = {
        "nose": 0,
        "eyeLeft": 1,
        "eyeRight": 2,
        "earLeft": 3,
        "earRight": 4,
        "shoulderLeft": 5,
        "shoulderRight": 6,
        "elbowLeft": 7,
        "elbowRight": 8,
        "wristLeft": 9,
        "wristRight": 10,
        "hipLeft": 11,
        "hipRight": 12,
        "kneeLeft": 13,
        "kneeRight": 14,
        "ankleLeft": 15,
        "ankleRight": 16,
    }

  def __getitem__(self, part):
    if part in self.keypoint_mapping:
      index = self.keypoint_mapping[part]
      return {"x": self.keypoints_list[index][0], "y": self.keypoints_list[index][1]}
    else:
      raise KeyError(f"Keypoint '{part}' not found.")

def arccos2(a,b,c):
    if a*b == 0:
        return np.pi/2
    else:
        return np.arccos( c/ (a*b))

def detect(keypoints, image_buffer):
    global form_check_start
    global form_check_cancel
    global flag_check_start
    global tmp_count
    global mindegreeLeft, mindegreeRight, test


        # 左右の肩と踵のx軸方向の距離が閾値を下回った時にform_check_startをインクリメント
    if abs(keypoints["shoulderLeft"]["x"] - keypoints["ankleLeft"]["x"]) < 50 and abs(keypoints["shoulderRight"]["x"] - keypoints["ankleRight"]["x"]) < 50:
        form_check_start += 1
    else:
        form_check_start = 0 
    # 正しい姿勢（肩と踵の距離が閾値以内）になってから0~1秒、1~2秒、2~3秒の際にカウントダウンの数字を表示し、3~3.5秒でSTARTの文字を表示
    """     if form_check_start > 15 and form_check_start <= 30 and squatcount == 0:
        cv2.putText(image_buffer, "3", (960, 640), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 255, 255), 50, cv2.LINE_AA)
        cv2.putText(image_buffer, "3", (960, 640), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 50, 0), 40, cv2.LINE_AA)
    elif form_check_start > 30 and form_check_start <= 45 and squatcount == 0:
        cv2.putText(image_buffer, "2", (960, 640), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 255, 255), 50, cv2.LINE_AA)
        cv2.putText(image_buffer, "2", (960, 640), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 50, 0), 40, cv2.LINE_AA)
    elif form_check_start > 45 and form_check_start <= 60 and squatcount == 0:
        cv2.putText(image_buffer, "1", (960, 640), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 255, 255), 50, cv2.LINE_AA)
        cv2.putText(image_buffer, "1", (960, 640), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 50, 0), 40, cv2.LINE_AA) 
    elif form_check_start > 60 and form_check_start <= 67.5 and squatcount == 0:
        cv2.putText(image_buffer, "START!", (560, 590), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 255, 255), 50, cv2.LINE_AA)
        cv2.putText(image_buffer, "START!", (560, 590), cv2.FONT_HERSHEY_DUPLEX, 10, (255, 50, 0), 40, cv2.LINE_AA)   """ 

    flag_check_start = 1 # STARTしたらスクワットのカウントを開始するためのflagを立てる

    ### 左膝の角度の計算
    # 膝の角度は腰・膝・足首の座標から計算するため、各ポイントの座標を変数に格納
    hipLeft = np.array([keypoints["hipLeft"]["x"], keypoints["hipLeft"]["y"]])
    kneeLeft = np.array([keypoints["kneeLeft"]["x"], keypoints["kneeLeft"]["y"]])
    ankleLeft = np.array([keypoints["ankleLeft"]["x"], keypoints["ankleLeft"]["y"]])

    # 膝を中心として、腰・足首からのベクトルを計算                    
    vec_hip_leftknee = hipLeft - kneeLeft
    vec_ankle_leftknee = ankleLeft - kneeLeft

    # ベクトルから角度を計算                    
    length_vec_hip_leftknee = np.linalg.norm(vec_hip_leftknee)
    length_vec_ankle_leftknee = np.linalg.norm(vec_ankle_leftknee)

    hip_knee_ankle_ratio_left = length_vec_hip_leftknee/length_vec_ankle_leftknee

    inner_product = np.inner(vec_hip_leftknee, vec_ankle_leftknee)

    rad = arccos2(length_vec_hip_leftknee,length_vec_ankle_leftknee,inner_product)

    #cos = inner_product / (length_vec_hip_leftknee * length_vec_ankle_leftknee)
    #rad = np.arccos(cos)
    degreeLeft = np.rad2deg(rad)

    ### 右膝の角度の計算
    # 膝の角度は腰・膝・足首の座標から計算するため、各ポイントの座標を変数に格納
    hipRight = np.array([keypoints["hipRight"]["x"], keypoints["hipRight"]["y"]])
    kneeRight = np.array([keypoints["kneeRight"]["x"], keypoints["kneeRight"]["y"]])
    ankleRight = np.array([keypoints["ankleRight"]["x"], keypoints["ankleRight"]["y"]])

    # 膝を中心として、腰・足首からのベクトルを計算 
    vec_hip_rightknee = hipRight - kneeRight
    vec_ankle_rightknee = ankleRight - kneeRight

    # ベクトルから角度を計算                      
    length_vec_hip_rightknee = np.linalg.norm(vec_hip_rightknee)
    length_vec_ankle_rightknee = np.linalg.norm(vec_ankle_rightknee)
    inner_product = np.inner(vec_hip_rightknee, vec_ankle_rightknee)

    hip_knee_ankle_ratio_right = length_vec_hip_rightknee/length_vec_ankle_rightknee

    rad = arccos2(length_vec_hip_rightknee,length_vec_ankle_rightknee,inner_product)
    print(hip_knee_ankle_ratio_left,hip_knee_ankle_ratio_right)
    degreeRight = np.rad2deg(rad)     

    if abs(keypoints["nose"]["x"] - keypoints["wristLeft"]["x"]) < 100 and abs(keypoints["nose"]["x"] - keypoints["wristRight"]["x"]) < 100 and abs(keypoints["nose"]["y"] - keypoints["wristLeft"]["y"]) < 100 and abs(keypoints["nose"]["y"] - keypoints["wristRight"]["y"]) < 100:
        form_check_cancel += 1
    else:
        form_check_cancel = 0

    ### 左膝の角度のヒートマップ計算       
    # 角度の扇型を描くための計算         

    ### スクワット回数カウント
    # 膝が伸びている（角度が130~170度）→膝が曲がっている（角度が110度以下）、の状態を1周した時にカウントするように設計
    global flag

    # 鼻と左手首・右手首が一定の距離にある場合にform_check_cancelをインクリメント

    mindegreeRight = min(degreeRight, mindegreeRight)
    mindegreeLeft = min(degreeLeft, mindegreeLeft)
    if hip_knee_ankle_ratio_left < 0.8 and hip_knee_ankle_ratio_right < 0.8 and flag == 1:
        flag = 0
        with lock:
            tmp_count += 1
            if mindegreeRight < 90 and mindegreeLeft < 90:
                test = "膝曲がってるね～いいね～"
            elif mindegreeRight < 100 and mindegreeLeft < 100:
                test = "膝が伸びてきてるよ"
            else:
                test = "膝が伸びすぎだって、きびしいって"
    elif hip_knee_ankle_ratio_left > 1.0 and hip_knee_ankle_ratio_right > 1.0:
        flag = 1
        mindegreeRight = 180
        mindegreeLeft = 180
        
     # 鼻と左手首・右手首が一定の距離にある状態が1秒以内
    if form_check_cancel > 0 and form_check_cancel <= 60:
        pass
        """ cv2.putText(image_buffer, "Count Canceling...", (400, 590), 
        cv2.FONT_HERSHEY_DUPLEX, 5, (255, 255, 255), 30, cv2.LINE_AA)
        cv2.putText(image_buffer, "Count Canceling...", (400, 590), 
        cv2.FONT_HERSHEY_DUPLEX, 5, (0, 50, 255), 20, cv2.LINE_AA)  """
    # 鼻と左手首・右手首が一定の距離にある状態が1秒以上になったらリセット実行
    elif form_check_cancel > 60 and form_check_cancel <= 90:
        """         cv2.putText(image_buffer, "Count Cancel!", (560, 590), 
        cv2.FONT_HERSHEY_DUPLEX, 5, (255, 255, 255), 30, cv2.LINE_AA)
        cv2.putText(image_buffer, "Count Cancel!", (560, 590), 
        cv2.FONT_HERSHEY_DUPLEX, 5, (0, 50, 255), 20, cv2.LINE_AA)   """ 
        flag_check_start = 0 # 開始時のカウントダウン（肩と踵の位置チェック）に使うフラグ
        with lock:
            tmp_count = 0
        flag = 0 # カウント時に使うフラグを0にする 
    
    """print(round(degreeLeft),round(degreeLeft))
    if round(degreeRight) < 170 and round(degreeRight) > 130 and round(degreeLeft) < 170 and round(degreeLeft) > 130 and flag == 1:
        flag = 0
        squatcount += 1
    elif round(degreeRight) < 110 and round(degreeLeft) < 110 and flag == 0 and flag_check_start == 1:
        flag = 1 # 膝の角度が110度以下になるとカウント（撮影角度によって実際の角度と異なるため90より大きめ） """
    
    # 姿勢分析
    x_left, y_left = vec_hip_leftknee
    x_right, y_right = vec_hip_rightknee
    if abs(x_left) > 30 and abs(x_right) > 30:
        st.session_state.inner_thigh = "スクワット完璧だって"
    elif abs(x_left) > 15 and abs(x_right) > 15:
        st.session_state.inner_thigh = "もっと足広げて"
    else:
        st.session_state.inner_thigh = "内股すぎるって厳しいって"


sys.path.append(os.pardir)

model = YOLO("yolov8n-pose.pt")

KEYPOINTS_NAMES = [
    "nose",  # 0
    "eye(L)",  # 1
    "eye(R)",  # 2
    "ear(L)",  # 3
    "ear(R)",  # 4
    "shoulder(L)",  # 5
    "shoulder(R)",  # 6
    "elbow(L)",  # 7
    "elbow(R)",  # 8
    "wrist(L)",  # 9
    "wrist(R)",  # 10
    "hip(L)",  # 11
    "hip(R)",  # 12
    "knee(L)",  # 13
    "knee(R)",  # 14
    "ankle(L)",  # 15
    "ankle(R)",  # 16
]

def coach_page():
    global tmp_count, test
    # 2列に分割
    col1, col2 = st.columns(2)
    reps = 0

    # 左側にはカメラから入力された映像を表示
    with col1:
        video_path = "スクワット.mp4"
        #st.video(video_path, start_time=0, format="video/mp4")
        webrtc_streamer(key="example", video_frame_callback=callback)
        with st.empty():
            while True:
                st.write(f"{tmp_count}")
                st.write(f"{test}")
                time.sleep(0.1)

    with col2:
        # コーチのコメントをチャット形式で表示
        st.markdown("# コーチ")
        st.write("ジョージ: いい感じだよ！")
        st.write("JK: もうちょっと頑張れ！")
        st.write("メスガキ: まだまだだね！")

    # トレーニング終了ボタン
    if st.button("トレーニング終了"):
        st.session_state.page = "main"
        st.rerun()

def callback(frame):
    global tmp_count
    img = frame.to_ndarray(format="bgr24")
    results = model.predict(img, device = "cpu", show_boxes = False, show_labels = False, classes = [0])
    annotatedFrame = results[0][0].plot(labels = False, boxes = False, probs = False)

    # 検出オブジェクトの名前、バウンディングボックス座標を取得
#    names = results[0].names
#    classes = results[0].boxes.cls
#    boxes = results[0].boxes

#    for box, cls in zip(boxes, classes):
#        name = names[int(cls)]
#        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
    if results[0].keypoints.conf is None:
        cv2.imshow("YOLOv8 human pose estimation", annotatedFrame)
        return

    if len(results[0].keypoints) == 0:
        return

    # 姿勢分析結果のキーポイントを取得する
    keypoints = results[0].keypoints
    confs = keypoints.conf[0].tolist()  # 推論結果:1に近いほど信頼度が高い
    xys = keypoints.xy[0].tolist()  # 座標

    key_points = Keypoints(xys)

    # 膝の座標が0のときは除外
    if (xys[13][1] == 0.0 and xys[13][0] == 0.0 ) or (xys[14][1] == 0.0 and xys[14][0] == 0.0 ):
        return

    detect(key_points,frame)

    for index, keypoint in enumerate(zip(xys, confs)):
        score = keypoint[1]

        # スコアが0.5以下なら描画しない
        if score < 0.5:
            continue

        x = int(keypoint[0][0])
        y = int(keypoint[0][1])

    return av.VideoFrame.from_ndarray(annotatedFrame, format="bgr24")

if __name__ == "__main__":
    coach_page()
