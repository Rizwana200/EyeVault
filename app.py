from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from openpyxl import Workbook
from flask import send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "eyevault_secret_key_123"
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
    

    
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_tokens_per_day = db.Column(db.Integer, default=5)


class Spect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patient.id')
    )

    bill_date = db.Column(db.String(20))

    consultation_fee = db.Column(db.Float, default=0)
    medicine_fee = db.Column(db.Float, default=0)

    spect_name = db.Column(db.String(100), default="")
    spect_cost = db.Column(db.Float, default=0)

    total_amount = db.Column(db.Float, default=0)
    paid_amount = db.Column(db.Float, default=0)
    due_amount = db.Column(db.Float, default=0)

    payment_status = db.Column(db.String(20), default="Due")
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

    msg = request.args.get('msg')
    msg_type = request.args.get('type')

    if request.method == 'POST':

        phone = request.form['phone']

        existing_patient = Patient.query.filter_by(
            phone=phone
        ).first()

        if existing_patient:
            return redirect('/register?msg=Patient already registered&type=danger')

        patient = Patient(
            name=request.form['name'],
            dob=request.form['dob'],
            gender=request.form['gender'],
            phone=phone
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/register?msg=Patient registered successfully&type=success')

    return render_template(
        'register.html',
        msg=msg,
        msg_type=msg_type
    )

# -------------------------
# Patient Login
# -------------------------
# -------------------------
# Patient Login
@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():

    if request.method == 'POST':

        phone = request.form['phone']

        patient = Patient.query.filter_by(phone=phone).first()

        if patient:
            return redirect(f'/patient-dashboard/{patient.id}')
        else:
            return render_template(
                'patient_login.html',
                error="Patient not found"
            )

    return render_template('patient_login.html')


# -------------------------
# Staff Login
# -------------------------
from flask import flash, render_template, request, redirect

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

        flash("Invalid Phone Number or Password", "error")
        return redirect('/staff-login')

    return render_template('staff_login.html')
# Staff Dashboard
@app.route('/staff-dashboard')
def staff_dashboard():

    msg = request.args.get('msg')

    return render_template(
        'staff_dashboard.html',
        msg=msg
    )

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

    today = str(date.today())

    settings = Settings.query.first()

    if not settings:
        settings = Settings(max_tokens_per_day=5)
        db.session.add(settings)
        db.session.commit()

    today_tokens_count = Token.query.filter_by(
        visit_date=today
    ).count()

    if today_tokens_count >= settings.max_tokens_per_day:
        return redirect(
            f'/patient-dashboard/{patient_id}?msg=Today token limit reached'
        )

    existing_token = Token.query.filter_by(
        patient_id=patient_id,
        visit_date=today
    ).first()

    if existing_token:
        return redirect(
            f'/patient-dashboard/{patient_id}?msg=You already have a token today. Token No: {existing_token.token_number}'
        )

    last_token_today = Token.query.filter_by(
        visit_date=today
    ).order_by(Token.token_number.desc()).first()

    if last_token_today:
        next_token = last_token_today.token_number + 1
    else:
        next_token = 1

    token = Token(
        patient_id=patient_id,
        token_number=next_token,
        visit_date=today,
        status="Waiting",
        source="App"
    )

    db.session.add(token)
    db.session.commit()

    return redirect(
        f'/patient-dashboard/{patient_id}?msg=Token generated successfully. Your token number is {next_token}'
    )
@app.route('/patient-dashboard/<int:patient_id>')
def patient_dashboard(patient_id):

    patient = Patient.query.get(patient_id)

    today = str(date.today())

    token = Token.query.filter_by(
        patient_id=patient_id,
        visit_date=today
    ).order_by(Token.token_number.desc()).first()

    current_token = Token.query.filter_by(
        visit_date=today,
        status='In Progress'
    ).first()

    completed_count = Token.query.filter_by(
        visit_date=today,
        status='Completed'
    ).count()

    token_closed = False
    settings = Settings.query.first()

    if settings:
        today_tokens_count = Token.query.filter_by(
            visit_date=today
        ).count()

        if today_tokens_count >= settings.max_tokens_per_day:
            token_closed = True

    visits = Visit.query.filter_by(
        patient_id=patient_id
    ).order_by(Visit.id.desc()).all()

    reports = Report.query.filter_by(
        patient_id=patient_id
    ).order_by(Report.id.desc()).all()

    bills = Billing.query.filter_by(
        patient_id=patient_id
    ).order_by(Billing.id.desc()).all()

    msg = request.args.get('msg')

    return render_template(
        'patient_dashboard.html',
        patient=patient,
        token=token,
        current_token=current_token,
        completed_count=completed_count,
        token_closed=token_closed,
        visits=visits,
        reports=reports,
        bills=bills,
        msg=msg
    )
@app.route('/token-dashboard')
def token_dashboard():

    today = str(date.today())

    tokens = Token.query.filter_by(
        visit_date=today
    ).order_by(
        Token.token_number
    ).all()

    patients = {}

    for token in tokens:
        patient = Patient.query.get(token.patient_id)
        patients[token.patient_id] = patient

    total_tokens = len(tokens)

    waiting = Token.query.filter_by(
        visit_date=today,
        status='Waiting'
    ).count()

    in_progress = Token.query.filter_by(
        visit_date=today,
        status='In Progress'
    ).count()

    completed = Token.query.filter_by(
        visit_date=today,
        status='Completed'
    ).count()

    settings = Settings.query.first()

    return render_template(
        'token_dashboard.html',
        tokens=tokens,
        patients=patients,
        total_tokens=total_tokens,
        waiting=waiting,
        in_progress=in_progress,
        completed=completed,
        settings=settings,
        today=today
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

    msg = request.args.get('msg')
    msg_type = request.args.get('type')

    if request.method == 'POST':

        phone = request.form['phone']

        existing_staff = Staff.query.filter_by(
            phone=phone
        ).first()

        if existing_staff:
            return redirect('/staff-register?msg=Staff already registered&type=danger')

        staff = Staff(
            name=request.form['name'],
            phone=phone,
            password=request.form['password']
        )

        db.session.add(staff)
        db.session.commit()

        return redirect('/staff-register?msg=Staff registered successfully&type=success')

    return render_template(
        'staff_register.html',
        msg=msg,
        msg_type=msg_type
    )

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

        today = str(date.today())

        settings = Settings.query.first()

        if not settings:
            settings = Settings(max_tokens_per_day=5)
            db.session.add(settings)
            db.session.commit()

        today_tokens_count = Token.query.filter_by(
            visit_date=today
        ).count()

        if today_tokens_count >= settings.max_tokens_per_day:
            return redirect('/staff-dashboard?msg=Today token limit reached')

        last_token_today = Token.query.filter_by(
            visit_date=today
        ).order_by(Token.token_number.desc()).first()

        if last_token_today:
            next_token = last_token_today.token_number + 1
        else:
            next_token = 1

        token = Token(
            patient_id=patient.id,
            token_number=next_token,
            visit_date=today,
            status="Waiting",
            source=source
        )

        db.session.add(token)
        db.session.commit()

        return redirect(f'/staff-dashboard?msg=Token created successfully. Token No: {next_token}')

    return render_template('manual_token.html')
@app.route('/token-settings', methods=['GET', 'POST'])
def token_settings():

    settings = Settings.query.first()

    if not settings:
        settings = Settings(max_tokens_per_day=5)
        db.session.add(settings)
        db.session.commit()

    if request.method == 'POST':
        settings.max_tokens_per_day = int(request.form['max_tokens'])
        db.session.commit()
        return redirect('/token-dashboard')

    return render_template(
        'token_settings.html',
        settings=settings
    )


@app.route('/add-spect', methods=['GET', 'POST'])
def add_spect():

    if request.method == 'POST':

        spect = Spect(
            name=request.form['name'],
            price=float(request.form['price'])
        )

        db.session.add(spect)
        db.session.commit()

        return redirect('/spects')

    return render_template('add_spect.html')


@app.route('/spects')
def spects():

    spects = Spect.query.all()

    return render_template(
        'spects.html',
        spects=spects)
@app.route('/add-bill/<int:patient_id>', methods=['GET', 'POST'])
def add_bill(patient_id):

    if request.method == 'POST':

        bill_date = request.form['bill_date']
        consultation_fee = float(request.form.get('consultation_fee', 0))
        medicine_fee = float(request.form.get('medicine_fee', 0))
        spect_name = request.form.get('spect_name', '')
        spect_cost = float(request.form.get('spect_cost', 0))
        paid_amount = float(request.form.get('paid_amount', 0))

        total = consultation_fee + medicine_fee + spect_cost
        due = total - paid_amount

        if due < 0:
            due = 0

        status = "Completed" if due == 0 else "Due"

        bill = Billing(
            patient_id=patient_id,
            bill_date=bill_date,
            consultation_fee=consultation_fee,
            medicine_fee=medicine_fee,
            spect_name=spect_name,
            spect_cost=spect_cost,
            total_amount=total,
            paid_amount=paid_amount,
            due_amount=due,
            payment_status=status
        )

        db.session.add(bill)
        db.session.commit()

        return redirect(f'/billing-history/{patient_id}')

    return render_template('add_bill.html', patient_id=patient_id)
@app.route('/billing-history/<int:patient_id>')
def billing_history(patient_id):

    patient = Patient.query.get(patient_id)

    bills = Billing.query.filter_by(
        patient_id=patient_id
    ).order_by(Billing.id.desc()).all()

    return render_template(
        'billing_history.html',
        patient=patient,
        bills=bills
    )
@app.route('/edit-bill/<int:bill_id>', methods=['GET', 'POST'])
def edit_bill(bill_id):

    bill = Billing.query.get_or_404(bill_id)

    if request.method == 'POST':

        bill.bill_date = request.form['bill_date']
        bill.consultation_fee = float(request.form.get('consultation_fee', 0))
        bill.medicine_fee = float(request.form.get('medicine_fee', 0))
        bill.spect_name = request.form.get('spect_name', '')
        bill.spect_cost = float(request.form.get('spect_cost', 0))
        bill.paid_amount = float(request.form.get('paid_amount', 0))

        bill.total_amount = (
            bill.consultation_fee +
            bill.medicine_fee +
            bill.spect_cost
        )

        bill.due_amount = bill.total_amount - bill.paid_amount

        if bill.due_amount < 0:
            bill.due_amount = 0

        bill.payment_status = "Completed" if bill.due_amount == 0 else "Due"

        db.session.commit()

        return redirect(f'/billing-history/{bill.patient_id}')

    return render_template('edit_bill.html', bill=bill)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)

