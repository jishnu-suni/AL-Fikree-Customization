import frappe
from frappe.model.document import Document

def validate(doc, method):
    # Fetch Labour Payment summary based on Employee and Date Range
    labour_payment_summary = frappe.db.get_all(
        "Labour Payment Summary",
        filters={
            "labour_id": doc.employee,
            "month_start":doc.start_date,
            "month_end": doc.end_date
        },
        fields=["name"]
    )

    total_overtime_amount = 0
    for summary in labour_payment_summary:
        summary_doc = frappe.get_doc("Labour Payment Summary", summary.name)

        for row in summary_doc.labour_attendance_summary_details:
            if row.reference_document == "Overtime Attendance" and row.status == "Unpaid":
                total_overtime_amount += row.payable_amount

                # Mark summary as Paid
                row.status = "Paid"

        summary_doc.save()

    # Add Overtime to Salary Slip earnings if any unpaid amount exists
    if total_overtime_amount > 0:
        doc.append("earnings", {
            "salary_component": "Overtime",
            "amount": total_overtime_amount
        })
