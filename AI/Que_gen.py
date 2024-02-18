#main file
from dotenv import load_dotenv
import os
load_dotenv()


from IPython.display import display
from IPython.display import Markdown
import textwrap


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel('gemini-pro')




def poop(context):
    poompt=f'''
Can you give me 10 quiz questions based on {context}, i want it in specific json file format, like -   
[
    {
        "question": "(Question)",
        "options": (["option1", "option2", "option3", "option4"]),
        "answer": "(answer here)"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "B"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Venus", "Jupiter", "Mars"],
        "answer": "C"
    }
]

'''
    return poompt

# poompt=poop('hey')
# response = model.generate_content(poompt)

import json
import re

def extract_questions(json_string):
    questions = []
    
    # Define regex patterns to extract question, options, and answer
    question_pattern = r'"question":\s*"([^"]*)"'
    options_pattern = r'"options":\s*\[([^\]]*)\]'
    answer_pattern = r'"answer":\s*"([^"]*)"'
    
    # Find all matches of questions, options, and answers using regex
    question_matches = re.findall(question_pattern, json_string)
    options_matches = re.findall(options_pattern, json_string)
    answer_matches = re.findall(answer_pattern, json_string)
    
    # Map options to letters A, B, C, etc.
    option_letters = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    # Iterate over matches and populate the dictionary
    for i in range(len(question_matches)):
        question = question_matches[i]
        # Split options by comma and strip whitespace and quotes
        options = [option.strip('" ') for option in options_matches[i].replace('\n', '').split(',')]
        answer = answer_matches[i]
        # Map answer to its corresponding letter
        answer_letter = next(option_letters)
        # Append question dictionary to the list
        questions.append({"question": question, "options": options, "answer": answer_letter})
    
    return questions


import json
def save_q(answers):
    file_path = r"Jsons\ques.json"
    with open(file_path, "w") as json_file:
        json.dump(answers, json_file)





def que_gen(q_set):
    questions_dict=extract_questions(q_set)
    save_q(questions_dict)

    pass