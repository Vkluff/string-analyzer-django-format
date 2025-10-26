String Analyzer API - Django Implementation (Stage 1 - HNG)

A RESTful API built with Django and Django REST Framework that analyzes strings and stores their computed properties.

Features

Computes and stores:

•
length

•
palindrome check

•
unique character count

•
word count

•
SHA-256 hash

•
character frequency map

Additional features:

•
Retrieve and filter stored strings

•
Delete strings

•
Natural language query filtering

•
Built-in admin panel for data management

•
Browsable API interface

Setup

Clone the repository

Bash


git clone https://github.com/yourusername/string_analyzer_django.git
cd string_analyzer_django


Create and activate a virtual environment

Bash


python -m venv string_venv
source string_venv/bin/activate  # On Mac/Linux


Or on Windows:

Bash


python -m venv string_venv
source string_venv\Scripts\activate


Install dependencies

Bash


pip install -r requirements.txt


Initialize the database

Create migrations and apply them:

Bash


python manage.py makemigrations
python manage.py migrate


Create a superuser account for the admin panel:

Bash


python manage.py createsuperuser


Run the API server

Bash


python manage.py runserver


The API will be available at http://127.0.0.1:8000/api/strings/

The admin panel will be available at http://127.0.0.1:8000/admin/

API Endpoints

1. Create/Analyze String

POST /api/strings/

Request Body:

JSON


{
  "value": "string to analyze"
}


Success Response:

JSON


{
  "id": "<sha256_hash>",
  "value": "string to analyze",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "<sha256_hash>",
    "character_frequency_map": { "s": 2, "t": 3, ... }
  },
  "created_at": "2025-08-27T10:00:00Z"
}


2. Get Specific String

GET /api/strings/{string_value}/

Success Response:

JSON


{
  "id": "<sha256_hash>",
  "value": "requested string",
  "properties": { ... },
  "created_at": "2025-08-27T10:00:00Z"
}


3. Get All Strings with Filtering

GET /api/strings/

Query Parameters:

•
is_palindrome: boolean

•
min_length: integer

•
max_length: integer

•
word_count: integer

•
contains_character: string

Example:

Plain Text


GET /api/strings/?is_palindrome=true&min_length=5&contains_character=a


Success Response:

JSON


{
  "data": [ ... ],
  "count": 3,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "contains_character": "a"
  }
}


4. Natural Language Filtering

GET /api/strings/filter_by_natural_language/?query={query}

Example:

Plain Text


GET /api/strings/filter_by_natural_language/?query=all single word palindromic strings


Success Response:

JSON


{
  "data": [ ... ],
  "count": 2,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}


5. Delete String

DELETE /api/strings/{string_value}/

Success Response: Status code 204 No Content (empty body)

Error Handling

•
409 Conflict: String already exists

•
400 Bad Request: Invalid request or missing fields

•
404 Not Found: String does not exist

•
422 Unprocessable Entity: Invalid data type for "value"

Example Usage (with curl)

Create a string

Bash


curl -X POST "http://127.0.0.1:8000/api/strings/" \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'


Get all palindromic strings

Bash


curl "http://127.0.0.1:8000/api/strings/?is_palindrome=true"


Get strings with specific length

Bash


curl "http://127.0.0.1:8000/api/strings/?min_length=5&max_length=10"


Natural language filter

Bash


curl "http://127.0.0.1:8000/api/strings/filter_by_natural_language/?query=all%20single%20word%20palindromic%20strings"


Delete a string

Bash


curl -X DELETE "http://127.0.0.1:8000/api/strings/racecar/"


Dependencies

All dependencies are listed in requirements.txt:

Plain Text


Django==5.2.7
djangorestframework==3.14.0
python-dotenv==1.0.0
PyMySQL==1.1.0
gunicorn==21.2.0


Install all dependencies

Bash


pip install -r requirements.txt


Environment Variables

Create a .env file in the project root with the following variables:

Plain Text


# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration - SQLite (Default)
DATABASE_ENGINE=sqlite3
DATABASE_NAME=db.sqlite3

# Database Configuration - MySQL (Optional)
# DATABASE_ENGINE=mysql
# DATABASE_NAME=string_analyzer
# DATABASE_USER=root
# DATABASE_PASSWORD=password123
# DATABASE_HOST=localhost
# DATABASE_PORT=3306


Project Structure

Plain Text


string_analyzer_django/
├── string_analyzer/          # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
├── analyzer/                 # Main application
│   ├── models.py             # Database models
│   ├── views.py              # API views and ViewSets
│   ├── serializers.py        # JSON serializers
│   ├── utils.py              # String analysis utilities
│   ├── admin.py              # Admin configuration
│   ├── urls.py               # App URL routing
│   └── migrations/           # Database migrations
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3                # SQLite database (created on first run)
├── README.md                 # Full documentation
├── SETUP.md                  # Detailed setup guide
└── QUICKSTART.md             # Quick start guide


Running Tests

After starting the server, you can test the endpoints using:

Using the Browsable API

Visit http://127.0.0.1:8000/api/strings/ in your browser and use the form to create and test strings.

Using curl

See the "Example Usage (with curl)" section above.

Using Python requests

Python


import requests

# Create a string
response = requests.post(
    "http://127.0.0.1:8000/api/strings/",
    json={"value": "hello"}
)
print(response.json())

# Get all strings
response = requests.get("http://127.0.0.1:8000/api/strings/")
print(response.json())

# Filter strings
response = requests.get("http://127.0.0.1:8000/api/strings/?is_palindrome=true")
print(response.json())

# Delete a string
response = requests.delete("http://127.0.0.1:8000/api/strings/hello/")
print(response.status_code)


Admin Panel

Access the Django admin panel at http://127.0.0.1:8000/admin/ with your superuser credentials.

Features:

•
View all analyzed strings

•
Search and filter strings

•
Edit string properties

•
Delete strings

•
Manage user accounts

Troubleshooting

Port 8000 already in use

Bash


python manage.py runserver 8001


Database errors

Bash


python manage.py migrate


Module not found errors

Bash


pip install -r requirements.txt


Superuser creation issues

Bash


python manage.py createsuperuser


Additional Resources

•
Django Documentation

•
Django REST Framework
