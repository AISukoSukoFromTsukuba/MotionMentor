import streamlit as st
from components import coach


def main():
    if "page" not in st.session_state:
        st.session_state.page = "main"

    # main page
    if st.session_state.page == "main":
        st.title("Hello World!")
        st.write("Welcome to Streamlit!")
        if st.button("next page"):
            st.session_state.page = "coach"
            st.rerun()
    elif st.session_state.page == "coach":
        coach.coach_page()


if __name__ == "__main__":
    main()
