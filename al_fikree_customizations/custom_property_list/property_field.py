import frappe


def get_property_setters():
    return[
        {
            "doctype": "Employee",
            "fieldname": "personal_details",
            "property": "depends_on",
            "property_type": "Data",
            "value": "eval:doc.employment_type;"
            # "value":"eval:doc.employment_type in [\"Labour\", \"Full time\"]"

            
        },       
    ]