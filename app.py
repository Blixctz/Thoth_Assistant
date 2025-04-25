import streamlit as st
from openai import OpenAI

# Set page config (must be first)
st.set_page_config(page_title="Thoth Assistant", layout="centered")

# Password protection
CORRECT_PASSWORD = st.secrets["THOTH_SECRET"]
password = st.text_input("Enter your passphrase", type="password")
if password != CORRECT_PASSWORD:
    st.warning("Access denied.")
    st.stop()

# Title
st.title("🧠 Thoth Assistant with Memory")

# Use Streamlit Secrets (for cloud)
api_key = st.secrets["OPENAI_API_KEY"]
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

        


