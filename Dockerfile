FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install Flask==3.0.2 && pip install pymysql==1.1.0

CMD ["python", "app.py"]