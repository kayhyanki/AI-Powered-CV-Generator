import pandas as pd
import streamlit as st
import PyPDF2 
import google.generativeai as genai
import tempfile
import os


def extract_form_data():
    job_title = st.text_input("Job Title")
    experience = st.number_input("Experience (years)")
    skills = st.text_area("Skills")
    return job_title, experience, skills

def extract_pdf_data(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_reader:
        reader = PyPDF2.PdfReader(pdf_reader)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def generate_model_content(job_title, experience, skills, bytes_resume_data):
    # Combining form data and resume text for better context
    prompt = f""" 
     You will need to generate a cover letter based on specific resume and a job description.
     Create a comprehensive, tailored model content for a {job_title} position. 
     Consider the applicant's {experience} years of experience and their key skills: {skills}. 
     Incorporate relevant information from the provided resume content: {bytes_resume_data}.
     Ensure the content is professional, persuasive, and highlights the applicant's strengths and accomplishments.
    """

    # Using the Gemini API
    genai.configure(api_key="AIzaSyDQt3j1-ZxeqDADVldbhE4OVVdsRF_NZi8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    model_content = model.generate_content(prompt)
    generated_text = model_content.text
    return generated_text

def main():
    st.markdown("""
    # 📝 GenAI-Powered Cover Letter Generator

    Generate a cover letter. All you need to do is:
    1. Upload your resume or copy your resume/experiences
    2. Paste a relevant job description
    3. Input some other relevant user/job data
    """)
    # Form data
    job_title, experience, skills = extract_form_data()
    # PDF upload
    pdf_file = st.file_uploader("Upload Resume (PDF)")    
    
    if st.button("Generate Cover Letter"):
        if pdf_file:
            #Saving the uploaded PDF to a temporary file4
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(pdf_file.read())
                temp_file_path = temp_file.name

            resume_text = extract_pdf_data(temp_file_path)
            bytes_resume_data = resume_text.encode('utf-8')

            #Remove the temporary file
            os.remove(temp_file_path)
        else:
            resume_text = ""
        
        model_content = generate_model_content(job_title, experience, skills, bytes_resume_data)
        st.text_area("Generate Cover Letter", value=model_content, height=400)

if __name__ == "__main__":
    main()
