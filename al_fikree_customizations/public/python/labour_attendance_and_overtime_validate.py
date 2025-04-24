import frappe
from frappe import _

def validate_duplicate_attendance(doc, event):
    # If enable_multiple_employee is checked, validate each child employee row
    if doc.enable_multiple_employee:
        if not doc.employee_list or not doc.date:
            return

        for row in doc.employee_list:
            if not row.employee:
                continue
            check_attendance_conflicts(row.employee, doc.date, doc.name, doc.is_half_day)

    # Else, validate single employee entry
    else:
        if not doc.employee or not doc.date:
            return
        check_attendance_conflicts(doc.employee, doc.date, doc.name, doc.is_half_day)


def check_attendance_conflicts(employee_id, attendance_date, current_doc_name, is_half_day_entry):
    employee_name = frappe.db.get_value("Employee", employee_id, "employee_name")

    # Check Labour Attendance with Full Day status already exists
    if not is_half_day_entry:
        existing_full_day_labour = frappe.db.exists(
            "Labour Attendance",
            {
                "employee": employee_id,
                "attendance_date": attendance_date,
                "docstatus": 1,
            }
        )

        if existing_full_day_labour:
            frappe.throw(_(
                f"Labour Attendance already marked as Full Day for employee <b>{employee_name}</b> on <b>{attendance_date}</b> (Doc: {existing_full_day_labour})."
            ))

        # Check Attendance with status other than Half Day exists
        existing_non_half_attendance = frappe.db.exists(
            "Attendance",
            {
                "employee": employee_id,
                "attendance_date": attendance_date,
                "docstatus": 1
            }
        )
        if existing_non_half_attendance:
            frappe.throw(_(
                f"Attendance already marked employee <b>{employee_name}</b> on <b>{attendance_date}</b> (Doc: {existing_non_half_attendance})."
            ))

    # If current doc is half day, check if already 2 half-days exist (Labour or Attendance)
    else:
        existing_full_day_labour = frappe.db.exists(
            "Labour Attendance",
            {
                "employee": employee_id,
                "attendance_date": attendance_date,
                 "status": "Full Day",
                "docstatus": 1,
            }
        )

        if existing_full_day_labour:
            frappe.throw(_(
                f"Labour Attendance already marked as Full Day for employee <b>{employee_name}</b> on <b>{attendance_date}</b> (Doc: {existing_full_day_labour})."
            ))

        # Check Attendance with status other than Half Day exists
        existing_non_half_attendance = frappe.db.exists(
            "Attendance",
            {
                "employee": employee_id,
                "attendance_date": attendance_date,
                "docstatus": 1,
                "status": ["!=", "Half Day"],
            }
        )
        if existing_non_half_attendance:
            frappe.throw(_(
                f"Attendance already marked employee <b>{employee_name}</b> on <b>{attendance_date}</b> (Doc: {existing_non_half_attendance})."
            ))
        # Get all half-day Labour Attendance entries for that day
        half_day_labour_attendances = frappe.get_all(
            "Labour Attendance",
            filters={
                "employee": employee_id,
                "attendance_date": attendance_date,
                "status": "Half Day",
                "docstatus": 1,
            },
            fields=["name"]
        )

        # Get all half-day Attendance entries for that day
        half_day_attendances = frappe.get_all(
            "Attendance",
            filters={
                "employee": employee_id,
                "attendance_date": attendance_date,
                "status": "Half Day",
                "docstatus": 1,
            },
            fields=["name"]
        )

        total_half_days = len(half_day_labour_attendances) + len(half_day_attendances)
        print(total_half_days)
        print(half_day_labour_attendances)
        print(half_day_attendances)
        print(len(half_day_labour_attendances))
        print(len(half_day_attendances))
        # If already 2 half-days are marked, throw error
        if total_half_days >= 2:
            sources = [d["name"] for d in half_day_labour_attendances + half_day_attendances]
            source_list = ", ".join(sources)
            frappe.throw(_(
                f"Only 2 Half Day attendances allowed per day. Existing entries for employee <b>{employee_name}</b> on <b>{attendance_date}</b>: {source_list}."
            ))
