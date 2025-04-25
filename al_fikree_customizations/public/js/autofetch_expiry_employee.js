frappe.ui.form.on('Employee', {
    valid_upto: function(frm) {
        update_days_left(frm, 'valid_upto', 'custom_days_left_passport');
        
    },

    emirates_id_expiry_date: function(frm) {
        update_days_left(frm, 'custom_emirates_id_expiry_date', 'custom_emirated_id_expiry_days');

        
    },
    
    on_load: function(frm) {
        if (!frm.doc.__islocal && !frm.doc.__days_updated) {
            update_days_left(frm, 'valid_upto', 'custom_days_left_passport');
            update_days_left(frm, 'custom_emirates_id_expiry_date', 'custom_emirated_id_expiry_days');

            frm.set_value('__days_updated', 1);
            frm.save();
        }

        frm.set_df_property('custom_days_left_passport', 'read_only', 1);
        frm.set_df_property('custom_emirated_id_expiry_days', 'read_only', 1);
        
    },

    // refresh: function(frm) {
    //     update_days_left(frm, 'valid_upto', 'custom_days_left_passport');
    //     update_days_left(frm, 'custom_emirates_id_expiry_date', 'custom_emirated_id_expiry_days');
    //     frm.set_df_property('custom_days_left_passport', 'read_only', 1);
    //     frm.set_df_property('custom_emirated_id_expiry_days', 'read_only', 1);
       
    
    // }
});

function update_days_left(frm, date_field, target_field) {
    if (frm.doc[date_field]) {
        const expiry_date = frappe.datetime.str_to_obj(frm.doc[date_field]);
        const today = new Date();

        const time_diff = expiry_date - today;
        const days_left = Math.ceil(time_diff / (1000 * 60 * 60 * 24));

        frm.set_value(target_field, days_left >= 0 ? days_left : 0);
    } else {
        frm.set_value(target_field, 0);
    }
    
} 


frappe.ui.form.on('Employee', {
    custom_view_history: function(frm) {
        frappe.set_route('List', 'Ticket Allowance', 'Report', {
            employee: frm.doc.name
        });
    }
});
