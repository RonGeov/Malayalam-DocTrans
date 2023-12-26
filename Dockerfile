FROM python:3

RUN apt-get update -y && \
    apt-get install tesseract-ocr-mal -y && \
    apt-get install poppler-utils -y

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]