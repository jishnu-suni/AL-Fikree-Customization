frappe.ui.form.on("Payroll Entry", {
    onload: function (frm) {
        // Hide the "Get Employees" button
        setTimeout(() => {
            document.querySelectorAll('.btn.btn-default.ellipsis').forEach(btn => {
                if (btn.innerText.trim() === "Get Employees") {
                    btn.style.display = "none";
                }
            });
        }, 500);
    },
    custom_fetch_employee: function (frm) {
        let filters = {
            company: frm.doc.company,
            branch: frm.doc.branch,
            department: frm.doc.department,
            designation: frm.doc.designation,
            currency: frm.doc.currency,
            payroll_payable_account: frm.doc.payroll_payable_account,
            salary_slip_based_on_timesheet: frm.doc.salary_slip_based_on_timesheet,
            payroll_frequency: frm.doc.payroll_frequency,
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date,
        };

        frappe.call({
            method: "al_fikree_customizations.public.python.payroll_entry.custom_fill_employee_details",
            args: {
                filters_json: JSON.stringify(filters),
            },
            freeze: true,
            callback: function (r) {
                if (r.message) {
                    frm.clear_table("employees");
                    r.message.forEach(emp => {
                        let row = frm.add_child("employees");
                        row.employee = emp.employee;
                        row.employee_name = emp.employee_name;
                        row.department = emp.department;
                        row.designation = emp.designation;
                    });
                    frm.set_value("number_of_employees", r.message.length);
                    frm.refresh_field("employees");
                    frm.refresh_field("number_of_employees");
                }
            },
        });
        frm.save();
    },
});
