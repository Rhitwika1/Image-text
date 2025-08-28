# ------------------ Importing required libraries ------------------
import streamlit as st              # Streamlit → to build the web app
import pandas as pd                 # Pandas → to create/save CSV files
import PIL.Image                    # PIL (Python Imaging Library) → to handle/display images
import google.generativeai as genai # Google Gemini API → for AI model

# ------------------ Configure API Key ------------------
# st.secrets is used to safely store API keys in Streamlit Cloud
# "GOOGLE_API_KEY" must be added in your .streamlit/secrets.toml file
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ------------------ Load the Gemini AI Model ------------------
# We are using Google's "gemini-1.5-flash" model (fast & efficient)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Function: Convert image to text ------------------
def image_to_text(uploaded_file):
    uploaded_file.seek(0)  # Reset file pointer to the start (important when reading files multiple times)
    file = genai.upload_file(uploaded_file, mime_type=uploaded_file.type)  # Upload file to Gemini API
    response = model.generate_content([file])  # Ask Gemini to analyze image
    return response.text  # Return AI's response (text description)

# ------------------ Function: Image + Query together ------------------
def image_and_query(uploaded_file, query):
    uploaded_file.seek(0)  # Reset pointer again
    file = genai.upload_file(uploaded_file, mime_type=uploaded_file.type)  # Upload image
    response = model.generate_content([query, file])  # Pass BOTH query + image to Gemini
    return response.text  # Return generated text (e.g., story, blog, description)

# ------------------ Streamlit App UI ------------------
st.title("Image to Text Extractor & Generator")  # App title
st.write("Upload an image and let AI extract details or create a story/blog about it.")  # Short description

# File uploader (only accepts image formats png, jpg, jpeg)
upload_image = st.file_uploader("Upload an Image", type=['png','jpg','jpeg'])

# Text input for user query (e.g., "Write a funny story about this picture")
query = st.text_input("Write a story or blog for this image")

# ------------------ Button Action ------------------
if st.button("Generate"):  # When user clicks "Generate"
    if upload_image and query:  # Run only if both image & query are provided

        # ---- Display uploaded image in app ----
        img = PIL.Image.open(upload_image)
        st.image(img, caption='Uploaded Image', width=300)

        # ---- Extract image details (AI-generated description) ----
        extracted_details = image_to_text(upload_image)
        st.subheader("Extracted Details")
        st.write(extracted_details)

        # ---- Generate creative details (story/blog) ----
        generated_details = image_and_query(upload_image, query)
        st.subheader("Generated Details")
        st.write(generated_details)

        # ---- Save results in a CSV file ----
        data = {"Extracted details": [extracted_details],  # Dictionary with results
                "Generated Details": [generated_details]}
        df = pd.DataFrame(data)       # Convert dictionary → DataFrame
        csv = df.to_csv(index=False)  # Convert DataFrame → CSV string

        # ---- Download button for CSV ----
        st.download_button(
            label="Download as CSV",  # Button label
            data=csv,                    # The CSV file data
            file_name="details.csv",     # Downloaded file name
            mime="text/csv"              # File type
        )
