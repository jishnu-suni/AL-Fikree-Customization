frappe.ui.form.on('Employee', {
    custom_fetch_from_salary_structure: function(frm) {
        if (frm.doc.custom_fetch_from_salary_structure) {
            frm.set_df_property('custom_wage', 'read_only', 1);
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Salary Structure Assignment',
                    filters: {
                        employee: frm.doc.name,
                        docstatus: 1
                    },
                    fields: ['salary_structure']
                },
                callback: function(response) {
                    let assignments = response.message;
                    if (assignments.length > 0) {
                        let salary_structure = assignments[0].salary_structure;
                        frappe.call({
                            method: 'frappe.client.get',
                            args: {
                                doctype: 'Salary Structure',
                                name: salary_structure
                            },
                            callback: function(res) {
                                if (res.message && res.message.earnings) {
                                    let total_earnings = 0;
                                    res.message.earnings.forEach(earning => {
                                        total_earnings += earning.amount;
                                    });
                                    let daily_wage = total_earnings / 30;
                                    let custom_wage_for_overtime = daily_wage / 8;
                                    frm.set_value('custom_wage', daily_wage);
                                    frm.set_value('custom_wage_for_overtime', custom_wage_for_overtime);
                                }
                            }
                        });
                    } else {
                        frappe.msgprint(__('Salary structure not assigned'));
                    
                    }
                }
            });
        } else {
            frm.set_df_property('custom_wage', 'read_only', 0);
        }
    }
});
