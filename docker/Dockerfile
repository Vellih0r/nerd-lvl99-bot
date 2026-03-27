FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY bot/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "-u", "bot/main.py" ]