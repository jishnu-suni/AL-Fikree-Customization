import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from al_fikree_customizations.custom_property_list.custom_field import CUSTOM_FIELD
from al_fikree_customizations.custom_property_list.property_field import get_property_setters


def after_migrate():
    make_property_setters()
    make_employee_fillters()
    make_employee_fillter_office()
    create_custom_fields(CUSTOM_FIELD, ignore_validate=True)
    # create_docs()

def after_install():
    make_property_setters()
    create_custom_fields(CUSTOM_FIELD, ignore_validate=True)
    # create_docs()


def make_property_setters():
    for property_setter in get_property_setters():
        frappe.make_property_setter(property_setter, validate_fields_for_doctype=False)

def make_employee_fillters():
    if not frappe.db.exists("List Filter",{'filter_name':"Labour"}):
        list_doc = frappe.new_doc("List Filter")
        list_doc.filter_name = "Labour"
        list_doc.reference_doctype = "Employee"
        list_doc.filters = '[["Employee","employment_type","=","Labour",false],["Employee","status","=","Active",false]]'
        list_doc.save()
    return True

def make_employee_fillter_office():
    if not frappe.db.exists("List Filter",{'filter_name':"Office Employee"}):
        list_doc_office = frappe.new_doc("List Filter")
        list_doc_office.filter_name = "Office Employee"
        list_doc_office.reference_doctype = "Employee"
        list_doc_office.filters = '[["Employee","employment_type","=","Full-time",false],["Employee","status","=","Active",false]]'
        list_doc_office.save()
    return True




# def create_docs():
#     install_docs = [
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Number",
#             "abbr": "nos",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Cubic Meter",
#             "abbr": "cu m",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Cubic Feet",
#             "abbr": "cu ft",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Square Meter",
#             "abbr": "sq m",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Square Feet",
#             "abbr": "sq ft",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Inch",
#             "abbr": "in",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Meter",
#             "abbr": "m",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Feet",
#             "abbr": "ft",
#         },
#         {
#             "doctype": "Task Unit",
#             "unit_name": "Percentage",
#             "abbr": "%",
#         },
#     ]

#     for d in install_docs:
#         try:
#             frappe.get_doc(d).insert(ignore_if_duplicate=True)
#         except frappe.NameError:
#             pass


def before_uninstall():
    delete_custom_fields(CUSTOM_FIELD)
    delete_property_setters()
    deleteuser_field_setup()


def delete_custom_fields(custom_fields):
    for doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            # only one field
            fields = [fields]

        if isinstance(doctypes, str):
            # only one doctype
            doctypes = (doctypes,)

        for doctype in doctypes:
            frappe.db.delete(
                "Custom Field",
                {
                    "fieldname": ("in", [field["fieldname"] for field in fields]),
                    "dt": doctype,
                },
            )

            frappe.clear_cache(doctype=doctype)



def delete_property_setters():
    field_map = {
        "doctype": "doc_type",
        "fieldname": "field_name",
    }

    for property_setter in get_property_setters():
        for key, fieldname in field_map.items():
            if key in property_setter:
                property_setter[fieldname] = property_setter.pop(key)

        frappe.db.delete("Property Setter", property_setter)



def deleteuser_field_setup():
    field_map = {
        "doctype": "doc_type",
        "fieldname": "field_name",
    }
    user_list = [{
            "doctype": "User",
            "fieldname": "role_profile_name",
            "property": "reqd",
            "property_type": "Check",
            "value": "1"
        }]
    for property_setter in user_list:
        for key, fieldname in field_map.items():
            if key in property_setter:
                property_setter[fieldname] = property_setter.pop(key)

        frappe.db.delete("Property Setter", property_setter)
