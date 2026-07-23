import datetime
from models import Shift

def generate_rota(employees, month, year):
    if not employees:  # safety check
        raise ValueError("Employee list is empty. Cannot generate rota.")

    shifts = []
    start_date = datetime.date(year, month, 1)
    days_in_month = (datetime.date(year, month+1, 1) - start_date).days if month < 12 else 31

    shift_types = ["6AM IST", "1PM IST"]
    weekend_night = "9PM IST"

    emp_index = 0
    used_weekend_employees = set()  # track who already got a weekend night assignment

    for day in range(days_in_month):
        date = start_date + datetime.timedelta(days=day)
        weekday = date.weekday()

        if weekday == 4:  # Friday
            # pick next employee who hasn't had a weekend night yet
            while employees[emp_index % len(employees)].id in used_weekend_employees:
                emp_index += 1
            assigned = employees[emp_index % len(employees)]
            used_weekend_employees.add(assigned.id)

            # assign both Friday and Saturday night to same employee
            shifts.append(Shift(date=date, shift_type=weekend_night, employee_id=assigned.id))
            saturday = date + datetime.timedelta(days=1)
            if saturday.month == month:  # ensure Saturday is still in same month
                shifts.append(Shift(date=saturday, shift_type=weekend_night, employee_id=assigned.id))

            emp_index += 1

        elif weekday not in [5]:  # skip Saturday because it's already handled with Friday
            for st in shift_types:
                assigned = employees[emp_index % len(employees)]
                shifts.append(Shift(date=date, shift_type=st, employee_id=assigned.id))
                emp_index += 1

    return shifts
