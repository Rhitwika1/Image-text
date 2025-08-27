# Image to text


A simple Streamlit web application that extracts text from an image using **Google Gemini API** and can also generate custom text (stories, blogs, etc.) based on the uploaded image and a user-provided query.

##  Features

- Upload an image (`.jpg`, `.jpeg`, `.png`)  
- Extract textual details from the image using Gemini  
- Generate custom text based on an image + query  
- Download results as a CSV file if wanted

##  Requirements

- Python 3.8+  
- Dependencies listed in `requirements.txt`
- make an env

##  Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Rhitwika1/ImagetoText.git
   cd ImagetoText

##  Create and activate a virtual environment

python -m venv venv

venv\Scripts\activate    # On Windows



## API Key Setup

set GOOGLE_API_KEY="your_api_key_here"    # Windows (CMD)
After writing this in powershell you can close the vs code and open it again so that it becomes activated and doesn't cause ny problem.


## Run the streamlit app
streamlit run app.py



