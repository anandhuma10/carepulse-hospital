# 🏥 CarePulse Hospital Management System

A full-stack **hospital management and healthcare web application** built with **Python, Django, and Django REST Framework (DRF)**.

CarePulse is designed around a realistic healthcare workflow connecting **patients, doctors, specialties, availability, appointment slots, and role-based portals**.

The system also includes an **AI-powered symptom-to-specialty recommendation workflow**, JWT authentication, REST APIs, email notifications through Brevo, and API testing with Postman.

---

## 🌐 Live Demo

**Live Application:**
https://anandhu10.pythonanywhere.com/

**API Documentation:**
`/api/docs/`

**API Schema:**
`/api/schema/`

---

# ✨ Key Features

## 👤 Patient Accounts & PatientProfile

Patients can have their own accounts and profiles.

The patient workflow is connected to the appointment system so that appointments can be associated with the appropriate patient.

---

## 📅 Appointment Management

CarePulse uses a structured appointment workflow connecting:

```text
Patient
   ↓
Doctor
   ↓
Date
   ↓
Available Time Slot
   ↓
Appointment
```

Features include:

* Patient appointment booking
* Doctor selection
* Department/specialty selection
* Appointment date selection
* Dynamic time slots
* Appointment status
* Patient-doctor relationship
* Double-booking prevention
* Appointment management

---

# 👨‍⚕️ Doctor Availability

Doctor availability is considered when generating appointment slots.

The system can determine available appointment times based on the doctor's configured availability.

```text
Doctor Availability
        ↓
Available Date
        ↓
Available Time Slots
        ↓
Patient Booking
```

---

# ⏰ Dynamic Time Slots

Instead of allowing patients to select arbitrary appointment times, available slots are generated based on doctor availability.

This creates a more realistic appointment scheduling workflow.

---

# 🚫 Double-Booking Prevention

The appointment workflow validates existing bookings before allowing a slot to be booked.

This helps prevent multiple patients from booking the same doctor and time slot.

```text
Patient selects slot
        ↓
Check existing appointment
        ↓
Slot available?
     ↙       ↘
   YES        NO
    ↓          ↓
 Book       Reject
```

---

# 🤖 AI-Powered Specialty Recommendation

CarePulse includes an AI-powered symptom recommendation system using **Google Gemini**.

Patients can provide:

* Body area
* Symptoms
* English descriptions
* Malayalam
* Manglish
* Other supported natural-language descriptions

Example:

```text
Body Area:
Abdomen

Symptoms:
I have stomach pain and gas after eating.
```

The AI recommends an appropriate hospital specialty/department.

The workflow is designed as:

```text
Patient Symptoms
       ↓
   Gemini AI
       ↓
Specialty Recommendation
       ↓
Available Doctors
       ↓
Available Slots
       ↓
Appointment
```

### ⚠️ Medical Disclaimer

The AI recommendation system provides general informational guidance only.

It does **not diagnose diseases or provide medical treatment**.

Patients should consult a qualified healthcare professional for medical concerns.

---

# 🏥 Specialty Routing

The AI recommendation is connected to the hospital's department/specialty data.

The recommended specialty is validated against available departments before retrieving relevant doctors.

```text
Symptoms
   ↓
AI Recommendation
   ↓
Department
   ↓
Doctors
   ↓
Doctor Availability
   ↓
Available Slots
```

This makes the AI feature part of the appointment workflow rather than an isolated recommendation page.

---

# 👥 Role-Based Portals

CarePulse provides separate workflows for different types of users.

## 📋 Patient Portal

Patients can:

* Manage their profile
* View appointment information
* Follow their appointment workflow
* Select doctors and available slots

---

## 👨‍⚕️ Doctor Portal

Doctors have their own dashboard for managing their assigned appointments.

The doctor dashboard provides access to the relevant appointment and patient information needed by the doctor.

---

## 🧑‍💼 Staff Portal

Hospital staff have a separate dashboard for appointment management.

Staff can:

* View appointments
* Confirm appointments
* Cancel appointments
* Manage appointment status

### 🔒 Role-Based Data Access

Staff members **do not have access to the patient's illness/symptom information**.

Patient medical/symptom information is restricted to the appropriate doctor-side workflow.

This implements a more realistic **role-based access control** approach instead of giving every user access to the same information.

---

# 📩 Email Notifications

CarePulse uses **Brevo** for email communication.

Features include:

* Appointment confirmation emails
* Appointment details sent to patients
* SMTP/email service integration

```text
Appointment Created
        ↓
Django Backend
        ↓
Brevo SMTP
        ↓
Patient Email
```

---

# 🔐 Authentication & Authorization

The project uses **JWT authentication** for API access.

### Obtain Token

```http
POST /api/auth/token/
```

### Refresh Token

```http
POST /api/auth/token/refresh/
```

Example:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Authenticated requests use:

```http
Authorization: Bearer <access_token>
```

Role-based permissions are used to control access to different areas of the system.

---

# 🔌 REST API

CarePulse uses **Django REST Framework** to provide RESTful APIs.

### API Technologies

* Django REST Framework
* ModelSerializer
* ViewSets
* Custom permissions
* JWT / SimpleJWT
* DRF Spectacular
* Swagger UI

### API Features

* Department API
* Doctor API
* Appointment API
* AI Recommendation API
* JWT Authentication
* API Documentation

---

# 🧪 API Testing

REST APIs are tested using **Postman**.

Postman is used to test:

* API endpoints
* Authentication
* JWT tokens
* Request/response data
* Appointment APIs
* Doctor APIs
* Department APIs
* AI recommendation API

---

# 📚 API Documentation

Interactive API documentation is available through Swagger UI.

```text
/api/docs/
```

Open:

```text
https://anandhu10.pythonanywhere.com/api/docs/
```

OpenAPI schema:

```text
/api/schema/
```

---

# 🧠 AI Recommendation API

### Endpoint

```http
POST /api/ai/recommend-doctor/
```

### Request

```json
{
    "symptom": "I have stomach pain and gas after eating",
    "body_area": "Abdomen"
}
```

### Workflow

```text
Symptom + Body Area
        ↓
     Gemini AI
        ↓
 Department Validation
        ↓
 Available Doctors
        ↓
 Doctor Availability
        ↓
 Available Slots
```

The AI recommendation is validated against the hospital database before retrieving doctors.

---

# 🗄️ Database Models

The application uses Django models to manage hospital information, users, doctors, appointments, and inquiries.

### PatientProfile

Stores patient profile information associated with the patient's account.

### Department

Stores hospital department/specialty information.

```text
Department
├── Name
├── Description
└── Image
```

### Doctor

Stores doctor information and department association.

```text
Doctor
├── Name
├── Department
├── Specialization
├── Availability
└── Image
```

### Appointment

Stores structured appointment information.

```text
Appointment
├── Patient
├── Doctor
├── Department
├── Date
├── Time Slot
└── Status
```

### AppointmentBooking

Handles website appointment booking data where applicable.

### ContactInquiry

Stores patient/user contact inquiries.

---

# 🏗️ Application Architecture

```text
                         CAREPULSE
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
      Patient            Doctor             Staff
       Portal             Portal            Portal
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                     Appointment System
                            │
              ┌─────────────┼─────────────┐
              │             │             │
           Patient        Doctor       Time Slot
              │             │             │
              └─────────────┼─────────────┘
                            │
                     Appointment
                            │
                    ┌───────┴───────┐
                    │               │
              AI Recommendation   Email
                    │               │
                 Gemini           Brevo
```

---

# 🤖 AI-to-Appointment Workflow

The upgraded CarePulse workflow aims to connect the entire journey:

```text
Patient
   ↓
Symptoms + Body Area
   ↓
Gemini AI
   ↓
Specialty Recommendation
   ↓
Available Doctors
   ↓
Doctor Availability
   ↓
Dynamic Time Slots
   ↓
Double-Booking Validation
   ↓
Appointment
   ↓
Patient / Doctor / Staff Portals
```

---

# 🛠️ Tech Stack

| Category             | Technology                       |
| -------------------- | -------------------------------- |
| Programming Language | Python                           |
| Backend Framework    | Django                           |
| REST API             | Django REST Framework            |
| Authentication       | JWT / SimpleJWT                  |
| API Documentation    | DRF Spectacular / Swagger        |
| Database             | SQLite                           |
| AI                   | Google Gemini API                |
| Email                | Brevo SMTP                       |
| Frontend             | HTML, CSS, JavaScript, Bootstrap |
| Static Files         | WhiteNoise                       |
| API Testing          | Postman                          |
| Version Control      | Git & GitHub                     |
| Deployment           | PythonAnywhere                   |

---

# 📁 Project Structure

```text
carepulse-hospital/
│
├── carepulse_hospital/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── home/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   ├── ai_service.py
│   └── email_backend.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── department.html
│   ├── doctors.html
│   ├── booking_form.html
│   ├── appointment_success.html
│   ├── contact.html
│   ├── ai_doctor.html
│   └── dashboard/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── departments/
│   └── doctors/
│
├── media/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🚀 Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/anandhuma10/carepulse-hospital.git
```

```bash
cd carepulse-hospital
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

BREVO_API_KEY=your-brevo-api-key
EMAIL_HOST_USER=your-email@example.com

GEMINI_API_KEY=your-gemini-api-key
```

Never commit `.env` or API keys to GitHub.

## 5. Apply Migrations

```bash
python manage.py migrate
```

## 6. Create Admin User

```bash
python manage.py createsuperuser
```

## 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## 8. Start Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# ☁️ Deployment

The current live version of CarePulse is deployed on **PythonAnywhere**.

PythonAnywhere supports Django applications through a configured web app and WSGI configuration.

The current deployment uses **SQLite**.

SQLite is available on PythonAnywhere, although PythonAnywhere notes that SQLite is better suited to smaller/testing workloads than a production-scale database.

Production configuration includes:

* Django WSGI deployment
* Virtual environment
* Environment variables
* Static file configuration
* SQLite database
* PythonAnywhere web application

---

# 🔒 Security

The project implements several security practices:

* JWT authentication
* Role-based authorization
* Custom API permissions
* Django CSRF protection
* Django password validation
* Staff-only dashboard access
* Environment variables for secrets
* `.env` excluded from Git
* Production `DEBUG=False`
* Restricted access to patient information

---

# 🌱 Development Workflow

The project uses Git feature branches for development.

Example:

```text
main
│
├── develop
│
├── feature/doctor-api
│
├── feature/jwt-auth
│
└── feature/ai-doctor-recommendation
```

Features are developed separately, tested, and then merged into the appropriate branch.

---

# 🔮 Future Improvements

Possible future improvements include:

* Advanced doctor scheduling
* Appointment cancellation workflow
* Email/SMS reminders
* Prescription management
* Medical record management
* Improved AI safety and validation
* Automated testing
* Docker containerization
* CI/CD pipeline
* Production database optimization
* Improved monitoring and logging

---

# ⚠️ Medical Disclaimer

CarePulse's AI recommendation feature is intended only for **general informational guidance**.

It does not provide medical diagnosis, treatment, or emergency medical advice.

Users should consult a qualified healthcare professional for medical concerns.

In an emergency, users should contact appropriate emergency medical services.

---

# 👨‍💻 Author

**Anandhu M.A.**

GitHub:
https://github.com/anandhuma10

---

# 📄 License

This project is intended for educational and portfolio purposes.
