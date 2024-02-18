import streamlit as st
import fitz  # PyMuPDF
from AI.marks import fin

fin()

st.set_page_config(layout='wide')

def render_pdf(file_path):
    doc = fitz.open(file_path)
    num_pages = doc.page_count

    conversation_history_resource = st.session_state.get('conversation_history', [])
    
    par_c1, par_c2, par_c3 = st.columns([6, 1, 2])

    with par_c1:
        page_number = st.session_state.get('page_number', 1)
        page = doc.load_page(page_number - 1)
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        if col1.button("Previous Page") and page_number > 1:
            st.session_state.page_number -= 1
        if col4.button("Next Page") and page_number < num_pages:
            st.session_state.page_number += 1
        image_bytes = page.get_pixmap().tobytes()
        st.image(image_bytes, use_column_width=True)


if __name__ == "__main__":
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history_resource = []
    render_pdf(r"D:\Github\Edu-AiX\report_card.pdf")