Tech Stack

Backend: Django (Python)

Frontend: Tailwind CSS, FontAwesome, JavaScript

AI/NLP: TextBlob (Sentiment & Keyword Analysis)

Database: SQLite (Default) / PostgreSQL ready

⚙️ Installation & Setup
1. install python 3.14


2. Install Dependencies

pip install django textblob django-crispy-forms pillow

3. go to downloaded project folder in terminal by cd command

4. Database Setup & Migrations

python manage.py makemigrations
python manage.py migrate


5. Create Admin Account (Hospital Staff)

Create your primary admin account to access the Hospital Control Center.

python manage.py createsuperuser


6. Run the Server

python manage.py runserver


Visit http://127.0.0.1:8000 in your browser.

🧠 AI Logic Overview

The system uses a custom MedicalAIEngine located in core/ai_engine.py:

Urgency Analysis: Uses TextBlob to perform sentiment analysis on symptoms. It also scans for critical keywords (e.g., "chest pain", "bleeding") to weight the urgency score from 1.0 to 10.0.

Wait Time Prediction: Calculates the predicted time based on the current length of the queue adjusted by the patient's individual urgency factor.