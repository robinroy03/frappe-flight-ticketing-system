import frappe


def update_gate_in_tickets(flight_name, new_gate):
	ticket_names = frappe.get_all(
		"Airplane Ticket",
		filters={
			"flight": flight_name,
			"docstatus": ["!=", 2],
		},
		pluck="name",
	)

	for name in ticket_names:
		try:
			frappe.db.set_value("Airplane Ticket", name, "gate_number", new_gate)
		except Exception as e:
			frappe.log_error(f"Failed to update gate for ticket {name}: {e}", "Gate Update Job")
