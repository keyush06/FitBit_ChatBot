  # Medical Chatbot with LLM Integration

A Django-based chatbot application designed to handle health-related inquiries using a language model. The chatbot interacts with patients by retrieving their medical data and providing responses based on predefined categories.

## Features
- Appointment rescheduling with doctor details.
- Medication reminders and regimen inquiries.
- Health and lifestyle advice.
- Retrieval of patient's medical information.
- Dynamic date handling for appointment changes.

## Requirements
- Python > 3.9 (Potentially 3.12)
- Django 4.x
- psycopg2
- Langchain and Langraph (for LLM orchestration)
- postgres

## Step 1: Install PostgreSQL
https://www.postgresql.org/

## Step 2: Set Up PostgreSQL
1. Access PostgreSQL
Open the PostgreSQL command-line interface (psql) or pgAdmin UI:
bash
psql -U postgres

You might need to enter the password you set during installation.

2. Create a New Database
Create a database for your Django project:
bash
CREATE DATABASE patient_db;

3. Create a Database User
Create a new user (role) for your project:
bash
CREATE USER chat_user WITH PASSWORD 'chatdb';

4. Grant Privileges
Grant the necessary privileges to the new user for the newly created database:
bash
GRANT ALL PRIVILEGES ON DATABASE chat_db TO chat_user;

5. Exit psql
Exit the PostgreSQL prompt by typing:
bash
\q

