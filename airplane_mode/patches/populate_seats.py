import random

import frappe


def execute():
	"""
	This patch finds all Airplane Tickets that do not have a seat assigned
	and populates the 'seat' field with a random value.
	"""
	tickets_to_update = frappe.get_all("Airplane Ticket", filters={"seat": ("is", "not set")})

	for ticket in tickets_to_update:
		random_int = random.randint(1, 99)
		random_char = random.choice("ABCDE")
		new_seat = f"{random_int}{random_char}"

		frappe.db.set_value("Airplane Ticket", ticket.name, "seat", new_seat)
