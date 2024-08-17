FROM python:3.11-slim

# Environment variables to prevent bytecode generation and to keep stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies, including Chromium and ChromeDriver
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    curl \
    gnupg \
    unzip \
    chromium-driver \
    chromium

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Set Chrome environment variables for the application
ENV CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER=/usr/bin/chromedriver

# Copy the entire project to the working directory
COPY . /app/

# Expose port 8000 for the application
EXPOSE 8000

# Run migrations and then start the application using Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 scraperwebapp.wsgi:application"]
