FROM python:3.11-slim

WORKDIR /myfile

COPY . .

RUN pip install Flask==3.0.2 && pip install pymysql==1.1.0 && pip install cryptography

CMD ["python", "app.py"]