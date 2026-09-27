import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Page Configuration
st.set_page_config(page_title="EduGenie - Learning Assistant", page_icon="🎓")
st.title("🎓 EduGenie: Learning Assistant")
st.sidebar.title("EduGenie Tools")
if st.sidebar.button("Generate Quiz"):
    prompt="Create a 3-question multiple-choice quize based on our study topic."
    st.session_state.messages.append({"role":"user","content":prompt})
    st.rerun()
              # Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY `.env` file-la kaanawillai! Key-a add pannunga.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=api_key)

# Chat History Session State Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ungaloda kelviya inga type pannunga..."):
    # Render User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("EduGenie yosikkirdhu..."):
            try:
                response=client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                    config={'system_instruction':"You are EduGenie, a helpful tutor for students..."}
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")