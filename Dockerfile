FROM python:3.8.10

RUN mkdir -p /home/app_fastapi

COPY . /home/app_fastapi

WORKDIR /home/app_fastapi

RUN pip install \
    -r \
    services/requirements.txt

CMD [ "uvicorn", "services.main:app", "--host", "0.0.0.0", "--port", "8000"]