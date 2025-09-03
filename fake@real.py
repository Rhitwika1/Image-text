# ------------------ Importing required libraries ------------------
import os
import streamlit as st
import pandas as pd
import PIL.Image
import google.generativeai as genai
import docx
import fitz  # PyMuPDF → for PDFs

# ------------------ Configure API Key ------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyAYpe46XHYgCJMjrAxXh4St1L8R-3n7KAU"  # replace with your real API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ------------------ Load the Gemini AI Model ------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ File Processing Functions ------------------
def extract_text_from_image(uploaded_file):
    uploaded_file.seek(0)
    file = genai.upload_file(uploaded_file, mime_type=uploaded_file.type)
    response = model.generate_content([file])
    return response.text

def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

def extract_text_from_excel(uploaded_file):
    uploaded_file.seek(0)
    df = pd.read_excel(uploaded_file)
    return df.to_string(index=False)

def extract_text_from_docx(uploaded_file):
    uploaded_file.seek(0)
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

# ------------------ Document Nature Checker ------------------
def check_document_nature(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["invoice", "amount due", "payment", "receipt"]):
        return "Invoice / Financial Document"
    elif any(word in text_lower for word in ["curriculum vitae", "resume", "experience", "skills", "education"]):
        return "Resume / CV"
    elif any(word in text_lower for word in ["research", "methodology", "references", "abstract", "study"]):
        return "Research Paper / Academic Document"
    elif any(word in text_lower for word in ["story", "once upon", "narrative", "characters"]):
        return "Story / Narrative"
    elif any(word in text_lower for word in ["blog", "post", "article", "tips", "guide"]):
        return "Blog / Article"
    elif any(word in text_lower for word in ["report", "summary", "analysis", "findings"]):
        return "Report / Business Document"
    else:
        return "General Document"

# ------------------ Document Authenticity Checker ------------------
def check_document_authenticity(text):
    text_lower = text.lower()

    suspicious_keywords = [
        "lottery", "winner", "urgent payment", "claim prize",
        "nigerian prince", "click here", "100% guaranteed",
        "limited time offer", "congratulations you won", "bank transfer","company-logo","generated"
    ]

    real_keywords = [
        "invoice number", "tax id", "academic references", 
        "official seal", "company registration", "signature", 
        "terms and conditions", "research methodology","certificate","Google"
        "invoice", "amount due", "payment", "receipt",
        "curriculum vitae", "resume", "experience", "skills", "education",
        "This is to certify that"
    ]

    if any(word in text_lower for word in suspicious_keywords):
        return "Potentially Fake / Scam-like Document"
    elif any(word in text_lower for word in real_keywords):
        return "Likely Real Document"
    else:
        return "Unclear Authenticity (Needs manual review)"

# ------------------ Main Function: Handle file + query ------------------

def process_file(uploaded_file, query):
    file_type = uploaded_file.type

    if "image" in file_type:  # Image files
        extracted_text = extract_text_from_image(uploaded_file)
    elif "pdf" in file_type:  # PDF
        extracted_text = extract_text_from_pdf(uploaded_file)
    elif "spreadsheet" in file_type or uploaded_file.name.endswith(".xlsx"):  # Excel
        extracted_text = extract_text_from_excel(uploaded_file)
    elif "word" in file_type or uploaded_file.name.endswith(".docx"):  # DOCX
        extracted_text = extract_text_from_docx(uploaded_file)
    else:
        extracted_text = "Unsupported file format."

    # Ask Gemini with both extracted text + user query
    response = model.generate_content([query, extracted_text])
    return extracted_text, response.text

# ------------------ Streamlit App UI ------------------
st.title("File to Text Extractor & Analyzer")
st.write("Upload an Image, PDF, Excel, or Word file and let AI extract, analyze, and generate content.")

# Accept multiple file types
upload_file = st.file_uploader(
    "Upload a File", 
    type=['png','jpg','jpeg','pdf','xlsx','docx']
)

query = st.text_input("Enter a query (e.g., 'Write a story/blog about this document')")

if st.button("Generate"):
    if upload_file and query:
        # ---- Display uploaded image if it's an image ----
        if "image" in upload_file.type:
            img = PIL.Image.open(upload_file)
            st.image(img, caption='Uploaded Image', width=300)

        # ---- Extract and generate ----
        extracted, generated = process_file(upload_file, query)

        st.subheader("Extracted Content")
        st.write(extracted[:2000])  # show first 2000 chars

        st.subheader("Generated Content")
        st.write(generated)

        # ---- Nature Detection ----
        st.subheader("Detected Nature of Document")
        nature = check_document_nature(generated)
        st.write(nature)

        # ---- Authenticity Check ----
        st.subheader("Document Authenticity Check")
        authenticity = check_document_authenticity(generated)
        st.write(authenticity)

        # ---- Save results ----
        data = {
            "Extracted details": [extracted],
            "Generated Details": [generated],
            "Detected Nature": [nature],
            "Authenticity": [authenticity]
        }
        
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)

        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="document_analysis.csv",
            mime="text/csv"
        )

        