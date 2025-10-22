import frappe


def execute(filters=None):
	columns = [
		{
			"label": "Airline",
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 200,
		},
		{
			"label": "Revenue",
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 150,
		},
	]

	data = []
	airline_revenue_map = {}
	total_revenue = 0

	all_airlines = frappe.get_all("Airline", fields=["name"])
	for airline in all_airlines:
		airline_revenue_map[airline.name] = 0

	submitted_tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"docstatus": 1},
		fields=["name", "flight", "total_amount"],
	)

	flight_names = list(set([t.flight for t in submitted_tickets]))
	if flight_names:
		flight_details = frappe.get_all(
			"Airplane Flight", filters={"name": ["in", flight_names]}, fields=["name", "airplane"]
		)
		flight_to_airplane_map = {f.name: f.airplane for f in flight_details}

		airplane_names = list(set([f.airplane for f in flight_details]))
		if airplane_names:
			airplane_details = frappe.get_all(
				"Airplane", filters={"name": ["in", airplane_names]}, fields=["name", "airline"]
			)
			airplane_to_airline_map = {a.name: a.airline for a in airplane_details}

			for ticket in submitted_tickets:
				flight_name = ticket.flight
				airplane_name = flight_to_airplane_map.get(flight_name)
				airline_name = airplane_to_airline_map.get(airplane_name)

				if airline_name and airline_name in airline_revenue_map:
					airline_revenue_map[airline_name] += ticket.total_amount

	for airline_name, revenue in airline_revenue_map.items():
		data.append({"airline": airline_name, "revenue": revenue})
		total_revenue += revenue

	chart = {
		"type": "donut",
		"data": {
			"labels": [d["airline"] for d in data if d["revenue"] > 0],
			"datasets": [{"values": [d["revenue"] for d in data if d["revenue"] > 0]}],
		},
	}

	summary = [
		{
			"value": total_revenue,
			"label": "Total Revenue",
			"indicator": "Green",
			"datatype": "Currency",
		}
	]

	return columns, data, None, chart, summary
