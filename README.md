# NovaQueue
<<<<<<< HEAD

> Smart Hospital Queue & Patient Management System

NovaQueue is a Django-based hospital queue and patient management system designed to simplify patient registration, appointment handling, queue management, doctor workflows, and AI-assisted healthcare operations.

The system provides separate workflows for patients, doctors, and administrators while keeping hospital operations organized through a centralized platform.

---

## Features

### 🏥 Hospital Queue Management

- Patient registration
- Digital queue management
- Queue status tracking
- Appointment management
- Patient waiting list
- Queue-based workflow for hospital staff

### 👤 Patient Management

- Patient registration and login
- Patient profile
- Appointment information
- Queue status
- Patient history
- Profile image support

### 👨‍⚕️ Doctor Management

- Doctor dashboard
- Patient information
- Appointment management
- Patient queue handling
- Prescription workflow
- Doctor-specific operations

### 🤖 AI-Assisted Features

NovaQueue includes AI-assisted functionality designed to support healthcare workflows.

AI functionality can assist with:

- Prescription-related assistance
- Patient information processing
- Healthcare workflow support
- AI-generated recommendations

> AI-generated information is intended as an assistance feature and should not replace professional medical judgment.

### 📊 Administrative Features

- Admin dashboard
- User management
- Patient management
- Doctor management
- Appointment monitoring
- Queue monitoring
- Hospital operation overview

### 🔐 Authentication

- Django authentication
- Login
- Logout
- User sessions
- Role-based workflow
- Django admin integration

### 🎨 Modern Interface

- Responsive UI
- Clean healthcare-focused design
- Reusable styling
- Dashboard-based interface
- Mobile-friendly layouts
- Accessible form elements

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Development database |
| HTML5 | Frontend structure |
| CSS3 | UI styling |
| JavaScript | Frontend interactions |
| Scikit-learn | Machine learning functionality |
| TextBlob | Natural language processing |
| Requests | API communication |
| Pillow | Image processing |

---

## Project Structure

```text
NovaQueue/
│
├── .github/
│   └── workflows/
│       └── django-check.yml
│
├── core/
│   ├── migrations/
│   ├── static/
│   │   └── core/
│   │       └── css/
│   │           └── novaqueue.css
│   │
│   ├── templates/
│   │   ├── admin/
│   │   ├── patient/
│   │   └── public/
│   │
│   ├── ai_engine.py
│   ├── ai_prescriptions.py
│   ├── analytics.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── hospital_qms/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt

Installation
1. Clone the repository
git clone https://github.com/utsadeepkundu/NovaQueue.git
cd NovaQueue
2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1

If PowerShell blocks activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then:

.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file from .env.example.

Copy-Item .env.example .env

Configure the required values inside .env.

Example:

DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GEMINI_API_KEY=your-api-key

Never commit .env to GitHub.

5. Apply database migrations
python manage.py makemigrations
python manage.py migrate
6. Create an administrator
python manage.py createsuperuser

Follow the prompts to create the admin account.

7. Run the development server
python manage.py runserver

Open:

http://127.0.0.1:8000/
Django Admin

The Django administration panel is available at:

http://127.0.0.1:8000/admin/

Log in using the superuser credentials created with:

python manage.py createsuperuser
Development Workflow

Run the Django development server:

python manage.py runserver

Check the project:

python manage.py check

Create migrations after changing models:

python manage.py makemigrations

Apply migrations:

python manage.py migrate
Environment Variables

NovaQueue uses environment variables for configuration and sensitive credentials.

Variable	Purpose
DJANGO_SECRET_KEY	Django security key
DEBUG	Development/debug mode
ALLOWED_HOSTS	Allowed hostnames
GEMINI_API_KEY	AI API access

Never commit real API keys, passwords, or secret keys to the repository.

AI Disclaimer

NovaQueue may provide AI-assisted functionality for certain workflows.

AI-generated information can contain errors and should be treated as supportive information rather than a medical diagnosis, prescription, or substitute for qualified healthcare professionals.

Security

For development:

DEBUG=True

For production:

DEBUG=False

Production deployments should also use:

A secure Django secret key
Environment variables for credentials
HTTPS
Proper ALLOWED_HOSTS
Secure cookies
Production-grade database configuration
Proper static/media file handling
Testing

Run Django's system checks:

python manage.py check

The project also includes a GitHub Actions workflow that performs Django validation on repository changes.

Future Improvements

Potential future improvements include:

Real-time queue updates
SMS/email notifications
Online appointment booking
Advanced hospital analytics
Doctor availability scheduling
Patient notification system
Improved AI-assisted workflows
PostgreSQL production support
Docker deployment
Cloud deployment
Progressive Web App support
License

This project is licensed under the MIT License.

See the LICENSE file for more information.

Author

Utsadeep Kundu

Computer Science & Engineering
Artificial Intelligence & Machine Learning

Project Status

🚧 Active Development

NovaQueue is currently under development and features may change as the project evolves.


## One small change I'd make before you push

Since your current project uses **Django 6.1.1**, I'd avoid claiming a specific Django version in the README unless we deliberately pin it in `requirements.txt`.

Your traceback confirms you're currently running Django 6.1.1. :contentReference[oaicite:0]{index=0}

So the README above intentionally says simply **Django** rather than putting a potentially outdated version number there.

After replacing both files:

```powershell
git add .gitignore README.md
git commit -m "Improve project documentation and gitignore"
git push origin main

Then your GitHub repo will have a much cleaner first impression.
=======
Smart Queue Management System
>>>>>>> 9b00cfedfebf7c4109eeffbaeb3b3fa30d7b5de0
