-- init.sql

-- Create the database if it does not exist
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'job_scraper') THEN
        CREATE DATABASE job_scraper;
    END IF;
END
$$;

-- Connect to the newly created or existing database
\c job_scraper

-- Create the table if it does not exist
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
