import streamlit as st
import PyPDF2
import io
import os
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path=".venv/.env")

st.set_page_config(page_title="AI Resume Analyzer", page_icon=":robot_face:", layout="centered")

st.title("AI Resume Analyzer")
st.markdown("""Upload your resume and let the AI analyze it for you!""")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf","txt"])
job_role = st.text_input("Job Title")
analyze = st.button("Analyze")

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return "Unsupported file format"

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        

        if not file_content.strip():
            st.error("File is empty")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback.
Focus on the following aspects:
Content clarity and impact
Skills presentation
Experience descriptions
Specific improvements for {job_role if job_role else 'general job applications'}

Resume content:
{file_content}

Please provide your analysis in a clear, structured format with specific recommendations."""

        client = genai.Client(api_key=GOOGLE_API_KEY)
        with st.spinner("Analyzing your resume..."):
            response = client.models.generate_content(
                model="gemini-3.5-pro", 
                contents=f"You are an expert in resume analysis with experience as HR Manager.\n\n{prompt}"
            )
        max_tokens = 1000
        st.markdown("### Analysis Completed")
        st.markdown(response.text)
    except Exception as e:  
        st.error(f"An error occurred: {e}")
