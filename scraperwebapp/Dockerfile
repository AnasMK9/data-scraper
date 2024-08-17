
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    curl \
    gnupg \
    unzip \
    chromium-driver \
    chromium

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ENV CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER=/usr/bin/chromedriver

COPY . /app/


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "scraperwebapp.wsgi:application"]
