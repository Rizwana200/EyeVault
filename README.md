# EyeVault

EyeVault is a Flask-based Hospital / Eye Clinic Management System built to manage patients, staff, visits, reports, billing, tokens, doctors, and spectacles in one place.

It helps clinic staff handle daily operations like patient registration, visit history, report uploads, token generation, billing management, and patient dashboard access.

---

## Built With

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap 5
- Jinja2
- OpenPyXL
- ReportLab

---

## Features

- Patient Registration and Patient Login
- Staff Registration and Staff Login
- Patient Dashboard with:
  - Personal details
  - Token status
  - Visit history
  - Uploaded reports
  - Billing history
- Staff Dashboard for clinic operations
- Add and manage patient visits
- Upload and view patient reports
- Generate patient tokens
- Manual token generation by staff
- Token dashboard with live token status
- Token limit settings
- Add and manage doctors
- Add and manage spectacles
- Add billing for patients
- Edit billing records
- View complete billing history
- Export token records to Excel
- Download patient visit history as PDF

---

## Project Modules

### 1. Patient Module
- Patient registration
- Patient login using phone number
- Patient dashboard
- View token details
- View reports
- View visit history
- View billing history

---

### 2. Staff Module
- Staff registration
- Staff login
- Search patient by phone
- Open patient information page
- Add visit details
- Upload reports
- Generate token
- Add billing
- Edit billing
- View billing history

---

### 3. Token Management
- Generate token from patient dashboard
- Manual token generation from staff dashboard
- Token dashboard to track:
  - Waiting tokens
  - In Progress tokens
  - Completed tokens
- Token limit settings per day
- Export token details to Excel

---

### 4. Billing Management
- Add bill for a patient
- Edit bill later if payment is pending
- Track:
  - Consultation fee
  - Medicine fee
  - Spectacles name
  - Spectacles cost
  - Total amount
  - Paid amount
  - Due amount
  - Payment status (Due / Completed)
- Billing history visible in both:
  - Staff side
  - Patient dashboard

---

### 5. Reports and History
- Upload patient reports
- View all uploaded reports
- Add patient visit details
- View visit history
- Download visit history as PDF

---

## Screenshots

### Home Page
![Home Page](screenshots_eyevault/home.png)

---

### Patient Registration
![Patient Registration](screenshots_eyevault/patient-register.png)

---

### Patient Login
![Patient Login](screenshots_eyevault/patient-login.png)

---

### Patient Dashboard
![Patient Dashboard](screenshots_eyevault/patient-dashboard.png)

---

### Staff Login
![Staff Login](screenshots_eyevault/staff-login.png)

---

### Staff Dashboard
![Staff Dashboard](screenshots_eyevault/staff-dashboard.png)

---

### Patient Information Page
![Patient Information](screenshots_eyevault/patient-information.png)

---

### Add Visit
![Add Visit](screenshots_eyevault/add-visit.png)

---

### Visit History
![Visit History](screenshots_eyevault/visit-history.png)

---

### Upload Report
![Upload Report](screenshots_eyevault/upload-report.png)

---

### Reports Page
![Reports](screenshots_eyevault/reports.png)

---

### Add Billing
![Add Billing](screenshots_eyevault/add-billing.png)

---

### Billing History
![Billing History](screenshots_eyevault/billing-history.png)

---

### Edit Billing
![Edit Billing](screenshots_eyevault/edit-billing.png)

---

### Token Dashboard
![Token Dashboard](screenshots_eyevault/token-dashboard.png)

---

### Doctors Page
![Doctors](screenshots_eyevault/doctors.png)

---

### Spectacles Page
![Spectacles](screenshots_eyevault/spects.png)

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Rizwana200/EyeVault.git
cd EyeVault

⚙️ Create Virtual Environment (COPY THIS EXACTLY)
👉 Step 1: Go inside your project folder
cd EyeVault
👉 Step 2: Create virtual environment
python -m venv venv
👉 Step 3: Activate virtual environment
🪟 Windows (CMD / PowerShell)
venv\Scripts\activate
🍎 Mac / Linux
source venv/bin/activate
✅ After activation you will see this:
(venv) C:\EyeVault>

That means virtual environment is ACTIVE ✔

👉 Step 4: Install requirements
pip install -r requirements.txt
👉 Step 5: Run project
python app.py