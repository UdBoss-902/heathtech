# HealthTech Scheduling System

A secure healthcare scheduling platform built with **FastAPI** and **PostgreSQL**.  
This MVP supports patients, doctors, appointments, and audit logs with full authentication and role‑based access control.

---

## 🚀 Features
- **Patients**: CRUD operations, scoped access to their own appointments.
- **Doctors**: CRUD operations, scoped access to assigned appointments.
- **Appointments**: Create, view, and manage appointments with role restrictions.
- **Audit Logs**: Track every action with user context (who did what, when).
- **Authentication**: JWT‑based login with password hashing (bcrypt).
- **Role‑Based Access**: Patients, Doctors, Admins each see only what they should.

---

## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Auth**: JWT via python‑jose
- **Password Hashing**: Passlib (bcrypt)
- **Validation**: Pydantic v2 (`EmailStr` support)

---

## 📦 Installation

Clone the repo:
git clone https://github.com/UdBoss-902/heathtech.git
cd healthtech

install dependencies:
pip install -r requirements.txt

run server:
uvicorn healthtech.main:app --reload --port 9000

