import google.generativeai as genai
import streamlit as st

api_key = st.secrets["gemini_api"]  # Ensure this is set in your Streamlit secrets
genai.configure(api_key=api_key)
# Initialize the Generative Model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to get the response from the model
def get_response(prompt):
    context_before = "Give me a short summary of the book"
    context_after = """You should consider reading it if: (3 to 4 reasons/person interests),
                       you should skip it if: (3 to 4 reasons/person interests)"""
    prompt = f"{context_before} {prompt}. {context_after}"
    response = model.generate_content([prompt])
    return response.text

# Streamlit App
st.set_page_config(page_title="Book Summary Chatbot", page_icon="📚", layout="wide")

# Custom CSS for chat layout
st.markdown("""
    <style>
    .chat-container {
        background-color: #F9F9F9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin: 20px auto;
        max-width: 700px;
    }
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .user-message {
        background-color: #DCF8C6;
        text-align: right;
    }
    .assistant-message {
        background-color: #E4E6EB;
        text-align: left;
    }
    .centered-header {
        text-align: center;
        color: #4A90A2;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Page Header
st.markdown("<h1 class='centered-header'>Book Summary Chatbot</h1>", unsafe_allow_html=True)
st.write("Note: This chatbot will take the name of a book and provide a summary along with advice on whether you should read it or not.")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Container
with st.container():
    chat_container = st.container()

    # Display existing chat messages in a styled box
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"<div class='chat-message user-message'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

# Handle new input - always at the bottom
prompt = st.chat_input("Please enter the name of a book")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True)

    response = get_response(prompt)
    #st.write(list(response))
    if response.startswith("##"):
        response = response.replace("##", "", 2)
        for i in range(1):
          response = response.replace(" ", "", 1)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):

        st.markdown(f"<div class='chat-message assistant-message'>{response}</div>", unsafe_allow_html=True)
