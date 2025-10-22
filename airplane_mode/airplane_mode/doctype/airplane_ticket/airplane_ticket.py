# Copyright (c) 2025, Robin Roy and contributors
# For license information, please see license.txt

import random

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_add_ons()
		self.calculate_total_amount()

	def calculate_total_amount(self):
		total_add_on_amount = sum(row.amount for row in self.add_ons)
		self.total_amount = int(self.flight_price) + total_add_on_amount
		print("#####\n\n\n#########")
		print(self.total_amount)

	def remove_duplicate_add_ons(self):
		unique = set()
		unique_item = set()
		for row in self.add_ons:
			if row.item not in unique_item:
				unique.add(row)
				unique_item.add(row.item)

		self.add_ons = unique
		print(self.add_ons)

	def on_submit(self):
		if self.status != "Boarded":
			frappe.throw("Status must be 'boarded'. Cannot submit ticket :(")

	def before_insert(self):
		random_int = random.randint(1, 99)
		random_char = random.choice("ABCDE")
		self.seat = f"{random_int}{random_char}"

		self.check_flight_capacity()

	def check_flight_capacity(self):
		flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane_name = flight.airplane

		capacity = frappe.db.get_value("Airplane", airplane_name, "capacity")

		existing_tickets_count = frappe.db.count(
			"Airplane Ticket",
			{
				"flight": self.flight,
				"docstatus": ("!=", 2),  # Exclude docstatus 2 (Cancelled)
			},
		)

		if existing_tickets_count >= capacity:
			frappe.throw(
				f"Cannot create ticket: Flight {self.flight} is already full (Capacity: {capacity})."
			)
