# Copyright (c) 2025, Robin Roy and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from frappe.website.website_generator import WebsiteGenerator


# class AirplaneFlight(Document):
# 	def on_submit(self):
# 		frappe.db.set_value(self.doctype, self.name, "status", "Completed")

# 	# def get_page_info(self):
# 	# 	return {
# 	# 		"title": self.name,
# 	# 		"route": f"/flights/{self.name}",
# 	# 	}

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status = "Completed"

	# def on_refresh(self):

	def on_update(self):
		print("waiting\n\n\n\n")
		frappe.log(f"\n\n\n\nUpdating gate number for flight {self.name} to {self.gate_number}")
		frappe.enqueue(
			"airplane_mode.utils.background_jobs.update_gate_in_tickets",
			flight_name=self.name,
			new_gate=self.gate_number,
			queue="short",
			at_front=True,
			job_name=f"update_gate_for_flight_{self.name}",
		)
