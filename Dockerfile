FROM python:3.11-alpine

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=80
ENV DELAY=0.1

CMD ["python", "main.py"]
