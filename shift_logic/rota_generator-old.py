import datetime
from models import Shift

def generate_rota(employees, month, year):
    if not employees: # safety check
        raise ValueError("Employee list is empty. Cannot generate rota.")
    shifts = []
    start_date = datetime.date(year, month, 1)
    days_in_month = (datetime.date(year, month+1, 1) - start_date).days if month < 12 else 31

    #shift_types = ["morning", "afternoon"]
    shift_types = ["6AM IST", "1PM IST"]
    #weekend_night = "night"
    weekend_night = "9PM IST"

    emp_index = 0
    for day in range(days_in_month):
        date = start_date + datetime.timedelta(days=day)
        weekday = date.weekday()

        if weekday in [4, 5]:  # Fri/Sat night shift
            assigned = employees[emp_index % len(employees)]
            shifts.append(Shift(date=date, shift_type=weekend_night, employee_id=assigned.id))
            emp_index += 1
        else:
            for st in shift_types:
                assigned = employees[emp_index % len(employees)]
                shifts.append(Shift(date=date, shift_type=st, employee_id=assigned.id))
                emp_index += 1
    return shifts
