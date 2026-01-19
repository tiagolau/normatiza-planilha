FROM python:3.9-slim

WORKDIR /app

# Ensure logs are flushed immediately to the console
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use port 8000 (standard for web apps)
EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
