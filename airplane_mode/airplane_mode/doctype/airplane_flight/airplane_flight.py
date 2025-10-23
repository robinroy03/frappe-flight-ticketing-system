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

	def on_update(self):
		doc_before_save = self.get_doc_before_save()

		# Check if doc_before_save exists and if gate_number actually changed
		if doc_before_save and doc_before_save.gate_number != self.gate_number:
			frappe.enqueue(
				"airplane_mode.utils.background_jobs.update_gate_in_tickets",
				flight_name=self.name,
				new_gate=self.gate_number,
				queue="short",
				job_name=f"update_gate_for_flight_{self.name}",
			)
