EyeVault

EyeVault is a Flask-based Hospital / Eye Clinic Management System built to manage patients, staff, visits, reports, billing, tokens, doctors, and spectacles in one place.

It helps clinic staff handle daily operations like patient registration, visit history, report uploads, token generation, billing management, and patient dashboard access.

Built With

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap 5
- Jinja2
- OpenPyXL
- ReportLab

Features

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

Project Modules

1. Patient Module
- Patient registration
- Patient login using phone number
- Patient dashboard
- View token details
- View reports
- View visit history
- View billing history

2. Staff Module
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

3. Token Management
- Generate token from patient dashboard
- Manual token generation from staff dashboard
- Token dashboard to track:
  - Waiting tokens
  - In Progress tokens
  - Completed tokens
- Token limit settings per day
- Export token details to Excel

4. Billing Management
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

5. Reports and History
- Upload patient reports
- View all uploaded reports
- Add patient visit details
- View visit history
- Download visit history as PDF

Screenshots

Home Page

![Home Page](screenshots_eyevault/home.png)

Patient Registration

![Patient Registration](screenshots_eyevault/patient-register.png)

Patient Login

![Patient Login](screenshots_eyevault/patient-login.png)

Patient Dashboard

![Patient Dashboard](screenshots_eyevault/patient-dashboard.png)

Staff Login

![Staff Login](screenshots_eyevault/staff-login.png)

Staff Dashboard

![Staff Dashboard](screenshots_eyevault/staff-dashboard.png)

Patient Information Page

![Patient Information](screenshots_eyevault/patient-information.png)

Add Visit

![Add Visit](screenshots_eyevault/add-visit.png)

Visit History

![Visit History](screenshots_eyevault/visit-history.png)

Upload Report

![Upload Report](screenshots_eyevault/upload-report.png)

Reports Page

![Reports](screenshots_eyevault/reports.png)

Add Billing

![Add Billing](screenshots_eyevault/add-billing.png)

Billing History

![Billing History](screenshots_eyevault/billing-history.png)

Edit Billing

![Edit Billing](screenshots_eyevault/edit-billing.png)

Token Dashboard

![Token Dashboard](screenshots_eyevault/token-dashboard.png)

Doctors Page

![Doctors](screenshots_eyevault/doctors.png)

Spectacles Page

![Spectacles](screenshots_eyevault/spects.png)

## Installation

Follow these steps to run the EyeVault project on your local system.

### 1. Clone the repository

```bash
git clone https://github.com/Rizwana200/EyeVault.git
cd EyeVault
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install required dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Flask application

```bash
python app.py
```

After running the project, open your browser and visit:

```bash
http://127.0.0.1:5000/
```

---

## Default Modules Available in EyeVault

The project includes the following major modules:

* Patient Registration
* Patient Login
* Staff Login
* Staff Dashboard
* Token Generation
* Manual Token Entry
* Token Dashboard
* Patient Visit History
* PDF Download of Visit History
* Report Upload and Report Viewing
* Doctor Management
* Spectacles Management
* Billing Management
* Billing Edit and Billing History
* Patient Dashboard with Billing and Visit Details

---

## Billing Features

The billing module supports:

* Bill creation for each patient
* Consultation fee entry
* Medicine fee entry
* Spectacles name entry
* Spectacles cost entry
* Total bill calculation
* Paid amount tracking
* Due amount tracking
* Payment status display as **Due** or **Completed**
* Billing history visible in both:

  * Staff side
  * Patient dashboard

---

## Project Structure

```bash
EyeVault/
│── app.py
│── requirements.txt
│── database.db
│── static/
│   ├── uploads/
│   └── screenshots_eyevault/
│── templates/
│   ├── home.html
│   ├── register.html
│   ├── patient_login.html
│   ├── staff_login.html
│   ├── staff_dashboard.html
│   ├── patient_dashboard.html
│   ├── patient_details.html
│   ├── add_visit.html
│   ├── history.html
│   ├── upload_report.html
│   ├── reports.html
│   ├── token_dashboard.html
│   ├── manual_token.html
│   ├── add_doctor.html
│   ├── doctors.html
│   ├── add_bill.html
│   ├── edit_bill.html
│   ├── billing_history.html
│   └── token_settings.html
```

---

## Screenshots

### Home Page

![Home Page](static/screenshots_eyevault/home.png)

### Patient Registration

![Patient Registration](static/screenshots_eyevault/patient_register.png)

### Patient Login

![Patient Login](static/screenshots_eyevault/patient_login.png)

### Staff Login

![Staff Login](static/screenshots_eyevault/staff_login.png)

### Staff Dashboard

![Staff Dashboard](static/screenshots_eyevault/staff_dashboard.png)

### Patient Information Page

![Patient Information](static/screenshots_eyevault/patient_info.png)

### Add Visit

![Add Visit](static/screenshots_eyevault/add_visit.png)

### Visit History

![Visit History](static/screenshots_eyevault/history.png)

### Upload Report

![Upload Report](static/screenshots_eyevault/upload_report.png)

### View Reports

![Reports](static/screenshots_eyevault/reports.png)

### Token Dashboard

![Token Dashboard](static/screenshots_eyevault/token_dashboard.png)

### Add Billing

![Add Billing](static/screenshots_eyevault/add_bill.png)

### Billing History

![Billing History](static/screenshots_eyevault/billing_history.png)

### Edit Billing

![Edit Billing](static/screenshots_eyevault/edit_bill.png)

### Patient Dashboard

![Patient Dashboard](static/screenshots_eyevault/patient_dashboard.png)

---

## Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* HTML
* CSS
* Bootstrap 5
* Jinja2
* OpenPyXL
* ReportLab

---

## Future Improvements

Possible future enhancements for the project:

* Staff session management with logout
* Admin panel for full hospital control
* Search and filter for patient history
* Online appointment booking
* SMS / Email token notification
* Payment receipt generation
* Better analytics dashboard for staff
* Cloud deployment support

---

## Author

**Rizwana**
Developed as a Hospital / Eye Clinic Management project using Flask.

GitHub Repository:
https://github.com/Rizwana200/EyeVault
