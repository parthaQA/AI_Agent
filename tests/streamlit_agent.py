import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resource', 'data.env')
load_dotenv(file_path)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=openai_api_key)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful AI assistant. Answer the following: {question}"
)

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit UI
st.title("Simple LLM App with LangChain & OpenAI")

st.write("Ask me anything!")

user_input = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if user_input:
        response = chain.run(user_input)
        st.success(response)
    else:
        st.warning("Please enter a question.")