CREATE DATABASE IF NOT EXISTS job_scraper;

\c job_scraper;

CREATE TABLE IF NOT EXISTS job_listings (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    salary_estimate VARCHAR(255),
    job_description TEXT,
    rating DECIMAL(3, 2),
    company_name VARCHAR(255),
    location VARCHAR(255),
    UNIQUE (job_title, company_name, location)  -- Prevent duplicate job entries
);
