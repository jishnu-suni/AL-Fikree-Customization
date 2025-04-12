import frappe

def create_attendance_for_leave(doc,event):
    if not doc.enable_multiple_employee:
        # check_attendance_already_marked =  frappe.db.get_all("Labour Attendance",filters = {"employee":doc.employee,"attendance_date":doc.date})
        if doc.status:
            if doc.status in ["Medical","Sick"]:
                attendance_status = "On Leave"
                create_leave_attendance(doc.employee,doc.date,attendance_status,doc.status,doc.name)
            if doc.status in ["Leave","Absent"]:
                attendance_status = "Absent"
                create_leave_attendance(doc.employee,doc.date,attendance_status,doc.status,doc.name)
    else:
        for employee in doc.employee_list:
            # check_attendance_already_marked =  frappe.db.get_all("Labour Attendance",filters = {"employee":employee.employee,"attendance_date":doc.date})
            if employee.status:   
                if employee.status in ["Medical","Sick"]:
                    attendance_status = "On Leave"
                    create_leave_attendance(employee.employee,doc.date,attendance_status,employee.status,doc.name)  
                if employee.status in ["Leave","Absent"]:
                    attendance_status = "Absent"
                    create_leave_attendance(employee.employee,doc.date,attendance_status,employee.status,doc.name)  


def create_leave_attendance(employee,date,attendance_status,status,reference):
	leave_attendance = frappe.get_doc({
		"doctype": "Attendance",
		"employee": employee,
		"attendance_date": date,  # Map date to attendance_date
		"status": attendance_status,
        "custom_leave_type":status,
		"custom_reference_labour_attendance_and_overtime":reference,
	})
	leave_attendance.insert(ignore_permissions=True)
	leave_attendance.submit()


def on_cancel(doc,event):
    # Cancel Labour Attendance
    labour_attendance_list = frappe.get_all(
        "Attendance",
        filters={"custom_reference_labour_attendance_and_overtime": doc.name},
        fields=["name"]
    )
    for la in labour_attendance_list:
        labour_attendance = frappe.get_doc("Attendance", la.name)
        if labour_attendance.docstatus == 1:  # Ensure it's submitted before canceling
            labour_attendance.cancel()