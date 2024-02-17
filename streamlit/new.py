# import streamlit as st
# import json
# import time

# #func to fetch question
# def load_quiz_datafrm(file_path):
#     with open(file_path, 'r') as file:
#         quiz_data = json.load(file)
#     return quiz_data

# #imp func to display the question
# def button_with_question_and_options(button_number,line):
#     # Get or create session state for time tracking and selected option
#     state = st.session_state
#     if 'start_times' not in state:
#         state.start_times = {}
#     if 'selected_option' not in state:
#         state.selected_option = {}

#     checkbox_key = f"Checkbox {button_number}"
#     checkbox_state = st.checkbox(f"Question number {button_number+1}")

#     # Check if checkbox is ticked to reveal the question and selectbox
#     if checkbox_state:
#         question = line['question']
#         st.write(f"**Question:** {question}")

#         options = line['options']
#         selected_option_key = f"Selected Option {button_number}"
#         state.selected_option[selected_option_key] = st.selectbox(f"Select an option for {button_number+1}:", options)

#         start_time_checkbox_key = f"Start Time Checkbox {button_number}"
#         if start_time_checkbox_key not in state.start_times:
#             state.start_times[start_time_checkbox_key] = None

#         if state.start_times[start_time_checkbox_key] is None:
#             state.start_times[start_time_checkbox_key] = time.time()  # Record the start time when the checkbox is ticked
        
#         # Submit button
#         if st.button(f"Submit Ans: {button_number+1}"):
#             start_time = state.start_times[start_time_checkbox_key]
#             if start_time is not None:
#                 end_time = time.time()  # Record the end time when the button is clicked
#                 elapsed_time = end_time - start_time  # Calculate the elapsed time
#                 selected_option = state.selected_option[selected_option_key]
#                 st.write(f"Time taken for Question {button_number+1}: {elapsed_time:.2f} seconds")
#                 st.write(f"Selected option for Question {button_number+1}: {selected_option}")
                


# def main():
#     st.title("All the best")
#     quiz_data = load_quiz_datafrm('quiz_data.json')
#     answer_sheet={}
#     for qnum,line in enumerate(quiz_data):  # Adjust the range based on the number of buttons
#         button_with_question_and_options(qnum,line)

        
#     # file_path = "data.json"

#     # # Write the dictionary to a JSON file
#     # with open(file_path, "w") as json_file:
#     #     json.dump(answer_sheet, json_file)

#     # print("JSON file saved successfully.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import json
import time

# Function to load quiz data from a JSON file
def load_quiz_datafrm(file_path):
    with open(file_path, 'r') as file:
        quiz_data = json.load(file)
    return quiz_data

# Function to display a question with options and track time
def button_with_question_and_options(button_number, line):
    # Get or create session state for time tracking and selected option
    state = st.session_state
    if 'start_times' not in state:
        state.start_times = {}
    if 'selected_option' not in state:
        state.selected_option = {}
    if 'answers' not in state:
        state.answers = {}

    checkbox_key = f"Checkbox {button_number}"
    checkbox_state = st.checkbox(f"Question number {button_number+1}")

    # Check if checkbox is ticked to reveal the question and selectbox
    if checkbox_state:
        question = line['question']
        st.write(f"**Question:** {question}")

        options = line['options']
        selected_option_key = f"Selected Option {button_number}"
        state.selected_option[selected_option_key] = st.selectbox(f"Select an option for {button_number+1}:", options)

        start_time_checkbox_key = f"Start Time Checkbox {button_number}"
        if start_time_checkbox_key not in state.start_times:
            state.start_times[start_time_checkbox_key] = None

        if state.start_times[start_time_checkbox_key] is None:
            state.start_times[start_time_checkbox_key] = time.time()  # Record the start time when the checkbox is ticked
        
        # Submit button
        if st.button(f"Submit Ans: {button_number+1}"):
            start_time = state.start_times[start_time_checkbox_key]
            if start_time is not None:
                end_time = time.time()  # Record the end time when the button is clicked
                elapsed_time = end_time - start_time  # Calculate the elapsed time
                selected_option = state.selected_option[selected_option_key]
                # st.write(f"Time taken for Question {button_number+1}: {elapsed_time:.2f} seconds")
                # st.write(f"Selected option for Question {button_number+1}: {selected_option}")
                st.write('Submitted')   

                # Save the answer and time taken to solve the question
                answer_sheet = {
                    'answer': selected_option,
                    'time_taken': elapsed_time
                }
                state.answers[button_number] = answer_sheet

                #saving the answers in a JSON file
                save_answers_to_json(state.answers)

# Function to save answers to a JSON file
def save_answers_to_json(answers):
    file_path = "answer_sheet.json"
    with open(file_path, "w") as json_file:
        json.dump(answers, json_file)

def main():
    st.title("All the best")
    quiz_data = load_quiz_datafrm(r'D:\Github\Edu-AiX\AI\ques.json')
    # answer_sheet = {}
    for qnum, line in enumerate(quiz_data):
        button_with_question_and_options(qnum, line)

if __name__ == "__main__":
    main()
