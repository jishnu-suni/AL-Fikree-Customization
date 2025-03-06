# Copyright (c) 2025, jishnu.suni@buildsuite.io and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe.utils import today, date_diff

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data

def get_columns():
    return [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Emirates ID", "fieldname": "custom_emirates_id", "fieldtype": "Data", "width": 150},
        {"label": "Emirates ID Expiry Date", "fieldname": "custom_emirates_id_expiry_date", "fieldtype": "Date", "width": 150},
        {"label": "Emirates ID Expiry Days", "fieldname": "emirates_id_expiry_days", "fieldtype": "Int", "width": 150}
    ]

def get_data():
    today_date = today()

    employees = frappe.get_all("Employee", 
        fields=["name as employee", "employee_name", "custom_emirates_id", "custom_emirates_id_expiry_date"],
        filters={"custom_emirates_id_expiry_date": ["!=", None]}
    )

    data = []
    for emp in employees:
        expiry_days = date_diff(emp.custom_emirates_id_expiry_date, today_date) if emp.custom_emirates_id_expiry_date else 0
        emp.update({"emirates_id_expiry_days": expiry_days})
        data.append(emp)

    return data
