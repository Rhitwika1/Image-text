import streamlit as st
import pandas as pd
import PIL.Image
import google.generativeai as genai

# Configure API key from Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Create a model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Functions
def image_to_text(uploaded_file):
    uploaded_file.seek(0)  # reset pointer
    file = genai.upload_file(uploaded_file, mime_type=uploaded_file.type)
    response = model.generate_content([file])
    return response.text

def image_and_query(uploaded_file, query):
    uploaded_file.seek(0)
    file = genai.upload_file(uploaded_file, mime_type=uploaded_file.type)
    response = model.generate_content([query, file])
    return response.text

# Streamlit app
st.title("Image to Text Extractor & Generator")
st.write("Upload an image and get details about it.")

upload_image = st.file_uploader("Upload an Image", type=['png','jpg','jpeg'])
query = st.text_input("Write a story or blog for this image")

if st.button("Generate"):
    if upload_image and query:
        # Display image
        img = PIL.Image.open(upload_image)
        st.image(img, caption='Uploaded Image', width=300)

        # Extract details
        extracted_details = image_to_text(upload_image)
        st.subheader("Extracted Details")
        st.write(extracted_details)

        # Generate details
        generated_details = image_and_query(upload_image, query)
        st.subheader("Generated Details")
        st.write(generated_details)

        # Save to CSV
        data = {"Extracted details": [extracted_details],
                "Generated Details": [generated_details]}
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)

        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="details.csv",
            mime="text/csv"
        )
