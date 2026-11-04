# 👁️ EyeVault

> **Your care, our vision.**

A Flask-based management system for a small eye clinic. It replaces paper registers and spreadsheets for patient records, daily queue tokens, visit history, reports, and billing.


---

## The problem

Small clinics often track patients, queue numbers, and payments by hand. That leads to lost reports, patients waiting without knowing their position, and bills where nobody is sure what is still unpaid.

EyeVault gives clinic staff one place to register patients, issue and track daily tokens, record visits, store reports, and manage bills. Patients get a dashboard showing their own token status, history, reports, and bills.

**Why I built it:** I wanted to take a real-world workflow, the daily running of a small clinic, and build it end to end myself, from database design to a Dockerized deployment.

**My contribution:** Solo project. I did the design, database schema, backend, templates, and Docker setup
---

## 📑 Table of Contents

1. At a Glance
2. Features
3. Tech Stack
4. Project Structure
5. Application Workflow
6. Database Design
7. Token Queue
8. Billing
9. Screenshots
10. Installation & Running Locally
11. Future Improvements
12. Key Learnings
13. AI-Assisted Development
14. Developer

---

## 📊 At a Glance

| Measure | Value |
|---|---|
| User roles | 2 (Patient, Staff) |
| Database tables | 9 |
| Tables linked to a patient by foreign key | 4 (Visit, Report, Token, Billing) |
| Application routes | 28 |
| Daily token limit | 5 by default, configurable by staff |
| Tokens per patient per day | 1 |
| Token statuses | 3 (Waiting, In Progress, Completed) |
| Token numbering | Starts at 1 each day, increases by 1 |
| Bill fields tracked | 4 amounts in, 3 computed (total, paid, due) plus status |
| Export formats | 2 (Excel for tokens, PDF for visit history) |
| Screenshots in this README | 9 |

---

## ✨ Features

### 👤 Patient Features
- Patient Registration & Login (using phone number)
- Patient Dashboard
- View Personal Details
- Generate a Token for Today
- View Live Token Status, including the current token being served and completed count
- View Visit History
- View Uploaded Reports
- View Billing History

### 👩‍💼 Staff Features
- Staff Registration & Login
- Staff Dashboard
- Search Patient by Phone
- View Registered Patients and Patient Details
- Add Visit Details (date, doctor, diagnosis, notes)
- Upload and View Patient Reports
- Manual Token Generation (walk-ins and phone requests)
- Token Dashboard (Waiting / In Progress / Completed)
- Set Daily Token Limit
- Add and Manage Doctors
- Add and Manage Spectacles
- Add, Edit, and View Bills
- Export Tokens to Excel
- Download Patient Visit History as PDF

---

## 🛠️ Tech Stack

**Backend**
- Python
- Flask
- Flask-SQLAlchemy (ORM)
- ReportLab (PDF export)
- OpenPyXL (Excel export)

**Frontend**
- Jinja2 templates
- Bootstrap 5
- HTML, CSS

**Database**
- SQLite

**DevOps**
- Docker

---

## 📂 Project Structure

```
EyeVault
│
├── app.py                  # models, routes, business logic
├── templates/              # Jinja2 pages (patient, staff, token, billing)
├── static/                 # CSS and uploaded reports
├── instance/               # SQLite database
├── screenshots_eyevault/   # README screenshots
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔄 Application Workflow

```
                          👁️ EyeVault
                               │
               ┌───────────────┴───────────────┐
               │                               │
               ▼                               ▼
          👤 Patient                       👩‍💼 Staff
               │                               │
               ▼                               ▼
        Register / Login                 Staff Login
               │                               │
               ▼                               ▼
       Patient Dashboard                Staff Dashboard
               │                               │
      ┌────────┼────────┐        ┌─────────────┼──────────────┐
      │        │        │        │             │              │
      ▼        ▼        ▼        ▼             ▼              ▼
   Generate  Visits   Reports  Search       Token          Billing
    Token    & Bills            Patient    Dashboard      & Spectacles
      │        │        │        │             │              │
      └────────┴────────┴────────┴─────────────┴──────────────┘
                               │
                               ▼
                       🗄️ SQLite Database
```

---

## 🗄️ Database Design

9 tables. `Patient` is the central table, and 4 others (Visit, Report, Token, Billing) link to it through `patient_id`.

```
Patient 1 ──< Visit
Patient 1 ──< Report
Patient 1 ──< Token
Patient 1 ──< Billing
```

| Model | Key fields | Notes |
|---|---|---|
| **Patient** | name, dob, gender, phone (unique) | Registered patients. Phone is unique and is used for login and search. |
| **Staff** | name, phone (unique), password | Clinic staff accounts. |
| **Visit** | patient_id, visit_date, doctor_name, diagnosis, notes | Belongs to a Patient. Feeds the visit history and the PDF export. |
| **Report** | patient_id, file_name, upload_date | Belongs to a Patient. Files are saved on the server and the file name is stored in the database. |
| **Token** | patient_id, token_number, visit_date, status, source | Belongs to a Patient. See Token Queue. |
| **Settings** | max_tokens_per_day (default 5) | Clinic-wide daily token limit. |
| **Billing** | patient_id, bill_date, consultation_fee, medicine_fee, spect_name, spect_cost, total_amount, paid_amount, due_amount, payment_status | Belongs to a Patient. Status is Due or Completed. |
| **Doctor** | name, specialization, available_time | Doctors list managed by staff. |
| **Spect** | name, price | Spectacles catalogue managed by staff. |

---

## 🎟️ Token Queue

EyeVault uses a token-based queue rather than time-slot appointments.

- **Daily limit:** 5 tokens per day by default, stored in `Settings.max_tokens_per_day`. Staff can change it from the token settings page.
- **Numbering:** each token has a `token_number` and a `visit_date`. Numbers start at 1 each day and increase by 1.
- **One token per patient per day.** A second request shows the patient's existing token number.
- **Limit reached:** once the day's count equals the limit, the patient dashboard shows token generation as closed, and staff manual tokens are also blocked.
- **Status flow:** Waiting → In Progress → Completed.
- **Two sources:** the patient generates a token from their dashboard, or staff create one manually for a walk-in or phone request.
- **Token dashboard:** shows 4 live counters (total, waiting, in progress, completed) for today, and tokens can be exported to Excel.

---

## 💳 Billing

- Total = consultation fee + medicine fee + spectacles cost.
- Due = total − paid amount, never below zero.
- Status is **Completed** when nothing is due, otherwise **Due**.
- Bills can be edited later so partial payments can be settled.
- Billing history is visible to both staff and the patient.

**Example:** consultation 300 + medicine 200 + spectacles 1500 gives a total of 2000. If 1000 is paid, due is 1000 and status is Due. After a later edit to paid 2000, due is 0 and status becomes Completed.

---

## 📸 Screenshots & UI Previews

### 🏠 Home Page
![Home Page](screenshots_eyevault/home-page.png)

---

### 📝 Patient Registration
![Patient Registration](screenshots_eyevault/patient-registration.png)

---

### 👤 Patient Directory
![Patient Directory](screenshots_eyevault/patient-directory.png)

---

### 👩‍💼 Staff Dashboard
![Staff Dashboard](screenshots_eyevault/staff-dashboard.png)

---

### 🔎 Patient Details
![Patient Details](screenshots_eyevault/patient-details.png)

---

### 🎟️ Token Dashboard
![Token Dashboard](screenshots_eyevault/token-dashboard.png)

---

### 👨‍⚕️ Doctors List
![Doctors List](screenshots_eyevault/doctors_list.png)

---

### 💳 Add Bill
![Add Bill](screenshots_eyevault/addbill.png)

---

### 🧾 Bill History
![Bill History](screenshots_eyevault/bill_history.png)

---

## ⚙️ Installation & Running Locally

### 📋 Prerequisites
- Python 3.9+
- pip
- Git
- Docker (optional)

### 📥 Clone the Repository

```bash
git clone https://github.com/Rizwana200/EyeVault.git
cd EyeVault
```

### 🐍 Create and Activate a Virtual Environment

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**Mac / Linux**
```bash
source venv/bin/activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Run the Project

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser. The database is created automatically on first run. Create a staff account at `/staff-register`.

### 🐳 Run with Docker

```bash
docker build -t eyevault .
docker run -p 5000:5000 eyevault
```

Then open http://127.0.0.1:5000/

---

## 🚀 Future Improvements

- Concurrency-safe token numbering using database unique constraints and retry on conflict
- Session-based staff authentication with route protection
- Password hashing for staff accounts
- OTP or password login for patients
- Secure report storage with random file names and an authenticated download route
- Server-side validation for billing amounts
- Automated tests with pytest (token limits, billing calculation, access control) and CI with GitHub Actions
- Migration to PostgreSQL for multi-clinic use
- SMS notifications for token status

---

## 💡 Key Learnings

- Building a server-rendered web application with Flask and Jinja2
- Relational modeling in SQLite with 9 SQLAlchemy models and foreign keys
- Designing a per-day token queue with a configurable limit
- Handling file uploads and serving patient reports
- Generating PDF and Excel exports with ReportLab and OpenPyXL
- Implementing billing logic with partial payments
- Containerizing a Flask app with Docker

---

## 🤖 AI-Assisted Development

I used AI tools as a pair-programming and review aid, mainly for debugging, reviewing my code, and structuring documentation. I did not paste suggestions in blindly. I read each one, checked it against how my code actually works, and ran it before keeping it.

---

## 👩‍💻 Developer

**Rizwana**, B.Tech in Computer Science & Engineering

GitHub: [github.com/Rizwana200](https://github.com/Rizwana200)

---

## 💙 EyeVault

**CARE • VISION • PRECISION**

> *Your care, our vision.*

> *Good software, like good eye care, works quietly so people can focus on what matters.*

> *Every patient seen, every token tracked, every record safe.*

> *Clear records. Shorter queues. Better care.*

Repository: [github.com/Rizwana200/EyeVault](https://github.com/Rizwana200/EyeVault)

⭐ If you find EyeVault useful, consider starring the repo.
