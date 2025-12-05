from dotenv import load_dotenv
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""
os.environ["LANGCHAIN_API_KEY"] = ""
import langchain

import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import PyPDF2
import pytesseract

import json

from langchain_community.llms import Ollama
import base64


# Create response from LLM model, input, pdf and prompt
def get_model_response(input_text, pdf_content, prompt):
    final_input = f"{input_text}\n\nResume:\n{pdf_content}\n\nPrompt:\n{prompt}"
    model = Ollama(model="gemma3", temperature=0.2)
    response = model.invoke(final_input)
    if isinstance(response, dict) and "message" in response:
        return response["message"]["content"]
    else:
        return str(response)


# Using PDF2Image (PDF to Image method)
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF pages to images
        images = pdf2image.convert_from_bytes(
            uploaded_file.read(),
            poppler_path=r"C://Program Files (x86)//poppler-25.12.0//Library//bin"
        )
        
        # Take first page for display
        first_page = images[0]

        # Convert to byte array for display
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_image_for_display = base64.b64encode(img_byte_arr).decode()

        # OCR the entire PDF to extract text
        full_text = ""
        for img in images:
            text = pytesseract.image_to_string(img)
            full_text += text + "\n"

        return full_text, pdf_image_for_display
    else:
        raise FileNotFoundError("No file uploaded")

def display_card_layout(data):
    st.markdown("""
        <style>
        .card {
            background-color: #3b2d29;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #e0e0e0;
        }
        .title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .keyword {
            display: inline-block;
            background-color: #e3f2fd;
            color: #0d47a1;
            padding: 6px 12px;
            margin: 4px;
            border-radius: 8px;
            font-size: 14px;
            border: 1px solid #90caf9;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <div class="title">🟩 JD Match</div>
        <p style="font-size:28px; font-weight:bold;">{data['JD match']}</p>
    </div>

    <div class="card">
        <div class="title">🟨 Missing Keywords</div>
        {''.join([f'<span class="keyword">{kw}</span>' for kw in data['missingkeywords']])}
    </div>

    <div class="card">
        <div class="title">🟦 Profile Summary</div>
        <p>{data['Profile Summary']}</p>
    </div>
    """, unsafe_allow_html=True)

# Create a streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF) ...", type =["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

#Prompt Engineering
input_prompt1 = """You are an experienced technical human resource manager, your task is to review the provided resume against the job description. Please share your professional evaluation on whether the candidates profile aligns with the role. Highlight the strengths and weakness of the applicant in relation to the specified job requirements"""

input_prompt2 = """You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First output should be as percentage and then keywords missing and at last the final thought"""

input_prompt3 = """
Hey act like a skilled or very experience ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analyst and big data engineer. You must consider that the job market is very competitive and you should provide best assistance for improving the resumes. Align the percentage matching based on job description and the missing keywords with high accuracy
resume:{text}
description:{jd}
I want the response in a single string having the structure {{"JD match":"%", "missingkeywords:[]", "Profile Summary":" "}}
"""

submit1 = st.button("Tell me about the resume")
submit2 = st.button("Percentage match [Accept / Reject]")
if submit1:
    if uploaded_file is not None:
        resume_text, pdf_image = input_pdf_setup(uploaded_file)
        st.image(pdf_image, caption="First page of resume")
        st.subheader("The response is ...")
        final_prompt = input_prompt1.format(text=resume_text, jd=input_text)
        response = get_model_response(input_text, resume_text, final_prompt)
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        resume_text, pdf_image = input_pdf_setup(uploaded_file)
        st.image(pdf_image, caption="First page of resume")
        st.subheader("The response is ...")
        final_prompt = input_prompt2.format(text=resume_text, jd=input_text)
        response = get_model_response(input_text, resume_text, final_prompt)
        st.write(response)
    else:
        st.write("Please upload the resume")

submit3 = st.button("Submit")
if submit3:
    if uploaded_file is not None:
        resume_text, pdf_image = input_pdf_setup(uploaded_file)
        st.image(pdf_image, caption="First page of resume")
        final_prompt = input_prompt1.format(text=resume_text, jd=input_text)
        response = get_model_response(input_text, resume_text, final_prompt)
        # st.write(response)
        # st.subheader(response)
        clean = response.replace("```json", "").replace("```", "")
        data = json.loads(clean)
        display_card_layout(data)

    else:
        st.warning("Please upload a PDF file.")



