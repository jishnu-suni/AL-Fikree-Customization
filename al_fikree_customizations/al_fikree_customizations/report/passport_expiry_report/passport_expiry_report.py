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
        {"label": "Passport Number", "fieldname": "passport_number", "fieldtype": "Data", "width": 150},
        {"label": "New Passport Number ", "fieldname": "custom_passport_number_new", "fieldtype": "Data", "width": 200},
        {"label": "Valid Upto", "fieldname": "valid_upto", "fieldtype": "Date", "width": 120},
        {"label": "Number of Days to Expiry", "fieldname": "days_to_expiry", "fieldtype": "Int", "width": 150},
        {"label": "Passport Status", "fieldname": "custom_passport_status", "fieldtype": "Data", "width": 150}
    ]

def get_data():
    today_date = today()

    employees = frappe.get_all("Employee", 
        fields=["name as employee", "employee_name", "passport_number", "custom_passport_number_new", "valid_upto", "custom_passport_status"],
        filters={"valid_upto": ["!=", None]}
    )

    data = []
    for emp in employees:
        days_to_expiry = date_diff(emp.valid_upto, today_date) if emp.valid_upto else 0
        emp.update({"days_to_expiry": days_to_expiry})
        data.append(emp)

    return data