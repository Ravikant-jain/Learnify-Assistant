import json
import matplotlib.pyplot as PageLayout
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.table import Table
import numpy as np
import matplotlib.pyplot as plt

# Load data from JSON files
with open(r'D:\Github\Edu-AiX\Jsons\ques.json', 'r') as f:
    questions_data = json.load(f)

with open(r'D:\Github\Edu-AiX\Jsons\answer_sheet.json', 'r') as f:
    answer_sheet_data = json.load(f)
    
    
    
def cal_marks(qd,ad):
    ak=[]
    sk=[]
    res_list=[]
    
    for i in qd:
        # print(i['answer'])
        ak.append(i['answer'])
        
    for i2 in ad:
        td=ad[i2]
        sk.append(td['answer'][:1])
        
    for idx,ca in enumerate(ak):
        if ca==sk[idx]:
            res_list.append(1)
            
        else:
            res_list.append(0)
    return res_list

mrk=cal_marks(questions_data,answer_sheet_data)

que_time=[]
for i2 in answer_sheet_data:
    td=answer_sheet_data[i2]
    que_time.append(td['time_taken'])
    
    
    

def fin():
    mrk=cal_marks(questions_data,answer_sheet_data)
    que_time=[]
    for i2 in answer_sheet_data:
        td=answer_sheet_data[i2]
        que_time.append(td['time_taken'])
    viz(mrk,que_time)

# Example lists (replace these with your actual lists)
marks = mrk
q_time = que_time

def viz(marks,q_time):
    text='''
    Congratulations on completing your test! 

    Remember, every challenge you face is an opportunity to learn and grow. 
    Keep pushing yourself, and believe in your abilities. 
    Your determination and hard work will surely lead to even greater success in the future.
    Stay focused, stay motivated, and never give up. You're capable of achieving amazing things! 

    Best wishes for your next endeavor! 
    '''

    # Create a PDF file
    with PdfPages('report_card.pdf') as pdf:
        # Add a message on the first page
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.axis('off')
        ax.text(0.5, 0.5, text, fontsize=12, ha='center', va='center')
        pdf.savefig()
        plt.close()

        # Create a table with question numbers and correctness
        table_data = [['Question Number', 'Correctness']]
        for i, mark in enumerate(marks):
            table_data.append([f'Question {i+1}', 'Correct' if mark == 1 else 'Wrong'])

        fig, ax = plt.subplots(figsize=(12,8))
        ax.axis('off')  # Turn off axis for the table
        table = Table(ax)
        table.set_fontsize(13)
        table.scale(2, 2)
        
        # Add data to the table
        for i, row in enumerate(table_data):
            for j, cell in enumerate(row):
                table.add_cell(i, j, width=0.1, height=0.05, text=cell, loc='center', facecolor='white')
        
        ax.add_table(table)
        ax.annotate('This table shows the correctness of answers for each question.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()

        # Pie chart for the overall correctness
        correct_count = sum(marks)
        wrong_count = len(marks) - correct_count
        plt.figure(figsize=(6, 6))
        labels = ['Correct Answers', 'Wrong Answers']
        sizes = [correct_count, wrong_count]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['green', 'red'])
        plt.title('Overall Correctness of Answers')
        plt.axis('equal')
        plt.annotate('This pie chart shows the distribution of correct and wrong answers.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()

        # Violin plot for time taken
        plt.figure(figsize=(8, 5))
        plt.violinplot(q_time, vert=False)
        plt.xlabel('Time Taken (seconds)')
        plt.title('Violin Plot of Time Taken for Each Question')
        plt.annotate('This violin plot shows the spread of time taken to answer each question.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()

        # Histogram for time taken
        plt.figure(figsize=(8, 5))
        plt.hist(q_time, bins=10, color='skyblue', edgecolor='black')
        plt.xlabel('Time Taken (seconds)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Time Taken for Each Question')
        plt.annotate('This histogram shows the distribution of time taken to answer questions.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()

        # Line plot for time taken
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(q_time)+1), q_time, marker='o', color='green')
        plt.xlabel('Question Number')
        plt.ylabel('Time Taken (seconds)')
        plt.title('Line Plot of Time Taken for Each Question')
        plt.grid(True)
        plt.annotate('This line plot shows the trend of time taken to answer questions.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()

        # Heatmap for time taken
        plt.figure(figsize=(8, 5))
        heatmap_data = [q_time, marks]
        plt.imshow(heatmap_data, cmap='viridis', aspect='auto')
        plt.colorbar(label='Time Taken (seconds)')
        plt.xlabel('Question Number')
        plt.ylabel('Correctness (1 for Correct, 0 for Wrong)')
        plt.title('Heatmap of Time Taken for Each Question')
        plt.annotate('This heatmap shows the relationship between correctness and time taken for each question.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()

        # Scatter plot with color encoding for correctness of answers
        plt.figure(figsize=(8, 5))
        plt.scatter(range(1, len(q_time)+1), q_time, c=marks, cmap='coolwarm')
        plt.colorbar(label='Correctness (1 for Correct, 0 for Wrong)')
        plt.xlabel('Question Number')
        plt.ylabel('Time Taken (seconds)')
        plt.title('Scatter Plot of Time Taken with Color Encoding for Correctness')
        plt.annotate('This scatter plot shows the relationship between time taken and correctness for each question.', xy=(0.5, 0.98), xycoords='axes fraction', ha='center', va='top')
        pdf.savefig()
        plt.close()


fin()