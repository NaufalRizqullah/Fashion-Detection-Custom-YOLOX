# disini saya pull image python3.7 yang versi slim
FROM python:3.7-slim

# lalu saya membuat directory di home
RUN mkdir -p /home/app_streamlit

# setelah itu saya copy kan file di local/host saya kedalam folder /home/streamlit
COPY . /home/app_streamlit

# selanjutya setelah saya copy, saya install dependency yang diperlukan oleh streamlit yang berada didalam file requirements.txt
RUN pip install -r /home/app_streamlit/requirements.txt

# setelah semua package didownload, jalakan streamlitnya
CMD [ "streamlit", "run", "/home/app_streamlit/app.py" ]