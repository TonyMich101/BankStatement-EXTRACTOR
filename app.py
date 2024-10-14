import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import os 
import streamlit as st
from PIL import Image

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_gemini_response(input,image,prompt):
    response = model.generate_content([prompt,image[0],input])
    return response.text

st.set_page_config(page_title="BS Extractor")
st.header("BS Extractor")

input = st.text_input("Input Prompt : ",key="input")
uploaded_file = st.file_uploader("Choose a image of bs ", type=['jpg','png','jpeg'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit = st.button("Tell me about image?")

prompt = """
    You are an expert in understanding bankstatements.We will upload an image and bankstatement
    and you will have to answer any questions based on uploaded bankstatement.
"""

def get_image_bytes(uploaded_image):
    if uploaded_image is not None:
        # read the uploaded image in bytes
        image_bytes = uploaded_image.getvalue()

        image_info = [
            {
            "mime_type": uploaded_image.type,
            "data": image_bytes
        }
        ]
        return image_info
    else:
        raise FileNotFoundError("Upload Valid image file!")


if submit and input:
    image_data = get_image_bytes(uploaded_file)
    response = get_gemini_response(input,image_data,prompt)
    st.subheader("The response is ")
    st.write(response)
