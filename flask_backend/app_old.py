from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee, Shift, Leave
from rota_generator import generate_rota

app = Flask(__name__)
engine = create_engine("sqlite:///rota.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    month, year = data["month"], data["year"]
    session = Session()
    employees = session.query(Employee).all()
    shifts = generate_rota(employees, month, year)
    for s in shifts:
        session.add(s)
    session.commit()
    return jsonify({"status": "rota generated"})

@app.route("/rota", methods=["GET"])
def rota():
    session = Session()
    shifts = session.query(Shift).all()
    return jsonify([{"date": s.date.isoformat(), "shift": s.shift_type, "employee": s.employee_id} for s in shifts])

@app.route("/leave", methods=["POST"])
def leave():
    data = request.json
    session = Session()
    leave = Leave(employee_id=data["employee_id"], date=data["date"], approved=False)
    session.add(leave)
    session.commit()
    return jsonify({"status": "leave requested"})

@app.route("/approve_leave/<int:leave_id>", methods=["POST"])
def approve_leave(leave_id):
    session = Session()
    leave = session.query(Leave).get(leave_id)
    leave.approved = True
    session.commit()
    return jsonify({"status": "leave approved"})
