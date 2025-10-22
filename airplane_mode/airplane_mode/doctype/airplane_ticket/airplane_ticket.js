// Copyright (c) 2025, Robin Roy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Airplane Ticket", {
	refresh: function (frm) {
		frm.page.add_action_item(__("Assign Seat"), function () {
			frappe.prompt(
				[
					{
						label: "Seat Number",
						fieldname: "seat",
						fieldtype: "Data",
						reqd: 1,
					},
				],
				function (values) {
					frm.set_value("seat", values.seat);

                    frm.save();
				},
				"Assign Seat",
				"Assign"
			);
		});
	},
});
