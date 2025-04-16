import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Set page config (must be first)
st.set_page_config(page_title="Thoth Assistant", layout="centered")

# Load environment variables
load_dotenv()

# Password protection
CORRECT_PASSWORD = os.getenv("THOTH_SECRET")
password = st.text_input("Enter your passphrase", type="password")
if password != CORRECT_PASSWORD:
    st.warning("Access denied.")
    st.stop()

# Title
st.title("🧠 Thoth Assistant with Memory")

# Load environment variables
load_dotenv()

# Load OpenAI API key from .env (locally) or secrets (cloud)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception as e:
        st.error("No OpenAI API key found. Please set it in .env or Streamlit Secrets.")
        st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize memory if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Thoth, a wise and compassionate assistant who remembers past conversations."}
    ]

# User input
prompt = st.text_area("Say something to Thoth:")

# On button press
if st.button("Speak, Thoth") and prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages,
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.markdown(f"**Thoth says:** {reply}")
    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)

# Show memory log
with st.expander("🧾 Chat History"):
    for msg in st.session_state.messages[1:]:
        role = msg["role"].capitalize()
        st.write(f"**{role}**: {msg['content']}")

        


