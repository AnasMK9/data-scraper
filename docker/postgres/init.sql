-- Create Database
CREATE DATABASE job_scraper;

-- Switch to job_scraper database
\c job_scraper;

-- Create job_listings table
CREATE TABLE job_listings (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(255),
    company_name VARCHAR(255),
    location VARCHAR(255),
    date_posted DATE,
    job_description TEXT,
    salary_range VARCHAR(255),
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_title, company_name, location, date_posted)
);
