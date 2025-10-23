// Copyright (c) 2025, Robin Roy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Shop", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Shop', {
    refresh: function(frm) {
        frm.set_query('shop_type', function() {
            return {
                filters: {
                    'enabled': 1 
                }
            };
        });
    }
});