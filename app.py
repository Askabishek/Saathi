import streamlit as st
import os
from pipeline import SaathiPipeline
from audiorecorder import audiorecorder
import tempfile

st.set_page_config(page_title="Saathi - Crime Intel Assistant", layout="wide")

st.title("🎯 Saathi — Crime Intelligence Assistant")
st.markdown("---")

# Initialize Pipeline
if "pipeline" not in st.session_state:
    st.session_state.pipeline = SaathiPipeline()

# Sidebar for configuration/info
with st.sidebar:
    st.header("Settings")
    st.info("Multimodal: Text + Voice + Vision (Vision via Groq Llama 3.2)")
    if st.button("Clear History"):
        st.session_state.messages = []

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Multimodal Input Section
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.chat_input("Ask about crime statistics, safety tips, or reports...")

with col2:
    audio = audiorecorder("🎤", "⏹️")

# Process Inputs
input_to_process = None
is_audio = False

if user_input:
    input_to_process = user_input
elif len(audio) > 0:
    # Save audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        audio.export(tmp_file.name, format="wav")
        input_to_process = tmp_file.name
        is_audio = True

if input_to_process:
    # Add user message to chat
    display_text = "🎤 [Audio Message]" if is_audio else input_to_process
    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.markdown(display_text)

    # Process via Pipeline
    with st.spinner("Analyzing..."):
        response_text, audio_path = st.session_state.pipeline.process_query(input_to_process, is_audio=is_audio)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)
            if audio_path and os.path.exists(audio_path):
                st.audio(audio_path)
                
    # Cleanup temp audio if used
    if is_audio and os.path.exists(input_to_process):
        os.remove(input_to_process)
