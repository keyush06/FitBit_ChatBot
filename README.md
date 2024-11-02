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
#### Open the PostgreSQL command-line interface (psql):
```bash
psql -U postgres
```
You might need to enter the password you set during installation.

2. Create a New Database
#### Create a database for your Django project:
```bash
CREATE DATABASE chat_db;
```
3. Create a Database User
#### Create a new user (role) for your project:
```bash
CREATE USER chat_user WITH PASSWORD 'chatdb';
```
4. Grant Privileges
#### Grant the necessary privileges to the new user for the newly created database:
```bash
GRANT ALL PRIVILEGES ON DATABASE chat_db TO chat_user;
```
5. Exit psql
Exit the PostgreSQL prompt by typing:
```bash
\q
```

## Step 3: Install Project Dependencies

### 1. Create a Virtual Environment
It is recommended to use a virtual environment to manage your project’s dependencies.

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Once your virtual environment is activated, install the project dependencies using the requirements.txt file:
bash
pip install -r requirements.txt

This command will install all the packages listed in the requirements.txt file into your virtual environment.

## Step 4: Run Migrations
Apply the database migrations to set up your database schema:
bash
python manage.py migrate

## Step 5: Create a Superuser
Create a superuser account to access the Django admin interface:
bash
python manage.py createsuperuser

Follow the prompts to create your admin user.

## Step 6: Run the Django Development Server
Start the Django development server to test the setup:
bash
python manage.py runserver

Visit http://127.0.0.1:8000/aichat/home in your browser. Log in to the admin interface using the superuser credentials at http://127.0.0.1:8000/admin/.



