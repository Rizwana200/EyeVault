from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook
from flask import send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# -------------------------
# Patient Table
# -------------------------
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(15), unique=True)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    phone = db.Column(db.String(15), unique=True)

    password = db.Column(db.String(100))
# -------------------------
# Visit Table
# -------------------------
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    visit_date = db.Column(db.String(20))
    doctor_name = db.Column(db.String(100))
    diagnosis = db.Column(db.String(200))
    notes = db.Column(db.Text)

# -------------------------
# Report Table
# -------------------------
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    file_name = db.Column(db.String(255))
    upload_date = db.Column(db.String(20))
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    token_number = db.Column(db.Integer)

    visit_date = db.Column(db.String(20))

    status = db.Column(db.String(20))

    source = db.Column(db.String(20))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    specialization = db.Column(db.String(100))

    available_time = db.Column(db.String(100))
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey('doctor.id')
    )

    appointment_date = db.Column(db.String(20))

    appointment_time = db.Column(db.String(20))

    status = db.Column(db.String(20))
# -------------------------
# Home Page
# -------------------------
@app.route('/')
def home():
    return render_template('home.html')

# -------------------------
# Patient Registration
# -------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        phone = request.form['phone']

        existing_patient = Patient.query.filter_by(
            phone=phone
        ).first()

        if existing_patient:

            return render_template(
                'register.html',
                error="Patient already registered with this phone number"
            )

        patient = Patient(
            name=request.form['name'],
            dob=request.form['dob'],
            gender=request.form['gender'],
            phone=phone
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/patients')

    return render_template('register.html')

# -------------------------
# Patient Login
# -------------------------
# -------------------------
# Patient Login
# -------------------------
@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():

    if request.method == 'POST':

        phone = request.form['phone']

        patient = Patient.query.filter_by(
            phone=phone
        ).first()

        if patient:
            return redirect(f'/patient-dashboard/{patient.id}')
        return "Patient not found"

    return render_template('patient_login.html')
# -------------------------
# Staff Login
# -------------------------

@app.route('/staff-login', methods=['GET', 'POST'])
def staff_login():

    if request.method == 'POST':

        phone = request.form['phone']
        password = request.form['password']

        staff = Staff.query.filter_by(
            phone=phone,
            password=password
        ).first()

        if staff:
            return redirect('/staff-dashboard')

        return "Invalid Phone Number or Password"

    return render_template('staff_login.html')
# -------------------------
# Staff Dashboard
# -------------------------
@app.route('/staff-dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')

# -------------------------
# View All Patients
# -------------------------
@app.route('/patients')
def patients():

    all_patients = Patient.query.all()

    return render_template(
        'patients.html',
        patients=all_patients
    )

# -------------------------
# Search Patient
# -------------------------
@app.route('/search-patient', methods=['POST'])
def search_patient():

    phone = request.form['phone']

    patient = Patient.query.filter_by(
        phone=phone
    ).first()

    return render_template(
        'patient_details.html',
        patient=patient
    )

# -------------------------
# Add Visit
# -------------------------
@app.route('/add-visit/<int:patient_id>',
           methods=['GET', 'POST'])
def add_visit(patient_id):

    if request.method == 'POST':

        visit = Visit(
            patient_id=patient_id,
            visit_date=request.form['visit_date'],
            doctor_name=request.form['doctor_name'],
            diagnosis=request.form['diagnosis'],
            notes=request.form['notes']
        )

        db.session.add(visit)
        db.session.commit()

        return redirect(f'/history/{patient_id}')

    return render_template(
        'add_visit.html',
        patient_id=patient_id
    )

# -------------------------
# Patient History
# -------------------------
@app.route('/history/<int:patient_id>')
def history(patient_id):

    visits = Visit.query.filter_by(
        patient_id=patient_id
    ).all()

    patient = Patient.query.get(patient_id)

    return render_template(
        'history.html',
        visits=visits,
        patient=patient
    )

# -------------------------
# Upload Report
# -------------------------
@app.route('/upload-report/<int:patient_id>',
           methods=['GET', 'POST'])
def upload_report(patient_id):

    if request.method == 'POST':

        file = request.files['report']

        filename = secure_filename(file.filename)

        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        report = Report(
            patient_id=patient_id,
            file_name=filename,
            upload_date=request.form['upload_date']
        )

        db.session.add(report)
        db.session.commit()

        return redirect(f'/reports/{patient_id}')

    return render_template(
        'upload_report.html',
        patient_id=patient_id
    )

# -------------------------
# View Reports
# -------------------------
@app.route('/reports/<int:patient_id>')
def reports(patient_id):

    patient_reports = Report.query.filter_by(
        patient_id=patient_id
    ).all()

    return render_template(
        'reports.html',
        reports=patient_reports
    )
@app.route('/generate-token/<int:patient_id>')
def generate_token(patient_id):

    last_token = Token.query.order_by(
        Token.token_number.desc()
    ).first()

    if last_token:
        next_token = last_token.token_number + 1
    else:
        next_token = 1

    token = Token(
        patient_id=patient_id,
        token_number=next_token,
        visit_date=str(date.today()),
        status="Waiting",
        source="App"
    )

    db.session.add(token)
    db.session.commit()

    return f"Token Generated Successfully. Token No: {next_token}"
@app.route('/patient-dashboard/<int:patient_id>')
def patient_dashboard(patient_id):

    patient = Patient.query.get(patient_id)

    return render_template(
        'patient_dashboard.html',
        patient=patient
    )
@app.route('/token-dashboard')
def token_dashboard():

    tokens = Token.query.order_by(
        Token.token_number
    ).all()

    patients = {}

    for token in tokens:
        patient = Patient.query.get(
            token.patient_id
        )
        patients[token.patient_id] = patient

    total_tokens = len(tokens)

    waiting = Token.query.filter_by(
        status='Waiting'
    ).count()

    in_progress = Token.query.filter_by(
        status='In Progress'
    ).count()

    completed = Token.query.filter_by(
        status='Completed'
    ).count()

    return render_template(
        'token_dashboard.html',
        tokens=tokens,
        patients=patients,
        total_tokens=total_tokens,
        waiting=waiting,
        in_progress=in_progress,
        completed=completed
    )
@app.route('/update-token/<int:token_id>/<status>')
def update_token(token_id, status):

    token = Token.query.get(token_id)

    if token:
        token.status = status
        db.session.commit()

    return redirect('/token-dashboard')   
@app.route('/my-token/<int:patient_id>')
def my_token(patient_id):

    token = Token.query.filter_by(
        patient_id=patient_id
    ).order_by(
        Token.token_number.desc()
    ).first()

    current_token = Token.query.filter_by(
        status='In Progress'
    ).first()

    return render_template(
        'my_token.html',
        token=token,
        current_token=current_token
    )
@app.route('/staff-register', methods=['GET', 'POST'])
def staff_register():

    if request.method == 'POST':

        staff = Staff(
            name=request.form['name'],
            phone=request.form['phone'],
            password=request.form['password']
        )

        db.session.add(staff)
        db.session.commit()

        return redirect('/staff-login')

    return render_template('staff_register.html') 

@app.route('/export-tokens')
def export_tokens():

    wb = Workbook()
    ws = wb.active

    ws.title = "Tokens"

    ws.append([
        "Token Number",
        "Patient Name",
        "Phone",
        "Status",
        "Source"
    ])

    tokens = Token.query.all()

    for token in tokens:

        patient = Patient.query.get(
            token.patient_id
        )

        ws.append([
            token.token_number,
            patient.name,
            patient.phone,
            token.status,
            token.source
        ])

    file_name = "tokens.xlsx"

    wb.save(file_name)

    return send_file(
        file_name,
        as_attachment=True
    )  
    
@app.route('/download-history/<int:patient_id>')
def download_history(patient_id):

    patient = Patient.query.get(patient_id)

    visits = Visit.query.filter_by(
        patient_id=patient_id
    ).all()

    pdf_file = f"patient_{patient_id}.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            f"Patient Name: {patient.name}",
            styles['Title']
        )
    )

    elements.append(
        Paragraph(
            f"Phone: {patient.phone}",
            styles['Normal']
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Visit History",
            styles['Heading2']
        )
    )

    for visit in visits:

        elements.append(
            Paragraph(
                f"Date: {visit.visit_date}",
                styles['Normal']
            )
        )

        elements.append(
            Paragraph(
                f"Doctor: {visit.doctor_name}",
                styles['Normal']
            )
        )

        elements.append(
            Paragraph(
                f"Diagnosis: {visit.diagnosis}",
                styles['Normal']
            )
        )

        elements.append(
            Paragraph(
                f"Notes: {visit.notes}",
                styles['Normal']
            )
        )

        elements.append(Spacer(1, 10))

    doc.build(elements)

    return send_file(
        pdf_file,
        as_attachment=True
    )   

@app.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():

    if request.method == 'POST':

        doctor = Doctor(
            name=request.form['name'],
            specialization=request.form['specialization'],
            available_time=request.form['available_time']
        )

        db.session.add(doctor)
        db.session.commit()

        return redirect('/doctors')

    return render_template('add_doctor.html')

@app.route('/doctors')
def doctors():

    doctors = Doctor.query.all()

    return render_template(
        'doctors.html',
        doctors=doctors
    )   
    
@app.route('/book-appointment/<int:patient_id>', methods=['GET', 'POST'])
def book_appointment(patient_id):

    doctors = Doctor.query.all()

    if request.method == 'POST':

        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=request.form['doctor_id'],
            appointment_date=request.form['appointment_date'],
            appointment_time=request.form['appointment_time'],
            status='Booked'
        )

        db.session.add(appointment)
        db.session.commit()

        return "Appointment Booked Successfully"

    return render_template(
        'book_appointment.html',
        doctors=doctors,
        patient_id=patient_id
    )


@app.route('/manual-token', methods=['GET', 'POST'])
def manual_token():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        source = request.form['source']

        patient = Patient.query.filter_by(phone=phone).first()

        if not patient:
            patient = Patient(
                name=name,
                dob="Not Provided",
                gender="Not Provided",
                phone=phone
            )
            db.session.add(patient)
            db.session.commit()

        last_token = Token.query.order_by(
            Token.token_number.desc()
        ).first()

        if last_token:
            next_token = last_token.token_number + 1
        else:
            next_token = 1

        token = Token(
            patient_id=patient.id,
            token_number=next_token,
            visit_date=str(date.today()),
            status="Waiting",
            source=source
        )

        db.session.add(token)
        db.session.commit()

        return f"Token Created Successfully. Token No: {next_token}"

    return render_template('manual_token.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)