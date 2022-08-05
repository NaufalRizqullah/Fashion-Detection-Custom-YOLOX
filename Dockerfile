FROM python:3.8.10

RUN mkdir -p /home/app_fastapi

COPY . /home/app_fastapi

RUN pip install \
    -r \
    /home/app_fastapi/services/requirements.txt

CMD [ "uvicorn", "home.app_fastapi.services.main:app"]