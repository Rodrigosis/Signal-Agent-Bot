FROM python:3.11-slim

# Evita arquivos .pyc e buffering estranho
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "src/application/bot_telegram.py"]
