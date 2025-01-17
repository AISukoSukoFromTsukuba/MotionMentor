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
sys.path.append(os.pardir)
from components.coach_voice_generator import vvox_test
from components.instructor import jordge,JK_manager, mesugaki
tmp_count = 0
form_check_start = 0
form_check_cancel = 0
flag_check_start = 0
flag = 0
mindegreeRight = 180
mindegreeLeft = 180
prev_tmp_count = 0
inner_thigh = "完璧"

if "squatcount" not in st.session_state:
    st.session_state.count = 0



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
    global prev_tmp_count
    global inner_thigh


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

    if hip_knee_ankle_ratio_left < 0.8 and hip_knee_ankle_ratio_right < 0.8:
        if flag == 1:
            flag = 0
            with lock:
                prev_tmp_count = tmp_count
                tmp_count += 1

        mindegreeRight = min(degreeRight, mindegreeRight)
        mindegreeLeft = min(degreeLeft, mindegreeLeft)
    elif hip_knee_ankle_ratio_left > 1.0 and hip_knee_ankle_ratio_right > 1.0:
        if flag == 0 and tmp_count > 0:
            with lock:
                if mindegreeRight < 85 and mindegreeLeft < 85:
                    st.session_state.leg_degree = "座っていると感じられるほど膝が曲がりすぎている状態"
                elif mindegreeRight < 100 and mindegreeLeft < 100:
                    st.session_state.leg_degree = "膝がほどよく曲がっていてとてもいい状態"
                elif mindegreeRight < 120 and mindegreeLeft < 120:
                    st.session_state.leg_degree = "膝の曲がりが中途半端で足が伸びている状態"
                else:
                    st.session_state.leg_degree = "膝の曲がりが不十分で、もう少し曲げるべき状態"
                mindegreeRight = 180
                mindegreeLeft = 180
        
        flag = 1
        
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
    #    flag_check_start = 0 # 開始時のカウントダウン（肩と踵の位置チェック）に使うフラグ
    #    with lock:
    #        tmp_count = 0
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
    with lock:

        print("---------------------------inner_thigh-----------------------------------------------------------")
        if abs(x_left) > 20 and abs(x_right) > 20:
            inner_thigh= "完璧"
        elif abs(x_left) > 10 and abs(x_right) > 10:
            inner_thigh = "足幅狭い"
        else:
            inner_thigh = "内股"



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
    global tmp_count
    global prev_tmp_count
    global inner_thigh
    # 2列に分割
    reps = 0
    if 'coach_event' not in st.session_state:
        st.session_state.coach_event = False

    if "leg_degree" not in st.session_state:
        st.session_state.leg_degree = ""

    webrtc_streamer(key="example", video_frame_callback=callback)
    col1, col2 = st.columns(2)  # 2列のコンテナを用意する
    with col1:
        if st.session_state.coach == "ジョージ":
            image = cv2.imread("components\coach_images\jordge.jpg")
        elif st.session_state.coach == "JK":
            image = cv2.imread("components\coach_images\JK.jpg")
        elif st.session_state.coach == "メスガキ":
            image = cv2.imread("components\coach_images\mesugaki.jpg")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        st.image(image,width=200)
    with col2:
        with st.empty():
            while True:
                st.markdown(f'<p style="font-size: 40px;">回数：{tmp_count}/{st.session_state.reps}<br>フォーム：{inner_thigh}</p>', unsafe_allow_html=True)
                count_chop = st.session_state.reps // 3
                if tmp_count != 0 and tmp_count % count_chop == 0:
                    st.session_state.coach_event = True
                    prev_tmp_count = tmp_count
                else:
                    time.sleep(0.3)
                if st.session_state.reps <= tmp_count:
                    st.session_state.coach_event = False
                    break

                if st.session_state.coach_event:
                    #st.markdown(inner_thigh)
                    input_text = f"""
                    トレーニングメニュー: {st.session_state.train_menu}
                    現在の回数:{tmp_count}
                    目標回数:{st.session_state.reps}
                    姿勢の状態: {inner_thigh}
                    """
                    #st.markdown(f"# コーチ : {st.session_state.coach}")
                    if st.session_state.coach == "ジョージ":
                        coach_comment = jordge.jordge(input_text)
                        #st.markdown(coach_comment)
                        vvox_test(coach_comment, 11, 1.1)
                        st.session_state.coach_event = False
                    elif st.session_state.coach == "JK":
                        coach_comment = JK_manager.JK_manager(input_text)
                        #st.markdown(coach_comment)
                        vvox_test(coach_comment, 2, 1.1)
                        st.session_state.coach_event = False
                    elif st.session_state.coach == "メスガキ":
                        coach_comment = mesugaki.mesugaki(input_text)
                        #st.markdown(coach_comment)
                        vvox_test(coach_comment, 3, 1.1)
                        st.session_state.coach_event = False
    


    if st.button("トレーニング終了"):
        st.write("お疲れ様でした！！！")
        time.sleep(3)
        st.session_state.page = "main"
        st.rerun()

def callback(frame):
    global tmp_count
    img = frame.to_ndarray(format="bgr24")

    results = model.predict(img, device = "cuda", show_boxes = False, show_labels = False, classes = [0])

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
