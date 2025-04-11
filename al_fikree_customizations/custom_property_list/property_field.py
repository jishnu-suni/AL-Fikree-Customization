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
        {
            "doctype": "Labour Attendance And Overtime",
            "fieldname": "status",
            "property": "options",
            "property_type": "Text",
            "value": "\nFull Day\nHalf Day\nAbsent\nMedical\nSick\nLeave",
        } 
    ]