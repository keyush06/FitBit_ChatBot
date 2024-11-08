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

## Step 1: Clone the Repository

Start by cloning the repository to your local machine.

```bash
git clone https://github.com/your-username/FitBit_ChatBot.git
cd FitBit_ChatBot
```

## Step 2: Install Project Dependencies

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


## Step 3: Configure Environment Variables
Create a .env file in the root directory of your project to store your environment variables, like API keys and database settings. 
#### My work is LLM agnostic, I also have LLMOpenAI function that can be called for OpenAI keys. As directed in the project, I have used Google's Gemini.

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key
MODEL_NAME=your_model_name

# You can also put the OpenAI keys
```

## Step 4: Set Up Django Configuration
Update the settings.py file if necessary to reflect your database and other settings.

If using environment variables for sensitive information, ensure settings.py loads them appropriately.

## Step 5:Migrate the Database
Apply the database migrations to set up your database schema:
```
bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Create a Superuser
To access Django's admin interface, create a superuser:
```
bash
python manage.py createsuperuser
```

Follow the prompts to create your admin user.

## Step 7: Load Initial Data (Optional)
If you have initial data to load (like test patients or sessions), you can create a Django fixture or manually add data via the Django admin.

## Step 8: Run the Django Development Server
Start the Django development server to test the setup:
bash
python manage.py runserver

Visit [http://127.0.0.1:8000/in](http://127.0.0.1:8000/) your browser.

### The overall User Interface is shown below: -

![image](https://github.com/user-attachments/assets/ce60f062-a3a2-45ef-a6f0-a52aba0df750)




