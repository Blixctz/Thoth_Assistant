import streamlit as st
import PyPDF2
import os
from openai import OpenAI

st.set_page_config(page_title="📄 Upload Document")

st.title("📄 Upload a File to Ask Thoth")

# Load API key from secrets
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Upload the file
uploaded_file = st.file_uploader("Choose a PDF or text file", type=["pdf", "txt"])

document_text = ""

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            document_text += page.extract_text() or ""
    elif uploaded_file.type == "text/plain":
        document_text = uploaded_file.read().decode("utf-8")
    else:
        st.warning("Unsupported file type.")

    # Show content preview
    with st.expander("📃 Document Preview"):
        st.write(document_text[:2000])  # Just the first bit for safety

    # Ask a question about the file
    question = st.text_input("Ask Thoth something about this file:")
    if st.button("🧠 Ask") and question:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Thoth, an expert assistant. You will answer questions based on the uploaded document."},
                    {"role": "user", "content": f"Document content: {document_text[:6000]}"},
                    {"role": "user", "content": f"Question: {question}"}
                ],
                max_tokens=800
            )
            st.markdown(f"**Thoth says:** {response.choices[0].message.content}")
        except Exception as e:
            st.error("Thoth encountered an error.")
            st.exception(e)
