import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def create_ticket_allowance(employee, date, number_of_days, ticket_allowance):
    employee_doc = frappe.get_doc('Employee', employee)

    # Ensure both dates are datetime objects
    joining_date = datetime.combine(employee_doc.date_of_joining, datetime.min.time())
    current_date = datetime.strptime(date, '%Y-%m-%d')

    # Calculate years since joining
    years_since_joining = (current_date - joining_date).days // 365

    # Check if ticket allowance is due (every 2 years)
    if years_since_joining < 2 or years_since_joining % 2 != 0:
        frappe.throw('Ticket Allowance can only be applied after every 2 years from joining date.')

    # Create Ticket Allowance record
    doc = frappe.get_doc({
        'doctype': 'Ticket Allowance',
        'employee': employee,
        'date': date,
        'number_of_days': number_of_days,
        'ticket_allowance': ticket_allowance
    })
    doc.insert()

    # Calculate next due date (next 2-year cycle from joining)
    next_due_years = (years_since_joining // 2 + 1) * 2
    next_due_date = joining_date + timedelta(days=next_due_years * 365)

    employee_doc.custom_last_ticket_allowance_date = date
    # employee_doc.custom_ticket_allowance_due_in = 1
    employee_doc.custom_ticket_allowance_due_in = (next_due_date - current_date).days
    employee_doc.save()
    return doc.name