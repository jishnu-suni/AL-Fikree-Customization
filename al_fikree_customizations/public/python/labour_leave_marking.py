import frappe


def create_attendance_for_leave(doc, event):
    if not doc.enable_multiple_employee:
        # check_attendance_already_marked =  frappe.db.get_all("Labour Attendance",filters = {"employee":doc.employee,"attendance_date":doc.date})
        if doc.status:
            if doc.status in ["Medical", "Sick"]:
                if doc.is_half_day:
                    attendance_status = "Half Day"
                    leave_type = "Sick Leave"
                    create_leave_attendance(
                        doc.employee,
                        doc.date,
                        attendance_status,
                        doc.status,
                        doc.name,
                        leave_type=leave_type,
                    )
                else:
                    attendance_status = "On Leave"
                    create_leave_attendance(
                        doc.employee, doc.date, attendance_status, doc.status, doc.name
                    )
            if doc.status in ["Leave", "Absent"]:
                if doc.is_half_day:
                    attendance_status = "Half Day"
                    leave_type = "Leave Without Pay"
                    create_leave_attendance(
                        doc.employee,
                        doc.date,
                        attendance_status,
                        doc.status,
                        doc.name,
                        leave_type=leave_type,
                    )
                else:
                    attendance_status = "Absent"
                    create_leave_attendance(
                        doc.employee, doc.date, attendance_status, doc.status, doc.name
                    )
    else:
        for employee in doc.employee_list:
            # check_attendance_already_marked =  frappe.db.get_all("Labour Attendance",filters = {"employee":employee.employee,"attendance_date":doc.date})
            if employee.status:
                if employee.status in ["Medical", "Sick"]:
                    if employee.is_half_day:
                        attendance_status = "Half Day"
                        leave_type = "Sick Leave"
                        create_leave_attendance(
                            doc.employee,
                            doc.date,
                            attendance_status,
                            doc.status,
                            doc.name,
                            leave_type=leave_type,
                        )
                    else:
                        attendance_status = "On Leave"
                        create_leave_attendance(
                            employee.employee,
                            doc.date,
                            attendance_status,
                            employee.status,
                            doc.name,
                            leave_type=None,
                        )
                if employee.status in ["Leave", "Absent"]:
                    if employee.is_half_day:
                        attendance_status = "Half Day"
                        leave_type = "Leave Without Pay"
                        create_leave_attendance(
                            employee.employee,
                            doc.date,
                            attendance_status,
                            employee.status,
                            doc.name,
                            leave_type=None,
                        )
                    else:
                        attendance_status = "Absent"
                        create_leave_attendance(
                            employee.employee,
                            doc.date,
                            attendance_status,
                            employee.status,
                            doc.name,
                            leave_type=None,
                        )


def create_leave_attendance(
    employee, date, attendance_status, status, reference, leave_type=None
):
    leave_attendance = frappe.get_doc(
        {
            "doctype": "Attendance",
            "employee": employee,
            "attendance_date": date,  # Map date to attendance_date
            "status": attendance_status,
            "custom_leave_type": status,
            "custom_reference_labour_attendance_and_overtime": reference,
            "leave_type": leave_type,
        }
    )
    leave_attendance.insert(ignore_permissions=True)
    leave_attendance.submit()


def on_cancel(doc, event):
    print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
    # Cancel Labour Attendance
    attendance_list = frappe.get_all(
        "Attendance",
        filters={"custom_reference_labour_attendance_and_overtime": doc.name},
        fields=["name"],
    )
    for la in attendance_list:
        attendance = frappe.get_doc("Attendance", la.name)
        if attendance.docstatus == 1:  # Ensure it's submitted before canceling
            attendance.cancel()

    labour_attendance_list = frappe.get_all(
        "Labour Attendance",
        filters={"custom_reference_labour_attendance_and_overtime": doc.name},
        fields=["name"],
    )
    for la in labour_attendance_list:
        labour_attendance = frappe.get_doc("Labour Attendance", la.name)
        if labour_attendance.docstatus == 1:  # Ensure it's submitted before canceling
            labour_attendance.cancel()

    overtime_attendance_list = frappe.get_all(
        "Overtime Attendance",
        filters={"custom_reference_labour_attendance_and_overtime": doc.name},
        fields=["name"],
    )
    for la in overtime_attendance_list:
        overtime_attendance = frappe.get_doc("Overtime Attendance", la.name)
        if overtime_attendance.docstatus == 1:  # Ensure it's submitted before canceling
            overtime_attendance.cancel()
