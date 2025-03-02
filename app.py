import streamlit as st
import pdfplumber
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set branding colors
st.set_page_config(page_title="Impact Analytica", page_icon="🌍", layout="wide")

# Custom styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f4f7f5;
        }
        .title {
            color: #2E8B57;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
        }
        .subtitle {
            color: #556B2F;
            text-align: center;
            font-size: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.markdown("<p class='title'>Impact Analytica 🌱</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Extract, analyze, and generate insights from sustainability reports</p>", unsafe_allow_html=True)

# Upload PDF file
uploaded_file = st.file_uploader("Upload a sustainability report (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        extracted_text = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)

        full_text = "\n\n".join(extracted_text)
        st.success("Text extracted successfully!")

    # OpenAI API Key from environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    
    # GPT Analysis
    if st.button("Analyze Report"):
        with st.spinner("Analyzing report with AI..."):
            prompt = f"""
            I have extracted text from a sustainability report. Please:
            1. Provide a concise **summary** of the document.
            2. Highlight key **insights** related to sustainability efforts.
            3. Suggest **recommendations** for future improvements.

            Here is the extracted text:
            {full_text[:4000]}  # Limiting input to 4000 characters
            """
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in sustainability analysis."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = response["choices"][0]["message"]["content"]
            
            # Display Analysis
            st.subheader("📄 Report Summary")
            st.write(analysis)
            
            # Save to file
            st.download_button(
                label="Download Analysis",
                data=analysis,
                file_name="sustainability_analysis.txt",
                mime="text/plain"
            )


