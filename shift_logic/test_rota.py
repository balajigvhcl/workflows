import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee
from shift_logic.rota_generator import generate_rota

def setup_db():
    """Create an in-memory SQLite DB for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_generate_rota_with_employees():
    session = setup_db()
    # Seed employees
    names = ["Balaji", "Thiyaga", "Muthu", "Sathya", "Narayan"]
    for n in names:
        session.add(Employee(name=n))
    session.commit()

    employees = session.query(Employee).all()
    shifts = generate_rota(employees, 8, 2026)

    # Assertions
    assert len(shifts) > 0
    # Ensure weekend nights are paired
    friday_shifts = [s for s in shifts if s.date.weekday() == 4 and s.shift_type == "9PM IST"]
    saturday_shifts = [s for s in shifts if s.date.weekday() == 5 and s.shift_type == "9PM IST"]
    assert len(friday_shifts) == len(saturday_shifts)
    # Ensure no employee gets more than one weekend pair
    weekend_ids = {s.employee_id for s in friday_shifts}
    assert len(weekend_ids) == len(friday_shifts)
