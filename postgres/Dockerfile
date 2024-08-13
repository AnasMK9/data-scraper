# Use the official PostgreSQL image as the base
FROM postgres:15.3

# Set the environment variables for database credentials
ENV POSTGRES_USER=scraper_user
ENV POSTGRES_PASSWORD=scraper_pass
ENV POSTGRES_DB=job_scraper

# Copy the initialization SQL script into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default PostgreSQL port
EXPOSE 5432

# docker build -t postgres_job_scraper_image .
# docker run -d --name postgres_job_scraper_container -p 5432:5432 postgres_job_scraper_image 
