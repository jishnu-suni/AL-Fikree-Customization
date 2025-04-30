import frappe
from frappe import _
from hrms.payroll.doctype.payroll_entry.payroll_entry import (
    get_salary_structure,
    get_filter_condition,
    get_joining_relieving_condition,
    get_emp_list,
    remove_payrolled_employees
)
import json
from frappe.utils import cint


# custom_payroll.py

import frappe
from frappe import _
from frappe.desk.reportview import get_filters_cond
from frappe.utils import getdate


@frappe.whitelist()
def custom_fill_employee_details(filters_json):
    filters = frappe.parse_json(filters_json)

    required_keys = ["company", "currency", "payroll_payable_account", "start_date", "end_date"]
    for key in required_keys:
        if key not in filters:
            frappe.throw(f"Missing required key: {key}")

    filters["start_date"] = getdate(filters["start_date"])
    filters["end_date"] = getdate(filters["end_date"])

    cond = get_filter_condition(filters)
    cond += get_joining_relieving_condition(filters["start_date"], filters["end_date"])

    salary_structures = get_salary_structure(
        filters["company"],
        filters["currency"],
        cint(filters.get("salary_slip_based_on_timesheet", 0)),
        filters.get("payroll_frequency") or "Monthly"
    )

    if not salary_structures:
        frappe.throw(_("No active Salary Structures found for given criteria."))

    cond += " and t2.salary_structure IN %(salary_structure)s"
    cond += " and t2.payroll_payable_account = %(payroll_payable_account)s"
    cond += " and %(from_date)s >= t2.from_date"

    emp_list = get_emp_list(
        salary_structures, cond, filters["end_date"], filters["payroll_payable_account"]
    )
    emp_list = remove_payrolled_employees(emp_list, filters["start_date"], filters["end_date"])

    return emp_list


def get_filter_condition(filters):
    cond = ""
    for f in ["company", "branch", "department", "designation"]:
        if filters.get(f):
            cond += f" and t1.{f} = {frappe.db.escape(filters[f])}"
    return cond


def get_joining_relieving_condition(start_date, end_date):
    return f"""
        and ifnull(t1.date_of_joining, '1900-01-01') <= '{end_date}'
        and ifnull(t1.relieving_date, '2199-12-31') >= '{start_date}'
    """


def get_salary_structure(company, currency, timesheet, frequency):
    SalaryStructure = frappe.qb.DocType("Salary Structure")
    query = (
        frappe.qb.from_(SalaryStructure)
        .select(SalaryStructure.name)
        .where(
            (SalaryStructure.docstatus == 1)
            & (SalaryStructure.is_active == "Yes")
            & (SalaryStructure.company == company)
            & (SalaryStructure.currency == currency)
            & (SalaryStructure.salary_slip_based_on_timesheet == timesheet)
        )
    )
    if not timesheet:
        query = query.where(SalaryStructure.payroll_frequency == frequency)
    return query.run(pluck=True)


def get_emp_list(salary_structure, cond, end_date, payroll_payable_account):

    print(cond)
    print(payroll_payable_account)
    return frappe.db.sql(
        f"""
        SELECT DISTINCT t1.name AS employee, t1.employee_name, t1.department, t1.designation
        FROM `tabEmployee` t1, `tabSalary Structure Assignment` t2
        WHERE t1.name = t2.employee
          AND t2.docstatus = 1
          AND t1.status != 'Inactive'
          {cond}
        ORDER BY t2.from_date DESC
        """,
        {
            "salary_structure": tuple(salary_structure),
            "from_date": end_date,
            "payroll_payable_account": payroll_payable_account,
        },
        as_dict=True,
    )


def remove_payrolled_employees(emp_list, start_date, end_date):
    return [
        emp for emp in emp_list
        if not frappe.db.exists(
            "Salary Slip",
            {
                "employee": emp.employee,
                "start_date": start_date,
                "end_date": end_date,
                "docstatus": 1,
            },
        )
    ]

