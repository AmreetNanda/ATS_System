from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import PyPDF2

import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from langchain_community.llms import Ollama
import base64


# Create response from LLM model, input, pdf and prompt
def get_model_response(input_text, pdf_content, prompt):
    model = Ollama(model="gemma3", temperature=0.2)
    final_input = f"{input_text}\n\nResume:\n{pdf_content}\n\nPrompt:\n{prompt}"
    response = model.invoke(final_input)
    return response

# Using PyPDf (PDF to Text method)
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text += page.extract_text() or ""
    return text


# Create a streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF) ...", type =["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

#Prompt Engineering
input_prompt1 = """You are an experienced technical human resource manager, your task is to review the provided resume against the job description. Please share your professional evaluation on whether the candidates profile aligns with the role. Highlight the strengths and weakness of the applicant in relation to the specified job requirements"""

input_prompt3 = """
Hey act like a skilled or very experience ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analyst and big data engineer. You must consider that the job market is very competitive and you should provide best assistance for improving the resumes. Align the percentage matching based on job description and the missing keywords with high accuracy
resume:{text}
description:{jd}
I want the response in a single string having the structure {{"JD match":"%", "missingkeywords:[]", "Profile Summary":" "}}
"""
submit = st.button("Submit")
if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)

        final_prompt = input_prompt3.format(
            text=resume_text,
            jd=input_text
        )

        response = get_model_response(
            input_text,
            resume_text,
            final_prompt
        )

        st.subheader(response)
    else:
        st.warning("Please upload a PDF file.")

