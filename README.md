The project consist of 2 files. 

The streamlit_agent.py file is consist code to create a simple llm based application with openAI and streamlit. A user can ask any question to the agentic AI.

The second file streamlit_agent_for_read_file_content.py is another llm based application created with openAI and streamlit. The purpose of application is to upload a pdf and txt files and then ask any question regarding the file uploaded. The agent will answer as per document.

I have used below libraries to create the application.The python version is 3.12

langchain~=0.3.19
openai
PyMuPDF
tiktoken
langchain-community~=0.3.18
python-dotenv~=1.0.1
streamlit~=1.42.2

Streamlit is a python framework to build web pages. 
["gpt-3.5-turbo", "gpt-4"] is used to build the application.


To run the application use command:

streamlit run <file name>
Enter the email id.
the application is hosted in local server.

