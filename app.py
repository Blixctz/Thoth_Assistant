import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ✅ MUST come first before any Streamlit commands
st.set_page_config(page_title="Thoth Assistant", layout="centered")

# Load secrets from .env file
load_dotenv()


# Password protection
CORRECT_PASSWORD = os.getenv("THOTH_SECRET")
password = st.text_input("Enter your passphrase", type="password")
if password != CORRECT_PASSWORD:
    st.warning("Access denied.")
    st.stop()

# Title
st.title("🧠 Thoth Assistant")

# Setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# User input
prompt = st.text_area("Say something to Thoth:")

if st.button("Speak, Thoth") and prompt:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(f"**Thoth says:** {response.choices[0].message.content}")
    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)
        


