import sys, os
#sys.path.append(os.path.abspath("../2.Database models"))
sys.path.append(os.path.abspath(".."))  # go up one level to project root
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee
#from rota_generator import generate_rota
#from 3_Shift_logic.rota_generator import generate_rota
from shift_logic.rota_generator import generate_rota

# Connect to the same DB
engine = create_engine("sqlite:///rota.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add sample employees if not already present
if session.query(Employee).count() == 0:
    names = ["Balaji", "Thiyaga", "Muthu", "Sathya", "Narayan"]
    for n in names:
        session.add(Employee(name=n))
    session.commit()

employees = session.query(Employee).all()

# Generate rota for August 2026
shifts = generate_rota(employees, 8, 2026)

# Print results
#for s in shifts[:20]:  # show first 20 entries
#    print(f"{s.date} - {s.shift_type} - Employee {s.employee_id}")
# Print results with names
for s in shifts[:20]:  # show first 20 entries
    emp = session.query(Employee).get(s.employee_id)
    print(f"{s.date} - {s.shift_type} - {emp.name}")

