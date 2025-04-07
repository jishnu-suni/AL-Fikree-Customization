# Copyright (c) 2025, jishnu.suni@buildsuite.io and contributors
# For license information, please see license.txt

# import frappe



import frappe
from frappe.utils import getdate, flt

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 100},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "OT Hours", "fieldname": "ot_hours", "fieldtype": "Float", "width": 100},
        {"label": "Extra Hours", "fieldname": "extra_hours", "fieldtype": "Float", "width": 100},
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 150},
        {"label": "Comments", "fieldname": "comments", "fieldtype": "Data", "width": 200}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("employee"):
        conditions += f" AND laos.labour_id = '{filters.get('employee')}'"
    if filters.get("project"):
        conditions += f" AND lod.project_id = '{filters.get('project')}'"
    
    records = frappe.db.sql(f'''
        SELECT lod.date, laos.labour_id AS employee, emp.employee_name, lod.project_id AS project, 
               SUM(lod.overtime_hours) AS ot_hours, SUM(lod.custom_extra_hours) AS extra_hours,
               (SELECT status FROM `tabLabour Extra Hour And Overtime Details` WHERE reference_doctype='Labour Attendance' 
               AND date = lod.date AND parent = laos.name LIMIT 1) AS status,
               (SELECT comments FROM `tabLabour Extra Hour And Overtime Details` WHERE reference_doctype='Labour Attendance' 
               AND date = lod.date AND parent = laos.name LIMIT 1) AS comments
        FROM `tabLabour Attendance And Overtime Summary` laos
        JOIN `tabLabour Extra Hour And Overtime Details` lod ON lod.parent = laos.name
        JOIN `tabEmployee` emp ON emp.name = laos.labour_id
        WHERE lod.date BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}'
        {conditions}
        GROUP BY lod.date, laos.labour_id, emp.employee_name, lod.project_id
        ORDER BY lod.date ASC''', as_dict=True)
    
    holidays = get_holidays(filters.get('from_date'), filters.get('to_date'))
    all_dates = {record["date"] for record in records} | set(holidays)
    
    sorted_data = []
    for date in sorted(all_dates):
        holiday_status = "Holiday" if date in holidays else ""
        matched_records = [record for record in records if record["date"] == date]
        
        if not matched_records:
            sorted_data.append({
                "date": date,
                "status": holiday_status,
                "ot_hours": 0,
                "extra_hours": 0,
                "project": "",
                "comments": ""
            })
        else:
            for record in matched_records:
                record["status"] = holiday_status or record["status"] or ""
                salary = get_employee_salary(record["employee"]) if "employee" in record else 0
                record["ot_amount"] = calculate_amount(salary, record["ot_hours"])
                record["extra_hour_amount"] = calculate_amount(salary, record["extra_hours"])
                sorted_data.append(record)
    
    return sorted_data

def get_holidays(from_date, to_date):
    return frappe.get_all("Holiday", filters={"holiday_date": ["between", [from_date, to_date]]}, pluck="holiday_date")

def get_employee_salary(employee):
    salary_structure_assignment = frappe.get_value("Salary Structure Assignment", {"employee": employee}, "salary_structure")
    if salary_structure_assignment:
        return frappe.get_value("Salary Structure", salary_structure_assignment, "custom_total_earnings")
    return 0

def calculate_amount(salary, hours):
    return flt((flt(salary) / 30 / 8) * flt(hours)) if salary else 0
