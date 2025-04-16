

frappe.ui.form.on('Labour Attendance And Overtime', {
    fetch_employees: function(frm) {
        // Validate required fields
        if (!frm.doc.project || !frm.doc.date || !frm.doc.status || !frm.doc.comments) {
            frappe.msgprint(__('Please fill Project, Date, Status,   and Comments before fetching employees.'));
            return;
        }
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Employee',
                filters: {
                    employment_type: 'Labour'
                },
                fields: ['name', 'employee_name']
            },
            callback: function(r) {
                if (r.message) {
                    frm.doc.employee_list = [];

                    const project = frm.doc.project;
                    const status = frm.doc.status;
                    const overtime_hours = frm.doc.overtime_hours;
                    const comments = frm.doc.comments;
                    const custom_is_half_day = frm.doc.custom_is_half_day;

                    const employeeList = r.message;

                    // Use Promise.all to fetch all employee details in parallel
                    const promises = employeeList.map(emp => {
                        return frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                doctype: 'Employee',
                                name: emp.name
                            }
                        }).then(emp_detail => {
                            const assignments = emp_detail.message.custom_project_assigned || [];
                            const is_assigned = assignments.some(a => a.project === project);

                            if (is_assigned) {
                                const row = frm.add_child('employee_list');
                                row.employee = emp.name;
                                row.employee_name = emp.employee_name;
                                row.status = status;
                                row.custom_is_half_day = custom_is_half_day;
                                row.overtime_hours = overtime_hours;
                                row.comments = comments;
                            }
                        });
                    });

                    Promise.all(promises).then(() => {
                        frm.refresh_field('employee_list');
                    });
                }
            }
        });
    }
});
