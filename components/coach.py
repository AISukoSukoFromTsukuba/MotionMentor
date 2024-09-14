import streamlit as st
import os
import sys

sys.path.append(os.pardir)


def coach_page():
    # 2列に分割
    col1, col2 = st.columns(2)
    reps = 0

    # 左側にはカメラから入力された映像を表示
    with col1:
        video_path = "スクワット.mp4"
        st.video(video_path, start_time=0, format="video/mp4")

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


if __name__ == "__main__":
    coach_page()
