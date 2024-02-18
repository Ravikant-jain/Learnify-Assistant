import streamlit as st
# Importing the main function from Quiz_logic.py
from Quiz_logic import ren_quiz

def main():
    st.title("Quiz Topic Selection")
    st.write("Please enter a topic for the quiz.")

    # Text input for quiz topic
    user_input = st.text_input("Enter Quiz Topic", "")

    # Button to start the quiz
    if st.button("Start Quiz"):
        st.write('okay')  # Redirect to the quiz logic page
        # st.page_link("quiz_logic.py", label="Home", icon="🏠")
if __name__ == "__main__":
    main()
