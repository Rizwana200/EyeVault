\# 🏥 EyeVault — Hospital Management System



!\[Python](https://img.shields.io/badge/Python-3.x-blue)

!\[Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)

!\[SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-orange)



\---



\## 🧭 Overview



EyeVault is a Flask-based hospital management system that digitizes hospital workflows such as:



\- Patient registration  

\- Doctor management  

\- Appointment booking  

\- Token generation  



It is designed using \*\*Flask + SQLAlchemy ORM\*\* with a focus on clean backend architecture.



\---



\## 🎯 Problem Statement



Traditional hospital systems suffer from:



\- Manual record management  

\- Duplicate patient entries  

\- Poor queue handling  



\---



\## ✔ Solution



EyeVault provides a structured system to:



\- Automate patient workflow  

\- Maintain unique patient records  

\- Manage appointment scheduling  

\- Generate queue tokens efficiently  



\---



\## ⚙️ System Architecture



Frontend → Flask Server → Business Logic → SQLAlchemy ORM → Database



\---



\## 🚀 Features



\### 👤 Patient Management

\- Register patients  

\- Prevent duplicate entries using phone number  



\### 👨‍⚕️ Doctor Management

\- Add and manage doctors  

\- Fetch doctor data dynamically  



\### 📅 Appointment System

\- Book appointments  

\- Store structured scheduling data  



\### 🎟️ Token System

\- Auto-generated tokens  

\- Maintains queue order  



\---



\## 🧠 Design Principles



\- ORM-based architecture  

\- Modular Flask design  

\- Separation of concerns  

\- Scalable backend structure  



\---



\## 🗄️ Database Schema



\*\*Patient\*\*

\- id, name, dob, gender, phone



\*\*Doctor\*\*

\- id, name, specialization



\*\*Appointment\*\*

\- id, patient\_id, doctor\_id, date, time, status



\*\*Token\*\*

\- id, patient\_id, token\_number, visit\_date, status



\---



\## 🛠️ Tech Stack



\- Python  

\- Flask  

\- SQLAlchemy  

\- HTML / Jinja2  

\- SQLite  



\---



\## 📦 Setup Instructions



```bash

git clone https://github.com/Rizwana200/EyeVault.git

cd EyeVault



python -m venv venv

venv\\Scripts\\activate



pip install -r requirements.txt



python app.py

