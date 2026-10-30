<p align="center">
  <img src="https://via.placeholder.com/600x180?text=Job+Board+Web+Application" alt="Job Board Logo"/>
</p>

<h1 align="center">🧑‍💼 Job Board Web Application</h1>

<p align="center">
A complete Django job portal where employers can post jobs and users can apply.
</p>

---

### 📌 Project Status

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Status](https://img.shields.io/badge/Production_Ready-brightgreen)

---

## 🧠 Overview

This is a **fully functional Job Board Application** built using Django.  
Employers can create job listings and applicants can submit applications with resumes.

Perfect for learning Django, portfolio building, or building a real job platform.

---

## 🚀 Features

- ✔ Create and manage job listings  
- ✔ View detailed job pages  
- ✔ Apply for jobs with resume + cover letter  
- ✔ User authentication (Login/Register)  
- ✔ Profile picture upload  
- ✔ Clean UI design  

---

## 🛠️ Tech Stack

| Feature | Technology |
|--------|------------|
| Backend Framework | Django |
| Python Version | 3.12 |
| Database | SQLite |
| Frontend | HTML + CSS + Bootstrap |
| File Upload Support | Yes |
| Authentication | Django Auth System |

---

## 📂 Folder Structure

project/
│── accounts/ → Authentication & profiles
│── jobs/ → Job logic (models, forms, views)
│── jobportal/ → Core project settings
│── templates/ → HTML templates
│── static/ → CSS, images
│── media/ → Uploaded resumes/profile photos
│── db.sqlite3 → (Optional demo database)
│── manage.py
│── requirements.txt


---

## ▶️ Installation & Setup

#### 1️⃣ Create Virtual Environment
```sh
python -m venv venv

2️⃣ Activate Virtual Environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py migrate

5️⃣ Create Admin User (Optional)
python manage.py createsuperuser

6️⃣ Start Server
python manage.py runserver


Open in browser:
👉 http://127.0.0.1:8000/

✨ Future Improvements

Employer dashboard

Search & filter jobs

Email notifications

Bookmark jobs

Application status tracking

👩‍💻 Author

Suhas GP
Learning and building real-world Django applications.

