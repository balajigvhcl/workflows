import sys, os
sys.path.append(os.path.abspath(".."))

from models import Base, Employee, Shift
from shift_logic.rota_generator import generate_rota


from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee, Shift
from shift_logic.rota_generator import generate_rota

#app = Flask(__name__)
###
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder="../frontend")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
###
# Database setup
engine = create_engine("sqlite:///rota.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/rota/<int:month>/<int:year>")
def get_rota(month, year):
    session = Session()
    employees = session.query(Employee).all()
    shifts = generate_rota(employees, month, year)

    rota = []
    for s in shifts:
        emp = session.query(Employee).get(s.employee_id)
        rota.append({
            "date": str(s.date),
            "shift_type": s.shift_type,
            "employee": emp.name
        })
    return jsonify(rota)

if __name__ == "__main__":
   #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)


