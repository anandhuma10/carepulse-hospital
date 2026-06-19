# CarePulse Hospital Management System

A complete Django-based healthcare application featuring patient appointment booking, specialty department directories, and automated email notifications via Brevo API.

## Features
* **Dynamic Specialized Directories**: Detailed healthcare listings filtered by medical departments.
* **Smart Appointment Booking**: Client-facing web engine with form confirmation.
* **Patient Inquiry Systems**: Secure messaging and contact channels.
* **Central Admin Dashboard**: Protected infrastructure for reviewing live client bookings.

## Local Environment Setup
1. **Clone Repository**: 
   ```bash
   git clone https://github.com
   cd carepulse-hospital
   ```
2. **Install Core Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Settings**: Create a local `.env` file containing your production `SECRET_KEY` and your live `BREVO_API_KEY`.
4. **Database Application**:
   ```bash
   python manage.py migrate
   ```
5. **Run the Platform**:
   ```bash
   python manage.py runserver
   ```
