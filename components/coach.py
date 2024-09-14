import streamlit as st
import os
import sys

sys.path.append(os.pardir)
from components.instructor import JK_manager, jordge, mesugaki


import time


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

        st.session_state.input_text = "動きが止まっています。"
        st.markdown(f"# コーチ : {st.session_state.coach}")
        if st.session_state.coach == "ジョージ":
            st.markdown(jordge.jordge(st.session_state.input_text))
        elif st.session_state.coach == "JK":
            st.markdown(JK_manager.JK_manager(st.session_state.input_text))
        elif st.session_state.coach == "メスガキ":
            st.markdown(mesugaki.mesugaki(st.session_state.input_text))

        # 1秒待機
        time.sleep(1)

    # トレーニング終了ボタン
    if st.button("トレーニング終了"):
        st.session_state.page = "main"
        st.rerun()


if __name__ == "__main__":
    coach_page()
