import streamlit as st
import os, sys

#sys.path.append(os.pardir)
from components import coach


st.set_page_config()


def main_page():
    st.markdown('<p style="font-size: 60px;">MotionMentor</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-family:UD Digi Kyokasho NK-R;font-size: 30px;">あなたの筋トレをサポートします。</p>', unsafe_allow_html=True)
    tabs_font_css = """
    <style>
    div[class*="stSelectbox"] label p {
    font-size: 30px;
    font-family:UD Digi Kyokasho NK-R;
    }
    div[class*="row-widget"] label p {
    font-family:UD Digi Kyokasho NK-R;
    }
    div[class*="stTextInput"] label p {
    font-size: 30px;
    font-family:UD Digi Kyokasho NK-R;
    }
    div[class*="stButton"] label p {
    font-size: 30px;
    font-family:UD Digi Kyokasho NK-R;
    }
    </style>
    """

    st.write(tabs_font_css, unsafe_allow_html=True)
    st.session_state.train_menu = st.selectbox("種目", ["スクワット", "腕立て伏せ"])

    # 回数をテキストボックスで入力
    st.session_state.reps = int(st.text_input("回数", 10))

    # コーチの選択
    st.session_state.coach = st.selectbox("コーチ", ["ジョージ", "JK", "メスガキ"])

    # トレーニング開始ボタン
    if st.button("トレーニング開始"):
        # 全ての入力が完了しているか確認
        if st.session_state.train_menu and st.session_state.reps and st.session_state.coach:
            st.session_state.page = "coach"
            st.rerun()
        else:
            st.error("全ての項目を入力してください。")


def main():
    if "page" not in st.session_state:
        st.session_state.page = "main"

    # main page
    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "coach":
        coach.coach_page()


if __name__ == "__main__":
    main()
