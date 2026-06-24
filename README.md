EyeVault — Hospital Management System

🧭 Overview



EyeVault is a Flask-based hospital management system designed to digitize and streamline core hospital workflows such as patient registration, doctor management, appointment scheduling, and token generation.



The system focuses on data consistency, workflow automation, and scalable backend design using Python and SQLAlchemy ORM.



🎯 Problem Statement



Traditional hospital systems rely heavily on manual processes for:



Patient registration

Appointment booking

Queue / token management



This leads to:



Inefficient workflows

Duplicate patient records

Poor queue tracking

✔ Solution



EyeVault introduces a structured backend system that automates hospital operations and ensures data consistency.



⚙️ System Architecture

Frontend (HTML / Jinja2)

&#x20;       ↓

Flask Web Server (Routes / Controllers)

&#x20;       ↓

Business Logic Layer (Python)

&#x20;       ↓

SQLAlchemy ORM

&#x20;       ↓

Database (SQLite / MySQL)

🚀 Key Features

👤 Patient Management

Create patient records

Prevent duplicate entries using phone number validation

👨‍⚕️ Doctor Management

Maintain doctor profiles

Dynamic retrieval of doctor data

📅 Appointment System

Book appointments with doctor and time slot

Maintain structured appointment records

🎟️ Token System

Auto-increment token generation

Maintain patient queue order

Track visit source

🧠 Core Design Principles

ORM-based architecture using SQLAlchemy

Normalized relational database schema

Separation of concerns (routes, models, logic)

Stateless request handling using Flask

Scalable backend structure

🗄️ Database Schema

Patient

id (Primary Key)

name

dob

gender

phone (unique)

Doctor

id (Primary Key)

name

specialization

Appointment

id (Primary Key)

patient\_id (Foreign Key)

doctor\_id (Foreign Key)

appointment\_date

appointment\_time

status

Token

id (Primary Key)

patient\_id (Foreign Key)

token\_number

visit\_date

status

source

🛠️ Tech Stack

Python 3.x

Flask

SQLAlchemy ORM

HTML / Jinja2 Templates

SQLite / MySQL

📦 Installation

1\. Clone repository

git clone https://github.com/Rizwana200/EyeVault.git

cd EyeVault

2\. Create virtual environment

python -m venv venv

venv\\Scripts\\activate

3\. Install dependencies

pip install -r requirements.txt

4\. Run application

python app.py



Open in browser:



http://127.0.0.1:5000/

📊 What This Project Demonstrates

Backend development using Flask

REST-style route design

Database modeling using ORM

CRUD operations across entities

Queue/token system logic

Real-world workflow automation

🔮 Future Enhancements

Role-based authentication (Admin / Doctor / Receptionist)

REST API layer for mobile integration

Appointment conflict resolution system

Dashboard analytics (patient flow, doctor workload)

Frontend upgrade using React / Bootstrap

