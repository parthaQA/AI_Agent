import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF for PDFs
from dotenv import load_dotenv

# Load environment variables
file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resource', 'data.env')
load_dotenv(file_path)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("📄 Chat with Your Document (LLM-powered)")
st.sidebar.write("Upload a document and start asking questions!")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4"]
selected_model = st.sidebar.selectbox("Choose a model:", model_options, index=0)

# Initialize OpenAI LLM with the chosen model
llm = ChatOpenAI(model_name=selected_model, openai_api_key=openai_api_key)

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf"])

if uploaded_file:
    file_contents = ""

    # Handle Text Files
    if uploaded_file.type == "text/plain":
        file_contents = uploaded_file.read().decode("utf-8")

    # Handle PDF Files
    elif uploaded_file.type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            file_contents += page.get_text("text")

    # Text Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    document_chunks = text_splitter.split_text(file_contents)

    # Store messages in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Upload a file and ask me anything!"}]

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Ask a question about the document:")

    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Process with LLM
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        chain = LLMChain(llm=llm, prompt=prompt_template)

        # Select relevant document chunk
        context = document_chunks[0] if document_chunks else "No content found."
        response = chain.run({"context": context, "question": user_input})

        # Append AI response
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)