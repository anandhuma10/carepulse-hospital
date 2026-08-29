# 🏥 CarePulse Hospital Management System

A full-stack **hospital management and healthcare web application** built with **Django and Django REST Framework (DRF)**.

CarePulse provides a patient-facing hospital website with department and doctor directories, appointment booking, contact inquiries, email notifications, a staff dashboard, REST APIs, JWT authentication, API documentation, and an **AI-powered doctor/department recommendation system**.

## 🌐 Live Demo

**Live Application:**
https://carepulse-hospital.onrender.com

**API Documentation:**
`/api/docs/`

**API Schema:**
`/api/schema/`

---

## ✨ Features

### 🏥 Hospital Website

* Hospital homepage
* About hospital section
* Medical department directory
* Doctor directory
* Doctors filtered by department
* Responsive user interface
* Contact/inquiry form

### 📅 Appointment Management

* Patient appointment booking
* Department selection
* Doctor selection
* Appointment date and time selection
* Patient contact information
* Appointment confirmation
* Appointment records stored in the database
* Staff dashboard for managing appointments

### 📩 Email Notifications

* Automated appointment confirmation emails
* Email configuration using **Brevo SMTP**
* Patient receives appointment details after successful booking

### 👨‍💼 Staff Dashboard

Staff members can:

* View patient inquiries
* View appointment bookings
* View individual inquiries
* Delete inquiries
* Delete appointments
* Manage hospital data through Django Admin

### 🤖 AI Doctor Recommendation

CarePulse includes an AI-powered recommendation feature.

Patients can enter:

* Body area
* Symptoms
* Symptoms written in English
* Malayalam
* Manglish
* Other supported natural-language descriptions

The system uses **Google Gemini** to recommend the most relevant hospital department.

The AI does **not diagnose diseases**.

Example:

```text
Body Area:
Abdomen

Symptoms:
I have stomach pain and gas after eating.
```

The system may recommend:

```text
Department:
General Medicine

Reason:
The symptoms may be appropriate for an initial evaluation
by a General Medicine specialist.

Recommended Doctors:
• Doctor 1
• Doctor 2
```

The recommended doctors are retrieved from the hospital database based on the AI-selected department.

> ⚠️ The AI recommendation feature provides general guidance only and is not a medical diagnosis.

---

# 🔐 REST API

CarePulse uses **Django REST Framework** to provide RESTful APIs.

### Technologies used

* Django REST Framework
* ModelSerializer
* ViewSets
* Custom permissions
* JWT Authentication
* DRF Spectacular

### API capabilities

* Department API
* Doctor API
* Appointment API
* AI Doctor Recommendation API
* JWT authentication
* API documentation

---

# 🔑 JWT Authentication

The project uses **JSON Web Tokens (JWT)** for API authentication.

### Obtain Token

```http
POST /api/auth/token/
```

### Refresh Token

```http
POST /api/auth/token/refresh/
```

Example request:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

The server returns an access token and refresh token.

Use the access token in authenticated API requests:

```http
Authorization: Bearer <access_token>
```

---

# 📚 API Documentation

Interactive API documentation is available through **Swagger UI**.

```text
/api/docs/
```

Open the deployed application and navigate to:

```text
https://carepulse-hospital.onrender.com/api/docs/
```

The OpenAPI schema is available at:

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

### Response

```json
{
    "department": "General Medicine",
    "reason": "The symptoms are suitable for an initial evaluation by General Medicine.",
    "doctors": [
        {
            "id": 1,
            "name": "Dr. Example"
        }
    ]
}
```

The department returned by Gemini is validated against the departments available in the database before doctors are retrieved.

---

# 🗄️ Database Models

The application currently uses models for managing hospital information and appointments.

### Department

Stores hospital department information.

Example:

```text
Department
├── Name
├── Description
└── Image
```

### Doctor

Stores doctor information and their associated department.

```text
Doctor
├── Name
├── Department
├── Specialization
└── Image
```

### Appointment

Stores authenticated API appointment records.

```text
Appointment
├── Patient
├── Doctor
├── Department
├── Appointment Date
└── Status
```

### AppointmentBooking

Stores appointments submitted through the website booking form.

### ContactInquiry

Stores patient/user contact inquiries.

---

# 🏗️ Project Architecture

```text
User
 │
 ├── Hospital Website
 │       │
 │       ├── Departments
 │       ├── Doctors
 │       ├── Appointment Booking
 │       └── Contact Form
 │
 ├── AI Doctor Recommendation
 │       │
 │       ├── Symptom
 │       ├── Body Area
 │       ↓
 │     Gemini API
 │       ↓
 │   Department Recommendation
 │       ↓
 │   Database
 │       ↓
 │   Recommended Doctors
 │
 └── REST API
         │
         ├── JWT Authentication
         ├── Department API
         ├── Doctor API
         └── Appointment API
```

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

# 🛠️ Tech Stack

| Category          | Technology                |
| ----------------- | ------------------------- |
| Backend           | Python                    |
| Web Framework     | Django                    |
| REST API          | Django REST Framework     |
| Authentication    | JWT / SimpleJWT           |
| API Documentation | DRF Spectacular / Swagger |
| Database          | SQLite / PostgreSQL       |
| AI                | Google Gemini API         |
| Email             | Brevo SMTP                |
| Frontend          | HTML, CSS, JavaScript     |
| Static Files      | WhiteNoise                |
| Version Control   | Git & GitHub              |
| Deployment        | Render                    |

---

# 🚀 Local Environment Setup

## 1. Clone the Repository

```bash
git clone https://github.com/anandhuma10/carepulse-hospital.git
```

```bash
cd carepulse-hospital
```

## 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

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

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

BREVO_API_KEY=your-brevo-api-key
EMAIL_HOST_USER=your-email@example.com

GEMINI_API_KEY=your-gemini-api-key
```

> Never commit `.env` or API keys to GitHub.

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

The application is deployed using **Render**.

Production deployment requires environment variables such as:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL
BREVO_API_KEY
EMAIL_HOST_USER
GEMINI_API_KEY
```

Static files are collected during deployment:

```bash
python manage.py collectstatic --noinput
```

The production database can use PostgreSQL through the `DATABASE_URL` environment variable.

---

# 🔒 Security

The project follows several basic security practices:

* Environment variables for secrets
* JWT authentication for APIs
* Custom API permissions
* Django CSRF protection
* Django password validation
* Staff-only dashboard access
* `.env` excluded from Git
* Production `DEBUG=False`
* Secure API authentication

---

# 🧪 Development Workflow

The project uses Git branches for feature development.

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

Feature changes are developed separately and merged into the appropriate branch after testing.

---

# 🔮 Future Improvements

Possible future improvements include:

* Patient registration and profile management
* Online appointment availability
* Doctor authentication
* Appointment status tracking
* Prescription management
* Medical record management
* Doctor availability schedules
* Appointment cancellation
* Email/SMS reminders
* Improved AI safety and validation
* AI-powered symptom categorization
* PostgreSQL production optimization
* Automated testing
* Docker containerization
* CI/CD pipeline

---

# ⚠️ Medical Disclaimer

CarePulse's AI Doctor Recommendation feature is intended only for **general informational guidance**.

It does not provide medical diagnosis, treatment, or emergency medical advice.

Users should consult a qualified healthcare professional for medical concerns. In an emergency, users should contact appropriate emergency medical services.

---

# 👨‍💻 Author

**Anandhu M.A.**

GitHub:
https://github.com/anandhuma10

---

# 📄 License

This project is intended for educational and portfolio purposes.

```
```
