// Copyright (c) 2025, Robin Roy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airline", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Airline', {
    refresh: function(frm) {
        if (frm.doc.website) {
         frm.add_web_link(frm.doc.website, 'Go to Website');
        }
    }
});