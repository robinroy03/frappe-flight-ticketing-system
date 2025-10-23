import frappe
from frappe.utils import today


def send_rent_reminders():
	settings = frappe.get_single("Airport Shop Settings")
	if not settings.enable_rent_reminders:
		print("Rent reminders are disabled in settings.")
		return

	shops_to_remind = frappe.get_all(
		"Shop",
		filters={
			"status": "Occupied",
			"contract_expiry_date": (">=", today()),
		},
		fields=["name", "shop_name", "tenant_name", "tenant_email", "rent_amount"],
	)

	if not shops_to_remind:
		print("No occupied shops found to remind.")
		return

	email_subject = "Gentle Reminder: Shop Rent Due Soon"

	for shop in shops_to_remind:
		if not shop.tenant_email:
			print(f"Skipping shop {shop.shop_name} ({shop.name}) - Missing tenant email.")
			continue

		message = f"""
Dear {shop.tenant_name or "Tenant"},

This is a friendly reminder that the rent of {frappe.utils.fmt_money(shop.rent_amount)} for your shop '{shop.shop_name}' (Shop ID: {shop.name}) is due by 3rd of the month.

Please ensure the payment is made on time.

If you have made the payment already kindly ignore this mail.

Thank you,
Airport Authority
"""
		try:
			frappe.sendmail(
				recipients=shop.tenant_email,
				subject=email_subject,
				message=message,
				now=True,
			)
			print(f"Rent reminder sent for shop {shop.name} to {shop.tenant_email}")
		except Exception as e:
			print(f"Failed to send reminder for shop {shop.name}: {e}")
