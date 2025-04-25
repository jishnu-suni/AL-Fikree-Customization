frappe.ui.form.on('Employee', {
    date_of_joining: function(frm) {
        calculate_ticket_allowance_due(frm);
    },

    custom_last_ticket_allowance_date: function(frm) {
        calculate_ticket_allowance_due(frm);
    },

    custom_ticket_allowance_due_in: function(frm) {
        toggle_add_ticket_allowance_visibility(frm);
    },
    on_load: function(frm) {
        if (!frm.doc.__islocal && !frm.doc.__ticket_due_updated) {
            calculate_ticket_allowance_due(frm);
            frm.set_value('__ticket_due_updated', 1);
            frm.save();
        }

        frm.set_df_property('custom_ticket_allowance_due_in', 'read_only', 1);
        // calculate_ticket_allowance_due(frm);
        // frm.set_df_property('custom_ticket_allowance_due_in', 'read_only', 1);
    },

});

function calculate_ticket_allowance_due(frm) {
    if (frm.doc.date_of_joining) {
        let reference_date = frm.doc.custom_last_ticket_allowance_date ? new Date(frm.doc.custom_last_ticket_allowance_date) : new Date(frm.doc.date_of_joining);
        let current_date = new Date();

        // Calculate next due date (2 years after reference date)
        let due_date = new Date(reference_date);
        due_date.setFullYear(reference_date.getFullYear() + 2);

        // Calculate days left for due
        let days_left = Math.ceil((due_date - current_date) / (1000 * 60 * 60 * 24));

        // Update custom_ticket_allowance_due_in field
        frm.set_value('custom_ticket_allowance_due_in', days_left >= 0 ? days_left : 0);

        // Control visibility
        toggle_add_ticket_allowance_visibility(frm);
    }
}

function toggle_add_ticket_allowance_visibility(frm) {
    frm.toggle_display('custom_add_ticket_allowance', frm.doc.custom_ticket_allowance_due_in === 0);
}




frappe.ui.form.on('Employee', {
    custom_add_ticket_allowance: function(frm) {
        frappe.prompt([
            {
                fieldname: 'date',
                label: 'Date',
                fieldtype: 'Date',
                reqd: 1
            },
            {
                fieldname: 'number_of_days',
                label: 'Number of Days',
                fieldtype: 'Int',
                reqd: 1
            },
            {
                fieldname: 'ticket_allowance',
                label: 'Ticket Allowance',
                fieldtype: 'Currency',
                reqd: 1
            }
        ],
        function(values) {
            frappe.call({
                method: 'al_fikree_customizations.public.python.create_ticket_allowance.create_ticket_allowance',
                args: {
                    employee: frm.doc.name,
                    date: values.date,
                    number_of_days: values.number_of_days,
                    ticket_allowance: values.ticket_allowance
                },
                callback: function(response) {
                    if (!response.exc) {
                        frappe.msgprint(__('Ticket Allowance record created successfully'));
                    }
                }
            });
        },
        __('Add Ticket Allowance'),
        __('Save'));
    }
});
