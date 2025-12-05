# ATS Resume Expert
---
A Streamlit-based **ATS (Applicant Tracking System) Resume Expert** that analyzes resumes against job descriptions using AI.  
It allows HR professionals or recruiters to quickly evaluate candidates, extract key information, and determine the alignment between resumes and job descriptions.

- **PDF Resume Upload**: Upload candidate resumes in PDF format.  
- **PDF Preview**: Display the first page of the resume using `pdf2image`.  
- **OCR Text Extraction**: Extract text from PDF images using `pytesseract` for AI processing.  
- **Job Description Analysis**: Input a job description to compare against the resume.  
- **AI-Powered Evaluation**: Uses the Ollama model to:
  - Assess alignment with job description  
  - Highlight missing skills and keywords  
  - Generate a profile summary and recommendations  
- **Visual Dashboard**: Shows a card-style layout with JD match %, missing keywords, and profile summary.


## Requirements
- Python 3.12+
- Local Ollama server with Gemma3 model
- GPU-enabled environment recommended for faster response

## Features
- Run LLaMA3 locally using Ollama
- Use LangChain's prompt templates
- Smooth Ul using Streamlit
- Real-time response generation

## Technologies Used:
- Streamlit, Python, pytesseract, poppler
- Models used: Gemma3

## Project Structure

```bash
Langchain_basic/
├─ assets/ (optional for images, sample PDFs, logos)
├─ app.py (simple ATS system)             
├─ advanced_ats.py  (advanced ats system) 
├─ README.md
└─ requirements.txt      # Python dependencies
```

## Installation

## 🛠 Installation

### 1. Clone the repo
```bash
git clone https://github.com/AmreetNanda/ATS_System.git
cd atssystem
```
### 2. Requirements.txt
```bash
langchain
langchain_community
langchain-core
langchain-classic
ipykernel
streamlit
python-dotenv
PyPDF2
pdf2image
pytesseract
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Install Poppler and pytesseract
```bash
- Install Poppler (required by pdf2image):
- Download from Poppler for Windows and add the bin folder to PATH.
- Install Tesseract OCR (required by pytesseract): https://github.com/tesseract-ocr/tesseract
```
### 4. Run Streamlit app
```bash
streamlit run app.py or streamlit run advanced_ats.py

```
Open in your browser:
```
👉 http://localhost:8501/
👉 Enter a Job Description in the text area.
👉 Upload a resume PDF.
👉 Click one of the buttons:
👉 Tell me about the resume – Get a professional evaluation.
👉 Percentage match [Accept / Reject] – Get a percentage match and missing keywords.
👉 Submit – Get detailed analysis with profile summary and visual card display.
```

## Demo
https://github.com/user-attachments/assets/9c2d55ad-38e3-43c4-b166-d9a764646d77

## License

[MIT](https://choosealicense.com/licenses/mit/)


