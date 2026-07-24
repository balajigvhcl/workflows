import sys, os
sys.path.append(os.path.abspath(".."))

import datetime
from flask import Flask, jsonify, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Employee, Shift
from shift_logic.rota_generator import generate_rota

# Flask app setup
app = Flask(__name__, static_folder="../frontend")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Database setup
engine = create_engine("sqlite:///rota.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Auto-seed employees if DB is empty
def seed_employees():
    session = Session()
    if session.query(Employee).count() == 0:
        sample_employees = [
            Employee(name="Balaji"),
            Employee(name="Muthu"),
            Employee(name="Thiyagarajan"),
            Employee(name="Narayan"),
            Employee(name="Sathya"),
            Employee(name="Veeresh"),
        ]
        session.add_all(sample_employees)
        session.commit()
        print("Seeded sample employees.")
    session.close()

seed_employees()

# ✅ NEW: Auto-generate rota if no shifts exist
def seed_rota(month=8, year=2026):
    session = Session()
    if session.query(Shift).count() == 0:
        employees = session.query(Employee).all()
        shifts = generate_rota(employees, month, year)
        for s in shifts:
            session.add(s)
        session.commit()
        print(f"Seeded rota for {month}/{year}")
    session.close()

seed_rota()

@app.route("/rota/<int:month>/<int:year>")
def get_rota(month, year):
    session = Session()
    employees = session.query(Employee).all()

    if not employees:
        return jsonify({"error": "No employees found to generate rota."}), 400

    shifts = generate_rota(employees, month, year)

    rota = []
    for s in shifts:
        emp = session.query(Employee).get(s.employee_id)
        rota.append({
            "date": str(s.date),
            "shift_type": s.shift_type,
            "employee": emp.name
        })
    session.close()
    return jsonify(rota)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
