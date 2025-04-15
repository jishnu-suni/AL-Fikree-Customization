import frappe
from frappe.model.document import Document

def validate(doc, method):
    ot_and_extra_hours_appending(doc, method)
    append_safe_worker_earning(doc, method)

def append_safe_worker_earning(doc, method):
    safe_worker = frappe.get_all(
        "Safe Worker",
        filters={
            "month_start_date": ["<=", doc.start_date],
            "month_end_date": [">=", doc.end_date],
        },
        fields=["name"]
    )

    if not safe_worker:
        return
    
    safe_worker_doc = frappe.get_doc("Safe Worker", safe_worker[0]["name"])

    for worker in safe_worker_doc.safe_worker_details:
        if worker.employee == doc.employee:
            # Check if "Safe Worker" component already exists
            if any(e.salary_component == "Safe Worker" for e in doc.earnings):
                return  # If exists, exit function without appending
            
            doc.append("earnings", {
                "salary_component": "Safe Worker",
                "amount": worker.amount
            })

    doc.gross_pay = sum(e.amount for e in doc.earnings if e.amount)
    doc.base_gross_pay = sum(e.amount for e in doc.earnings if e.amount)
    doc.gross_year_to_date = sum(e.amount for e in doc.earnings if e.amount)
    doc.total_deduction = sum(d.amount for d in doc.deductions if d.amount)
    doc.net_pay = doc.base_gross_pay - doc.total_deduction
    doc.rounded_total = doc.base_gross_pay - doc.total_deduction
    doc.base_rounded_total = doc.base_gross_pay - doc.total_deduction
    doc.base_net_pay = doc.base_gross_pay - doc.total_deduction
    doc.year_to_date = doc.base_gross_pay - doc.total_deduction
    doc.month_to_date = doc.base_gross_pay - doc.total_deduction


def ot_and_extra_hours_appending(doc, event):
    # Check if 'show_overtime_amount_in_salary_slip' is enabled in Labour Wage Settings
    labour_wage_settings = frappe.get_doc("Labour Wage Settings")

    # Fetch Labour Payment Summary
    labour_payment_summary = frappe.get_all(
        "Labour Payment Summary",
        filters={
            "labour_id": doc.employee,
            "month_start": doc.start_date,
            "month_end": doc.end_date
        },
        fields=["name"]
    )
    
    if not labour_payment_summary:
        doc.earnings = [
            earning for earning in doc.earnings
            if earning.salary_component != "Extra Allowance"
        ]
        existing_salary_components = [earning.salary_component for earning in doc.earnings]
        if "Holiday OT" not in existing_salary_components:
            doc.append("earnings", {"salary_component": "Holiday OT", "amount": 0})

        if "Friday OT" not in existing_salary_components:
            doc.append("earnings", {"salary_component": "Friday OT", "amount": 0})

        doc.gross_pay = sum(e.amount for e in doc.earnings if e.amount)
        doc.base_gross_pay = sum(e.amount for e in doc.earnings if e.amount)
        doc.gross_year_to_date = sum(e.amount for e in doc.earnings if e.amount)
        doc.total_deduction = sum(d.amount for d in doc.deductions if d.amount)
        doc.net_pay = doc.base_gross_pay - doc.total_deduction
        doc.rounded_total = doc.base_gross_pay - doc.total_deduction
        doc.base_rounded_total = doc.base_gross_pay - doc.total_deduction
        doc.base_net_pay = doc.base_gross_pay - doc.total_deduction
        doc.year_to_date = doc.base_gross_pay - doc.total_deduction
        doc.month_to_date = doc.base_gross_pay - doc.total_deduction
    
    # Fetch Labour Attendance And Overtime Summary
    attendance_overtime_summary = frappe.get_all(
        "Labour Attendance And Overtime Summary",
        filters={
            "labour_id": doc.employee,
            "month_start": doc.start_date,
            "month_end": doc.end_date
        },
        fields=["name"]
    )
    
    if not attendance_overtime_summary:
        return
    
    # Fetch overtime details
    ot_amounts = {}
    extra_allowance_total = 0

    extra_allowance_hours = 0
    ot_hours = 0
    
    for summary in attendance_overtime_summary:
        overtime_details = frappe.get_all(
            "Labour Extra Hour And Overtime Details",
            filters={"parent": summary.name},
            fields=["reference_doctype", "reference_document", "date", "hours", "status", "overtime_hours", "custom_extra_hours"]
        )
        for detail in overtime_details:
            if detail.reference_doctype == "Overtime Attendance":
                payable_amount = frappe.db.get_all(
                    "Labour Attendance Summary Details",
                    filters = {"document_no": detail.reference_document},
                    fields = "payable_amount"
                )
                if payable_amount:
                    payable_amount = payable_amount[0]["payable_amount"]
                    ot_type = detail.custom_ot_type  # Assuming a mappindded for OT type
                    if not ot_type:
                        ot_type = "Normal"
                    ot_amounts[ot_type] = ot_amounts.get(ot_type, 0) + (payable_amount * detail.overtime_hours / detail.hours)
                    ot_hours += detail.overtime_hours
                    extra_allowance_total += (payable_amount * detail.custom_extra_hours / detail.hours)
                    extra_allowance_hours += detail.custom_extra_hours

    # Append Extra Allowance if applicable

    # total_earnings = frappe.db.get_value("Salary Structure",doc.salary_structure,"custom_total_earnings")
    holidays = frappe.db.count("Holiday", filters={
        "holiday_date": ["between",(doc.start_date, doc.end_date)]
    })
    total_days = doc.payment_days + holidays
    total_working_days = doc.total_working_days
    # total_earnings = frappe.db.get_value("Salary Structure",doc.salary_structure,"custom_total_earnings")
    salary_structure = frappe.get_doc("Salary Structure", doc.salary_structure)
    total_earnings = sum(
        component.amount for component in salary_structure.earnings if component.amount
    )
    this_month_salary = total_days * (total_earnings/30)
    extra_allowance_hours = extra_allowance_hours
    extra_allowance_amount = (total_earnings/30/8)*extra_allowance_hours
    overtime_amount = (total_earnings/30/8)*ot_hours

    absent_count = frappe.db.count("Attendance", {
        "employee": doc.employee,
        "attendance_date": ["between", [doc.start_date, doc.end_date]],
        "status": "Absent",
        "custom_leave_type": "Absent",
        "docstatus": 1 
    })
    if absent_count:
        deduction_amount = (total_earnings/30)*absent_count
        total_amount_to_paid = this_month_salary + overtime_amount + extra_allowance_amount - deduction_amount
    else:
        total_amount_to_paid = this_month_salary + overtime_amount + extra_allowance_amount

    doc.custom_overtime_hours = ot_hours
    doc.custom_extra_hours = extra_allowance_hours
    doc.custom_total_salary = total_amount_to_paid
    doc.custom_overtime_amount = overtime_amount
    doc.custom_extra_hour_amount = extra_allowance_amount

    # Map OT type to Salary Component

    ot_component_map = {
        row.applicable_days: {
            "salary_component": row.salary_component,
            "wage_rate": row.wage_rate
        }
        for row in labour_wage_settings.overtime_wage
    }
    extra_hours_component = labour_wage_settings.extra_hours_salary_component
    # Get existing salary components
    existing_components = {earning.salary_component for earning in doc.earnings}

# Add earnings rows for OT wage
    for ot_type, amount in ot_amounts.items():
        if ot_type in ot_component_map and amount > 0:
            salary_component = ot_component_map[ot_type]["salary_component"]
            wage_rate = ot_component_map[ot_type]["wage_rate"]
            if salary_component not in existing_components:
                doc.append("earnings", {
                    "salary_component": salary_component,
                    "amount": float(overtime_amount) * float(wage_rate)
                })
    normal_ot = 0
    basic_amount = 0

    for basic in doc.earnings:
        if basic.salary_component == "Basic":
            basic_amount = basic.amount
        if basic.salary_component == "Normal OT":
            normal_ot = basic.amount
    pending_extra_amount = total_amount_to_paid - basic_amount - normal_ot
    
    extra_allowance_total = pending_extra_amount
            
    existing_component = next((e for e in doc.earnings if e.salary_component == extra_hours_component), None)

    if extra_allowance_total > 0:
        if existing_component:
            existing_component.amount = extra_allowance_total
        else:
            doc.append("earnings", {"salary_component": extra_hours_component, "amount": extra_allowance_total})
        

    
    existing_salary_components = [earning.salary_component for earning in doc.earnings]
    if "Holiday OT" not in existing_salary_components:
        doc.append("earnings", {"salary_component": "Holiday OT", "amount": 0})

    if "Friday OT" not in existing_salary_components:
        doc.append("earnings", {"salary_component": "Friday OT", "amount": 0})



    doc.gross_pay = sum(e.amount for e in doc.earnings if e.amount)
    doc.base_gross_pay = sum(e.amount for e in doc.earnings if e.amount)
    doc.gross_year_to_date = sum(e.amount for e in doc.earnings if e.amount)
    doc.total_deduction = sum(d.amount for d in doc.deductions if d.amount)
    doc.net_pay = doc.base_gross_pay - doc.total_deduction
    doc.rounded_total = doc.base_gross_pay - doc.total_deduction
    doc.base_rounded_total = doc.base_gross_pay - doc.total_deduction
    doc.base_net_pay = doc.base_gross_pay - doc.total_deduction
    doc.year_to_date = doc.base_gross_pay - doc.total_deduction
    doc.month_to_date = doc.base_gross_pay - doc.total_deduction