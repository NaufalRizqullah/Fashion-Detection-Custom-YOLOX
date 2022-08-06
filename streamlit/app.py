from PIL import Image
from io import BytesIO
import numpy as np
import io
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


import streamlit as st


# interact with FastAPI endpoint
backend = "http://host.docker.internal:8000/v1/detect/streamlit/demo"

# function to connect backend
def postToBackend(image, server_url: str):
    # Perhatikan field "im", dia harus sesuai sm field yg dibutuhkan sama backend
    m = MultipartEncoder(fields={"im": ("filename", image, "image/jpeg")})

    return requests.post(server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000)

# sourcery skip: use-named-expression
seeResult = False

st.title("A simple Fashion Object Detection")
st.caption("By **_Skylar White_**")
st.markdown("***")

# Sidebar
st.sidebar.header("This is nothing and just a simple project, so yeah. have fun 😀")
st.sidebar.write("- Visit My Github [NaufalRizqullah](https://github.com/NaufalRizqullah)")

# Main Content
col1, col2 = st.columns(2)

with st.form("my_form"):
    uploaded_file = st.file_uploader("Masukan File Gambar yang ingin Dideteksi", ["png", "jpg", "jpeg"])
    if uploaded_file is not None:

        # To read file as bytes and convert to np.array
        bytes_data = uploaded_file.getvalue()
        image = Image.open(BytesIO(uploaded_file.getvalue()))
        imageList = np.array(image)

        # Show Image after load
        # st.markdown('**_Input_**')
        # st.image(imageList, caption="Input Image", width=500)
    
    send = st.form_submit_button('Try Detect Fashion!')
    if send:
        if uploaded_file:
            st.markdown('**_Result_**')

            with st.spinner('Wait for it...'):
                # Send to Backend
                bytes_data = uploaded_file.getvalue()
                fashionDetect = postToBackend(bytes_data, backend)

                # take result
                imageRes = Image.open(io.BytesIO(fashionDetect.content))

                # st.image(imageRes, caption="Result Image", width=500)
            st.success('Selesai!')
            seeResult = True
        else:
            st.warning('Image not Found! Please Insert Image')

# Show Result in new section
if seeResult:
    col1.header("Original")
    col1.image(imageList, use_column_width=True)
    col2.header("Detected")
    col2.image(imageRes, use_column_width=True)