from PIL import Image
from io import BytesIO
import numpy as np
import time

import streamlit as st


st.title("A simple Fashion Object Detection")
st.caption("By **_Skylar White_**")
st.markdown("***")

# Sidebar
st.sidebar.header("This is nothing and just a simple project, so yeah. have fun 😀")
st.sidebar.write("- Visit My Github [NaufalRizqullah](https://github.com/NaufalRizqullah)")

# Main Content
with st.form("my_form"):
    uploaded_file = st.file_uploader("Masukan File Gambar yang ingin Dideteksi", ["png", "jpg", "jpeg"])
    if uploaded_file is not None:

        # To read file as bytes and convert to np.array
        bytes_data = uploaded_file.getvalue()
        image = Image.open(BytesIO(uploaded_file.getvalue()))
        imageList = np.array(image)

        # Show Image after load
        st.markdown('**_Input_**')
        st.image(imageList, caption="Input Image", width=500)

    if send := st.form_submit_button('Try Detect Fashion!'):
        if uploaded_file:
            st.markdown('**_Result_**')

            with st.spinner('Wait for it...'):
                time.sleep(5)
                # Send to FastAPI endpoint ( but can't :'( [not now])
                st.write('Detection Send!')
                # Show Result
                st.image(imageList, caption="Result Image", width=500)
            st.success('Done!')
        else:
            st.warning('Image not Found! Please Insert Image')