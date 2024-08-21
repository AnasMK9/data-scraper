# Data Scraper

This project is a web application designed to scrape job listings from Glassdoor using Django and Celery, all orchestrated with Docker. The scraped jobs are stored in a PostgreSQL database, and the application allows users to search for jobs based on keywords.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Setting Up Environment Variables](#setting-up-environment-variables)
- [Running the Project](#running-the-project)
- [Creating a Django Admin User](#creating-a-django-admin-user)
- [Using Celery for Background Tasks](#using-celery-for-background-tasks)
- [Contributing](#contributing)
- [License](#license)

## Features
- Scrape job listings from Glassdoor based on keywords.
- Store job data in a PostgreSQL database.
- Run background scraping tasks with Celery.
- Fully Dockerized for easy setup and deployment.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.
- Git installed on your machine.

### Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/AnasMK9/data-scraper.git
    cd data-scraper
    ```

2. **Set up environment variables:**
   - Copy the example environment file and modify it with your own configuration.
    ```bash
    cp scraperwebapp/.env.example scraperwebapp/.env
    ```
   - Update the `.env` file with your PostgreSQL credentials, Django secret key, etc.

## Running the Project

1. **Build and start the services:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images and start the services, including Django, Celery, Redis, and PostgreSQL.

2. **Run database migrations:**
    ```bash
    docker-compose exec scraperwebapp python manage.py migrate
    ```

3. **Access the application:**
   - The web application will be available at [http://localhost:8000](http://localhost:8000).
   - The Django admin interface can be accessed at [http://localhost:8000/admin](http://localhost:8000/admin).

## Creating a Django Admin User

To manage the application, you need to create a Django admin user. Run the following command:

```bash
docker-compose exec -it scraperwebapp python manage.py createsuperuser
```

## Using Celery for Background Tasks
Celery is used to run background scraping tasks. It is configured and automatically started with Docker Compose.

## Running a Task
Tasks are automatically queued when new keywords are added. The Celery worker will pick up the tasks and execute them.

## Setting Up Environment Variables
The application requires several environment variables to be set up. You can find .env.example files in each directory.
```
DATABASE_URL: The connection string for the PostgreSQL database.
SECRET_KEY: The secret key for Django.
ALLOWED_HOSTS: A comma-separated list of hosts/IPs allowed to connect to the application.
```
