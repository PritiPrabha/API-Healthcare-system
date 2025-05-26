# API-Healthcare-system
A basic Flask RESTful API for managing doctor-patient interactions in a healthcare system.
# HealthConnect 🏥

**HealthConnect** is a secure web-based system built using Flask that enables patients to register, describe their health problems, and be matched with relevant doctors. It uses JWT for authentication and MySQL as the backend database.

---

## 🚀 Project Overview

This project provides RESTful APIs for:

- Patient registration and login
- Doctor registration and login
- Submitting health-related queries
- Matching patients with doctors using keyword-based logic
- Viewing patient history and profiles securely

---

## 🛠️ Key Technologies

- **Flask** – Web framework for building APIs
- **MySQL** – Relational database for storing users and queries
- **Flask-JWT-Extended** – JWT-based user authentication
- **Flask-Bcrypt** – Secure password hashing
- **Flask-CORS** – Handling cross-origin requests
- **Postman / CURL** – For testing APIs

---

## 📁 Project Structure

- `pro.py`: Patient routes (register, login, profile, query submission)
- `doc.py`: Doctor routes (register, login, profile)
- `query.py`: Logic to handle and match patient queries with doctors

---

## 🔐 Authentication

JWT is used to protect sensitive endpoints like `/profile1`, `/profile2`, `/userhistory`, and `/tellproblem`.

---

## 📌 API Endpoints

### Patient Endpoints (`pro.py`)
| Endpoint         | Method | Description                             |
|------------------|--------|-----------------------------------------|
| `/addtodo`       | POST   | Register a new patient                  |
| `/userlogin`     | POST   | Login and receive JWT token             |
| `/viewalltodo`   | GET    | View all patient names and places       |
| `/profile1`      | GET    | View logged-in patient profile          |
| `/tellproblem`   | POST   | Submit health issue and get doctor info |
| `/userhistory`   | GET    | View past queries and matched doctors   |

### Doctor Endpoints (`doc.py`)
| Endpoint         | Method | Description                             |
|------------------|--------|-----------------------------------------|
| `/addtodo`       | POST   | Register a new doctor                   |
| `/userlogin`     | POST   | Login and receive JWT token             |
| `/viewalltodo`   | GET    | View all doctor names and specialties   |
| `/profile2`      | GET    | View logged-in doctor profile           |

### Query Matching (`query.py`)
| Endpoint         | Method | Description                             |
|------------------|--------|-----------------------------------------|
| `/addtodo`       | POST   | Process a query and assign a doctor     |

---

## 🧪 Sample Workflow

1. A patient registers using `/addtodo`.
2. The patient logs in and receives a JWT token.
3. The patient submits a problem (e.g., "fever") using `/tellproblem`.
4. The system checks the `doctor` table for keyword match (`dkw`) and stores the result.
5. The patient can view all previous queries and matched doctors via `/userhistory`.

---

## 📌 Database Tables Overview

- **patient**: Stores patient details (name, email, phone, etc.)
- **doctor**: Stores doctor details (name, specialization, keyword, etc.)
- **query**: Stores health issue submissions and matched doctor responses

---

🔭 Further Research & Improvements
💬 Chat-based Messaging between doctors and patients

🤖 AI-based Symptom Diagnosis Assistant

📱 Mobile App Version using Flutter or React Native

🩻 Attach Medical Reports (PDF/Image) in queries

📢 Notification System for real-time responses

🔒 Role-Based Access Control (RBAC) for enhanced security

---

## ✅ Requirements

```bash
pip install Flask flask-mysqldb flask-bcrypt flask-jwt-extended flask-cors
python pro.py
python doc.py
python query.py

![image alt](https://github.com/PritiPrabha/API-Healthcare-system/blob/main/after_login.jpg?raw=true)
