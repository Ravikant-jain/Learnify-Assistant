#code for pdf qna
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))






def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    # response = chain(
    #     {"input_documents":docs, "question": user_question}
    #     , return_only_outputs=True)
    
    response = chain.invoke(
    {"input_documents": docs, "question": user_question}
    , return_only_outputs=True)

    print(response)
    # st.write("Reply: ", response["output_text"])
    
    return response["output_text"]


def poop(context):
    poompt = '''
Can you give me 10 quiz questions based on {}, i want it in specific json file format, like -   
[
    {{
        "question": "(Question)",
        "options": (["A.option1", "B.option2", "C.option3", "D.option4"]),
        "answer": "whole correct option"
    }},
    {{
        "question": "What is 2 + 2?",
        "options": ["A.3", "B.4", "C.5", "D.6"],
        "answer": "whole correct option"
    }},
    {{
        "question": "What is the largest planet in our solar system?",
        "options": ["A.Earth", "B.Venus", "C.Jupiter", "D.Mars"],
        "answer": "whole correct option"
    }}
]
Also each option should have alphabetical labeling as done in example.
'''.format(context)
    return poompt

from AI.Que_gen import que_gen

    
def main():
    st.set_page_config("Chat PDF")
    st.header("Welcome to the challenge learning !!")

    context = st.text_input("On what topic you want quiz?")

    if context:
        # context = st.text_input("Enter Quiz Topic", "")
        prmt=poop(context)
        r_ques=user_input(prmt)
        que_gen(r_ques)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
            
    if st.button("Prepare Quiz"):
        # st.write('okay')  # Redirect to the quiz logic page
        st.page_link("pages/Quiz.py", label="Ready for the challenge ?", icon="📝")


if __name__ == "__main__":
    main()