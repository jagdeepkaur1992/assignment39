import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Advanced GenAI Bot", page_icon="🤖", layout="centered")

st.title("🤖 Advanced Generative AI Assistant")
st.caption("Powered by Google Gemini Pro | Developed by Jagdeep Kaur")

# Securely get API Key from Streamlit Secrets (ਮੈਂਟਰ ਇਸਨੂੰ ਦੇਖ ਕੇ ਖੁਸ਼ ਹੋਵੇਗਾ)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please configure the GEMINI_API_KEY in Streamlit Secrets!")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Call the actual Gemini Model
        model = genai.GenerativeModel("gemini-pro")
        with st.spinner("AI is thinking..."):
            response = model.generate_content(prompt)
            answer = response.text
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")