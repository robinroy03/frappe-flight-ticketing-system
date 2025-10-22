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
