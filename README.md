# Teacher Portal - Students

This is a Flask-based web application for managing student records with CRUD operations and search functionality.

1. Clone the repository:
##bash
git clone https://github.com/Yogesh2580123/teacher-portal-students.git
cd teacher-portal-students

virtualenv venv
venv\scripts\activate



pip install -r requirements.txt


## How to Run Locally
py run.py

## 📁 Project Structure
teacher-portal-students/
│
├── app/ # Main Flask app package
│ ├── static/ # All static files (CSS, JS)
│ │ ├── css/
│ │ │ └── main.css
│ │ └── javascript/
│ │ └── main.js
│ ├── templates/ # HTML templates (Jinja2)
│ │ ├── index.html
│ │ └── navbar.html
│ ├── init.py # Flask app factory
│ └── routes.py # All Flask routes
│
├── run.py # Entry point to start the Flask app
├── requirements.txt # Python dependencies
└── README.md # Project documentation