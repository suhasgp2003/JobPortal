# CareerNest – Django Job Portal

A Django-based job portal that focuses on real backend systems like task scheduling, async processing, OTP verification, application workflows, and rate limiting.

---

## 🛠 Tech Stack

### Backend
- Django
- PostgreSQL
- Celery
- Redis

### Frontend
- Django Templates
- HTML / CSS / JavaScript

### External Services
- Twilio (SMS)
- SMTP (Email)

---

## ⚡ Core Features

### 🔹 Scheduled Tasks (Celery Beat)
- Runs automatically every 24 hours
- Handles job lifecycle:
  - Closes applications after the deadline (no new applications allowed)
  - Later marks the job as closed and updates remaining applications
- Keeps the system consistent without manual work

---

### 🔹 Async Processing (Celery + Redis)
- Handles tasks in the background:
  - Sending emails
  - Sending OTPs
  - Updating application status
- Keeps the app fast and responsive

---

### 🔹 Rate Limiting Middleware (Redis)
- Custom middleware using Redis
- Limits how many requests a user can make
- Prevents spam and abuse
- Works using time windows

---

### 🔹 Search & Filtering
- Full-text search (FTS) using PostgreSQL
- Website supports filtering for better job discovery

---

### 🔹 OTP Verification
- Email OTP (SMTP)
- SMS OTP (Twilio)
- OTP expires after some time
- Unverified users are removed automatically

---

### 🔹 Notifications
- Sent when:
  - Application status changes
  - Interview is scheduled
  - Job is closed
- Processed in background using Celery

---

### 🔹 Job & Application Flow
- Application stages:
  - Applied → Shortlisted → Interview → Offered / Rejected
- Separate stages for:
  - Application deadline (stop applying)
  - Final job closure (after interviews)
- Prevents duplicate applications
- Supports bulk actions

---

### 🔹 Dashboards
- Candidate dashboard:
  - View applications and status

- Company dashboard:
  - Manage jobs and applicants
  - Update application status

---

## 🧠 How It Works

### Application Flow

1. Candidate applies to a job  
2. Application is saved  
3. Company updates status  
4. Notification task runs  
5. Candidate gets update  

---

### Background Task Flow

1. Action triggers a task  
2. Task goes to Redis queue  
3. Celery processes it  
4. Email/SMS is sent  

---

### Scheduled Task Flow

1. Runs every 24 hours  
2. Closes applications after deadline  
3. Later closes the job and updates applications  

---

## ⚙️ Setup

Runs out of the box on SQLite. PostgreSQL, Redis/Celery, SMTP and Twilio are optional
and switch on when their values are set in `.env` (copy `.env.example`).

| Service | Without config | With config |
|---|---|---|
| Database | SQLite (word-match search) | PostgreSQL full-text search (`POSTGRES_PASSWORD`) |
| Tasks | Run in-process; daily job lifecycle runs at most hourly on request | Celery worker + beat (`REDIS_URL`) |
| Cache / rate limit | In-memory | Redis |
| Email / OTP | Printed to the console | SMTP (`EMAIL`, `EMAIL_PASSWORD`) |
| SMS OTP | Printed to the console | Twilio (`TWILIO_SID`, `TWILIO_AUTH`, `FROM_NO`) |

### Install & run
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Companies must be approved by an admin before they can post jobs:
Admin → Companies → tick **Is verified**.

### With Redis (optional)
```bash
celery -A jobportal worker -l info --pool=solo
celery -A jobportal beat -l info
```
