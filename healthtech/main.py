from fastapi import FastAPI
from healthtech import models
from healthtech.database import engine, Base
from healthtech.routers import patients, doctors, appointments, audit_logs, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Health Tech MVP")

# Routers
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(audit_logs.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Health Tech API is running "}
