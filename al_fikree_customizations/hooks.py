app_name = "al_fikree_customizations"
app_title = "Al Fikree Customizations"
app_publisher = "jishnu.suni@buildsuite.io"
app_description = "Customize Erpnext and Frappe"
app_email = "jishnu.suni@buildsuite.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/al_fikree_customizations/css/al_fikree_customizations.css"
# app_include_js = "/assets/al_fikree_customizations/js/al_fikree_customizations.js"

# include js, css files in header of web template
# web_include_css = "/assets/al_fikree_customizations/css/al_fikree_customizations.css"
# web_include_js = "/assets/al_fikree_customizations/js/al_fikree_customizations.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "al_fikree_customizations/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "al_fikree_customizations.utils.jinja_methods",
# 	"filters": "al_fikree_customizations.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "al_fikree_customizations.install.before_install"
# after_install = "al_fikree_customizations.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "al_fikree_customizations.uninstall.before_uninstall"
# after_uninstall = "al_fikree_customizations.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "al_fikree_customizations.utils.before_app_install"
# after_app_install = "al_fikree_customizations.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "al_fikree_customizations.utils.before_app_uninstall"
# after_app_uninstall = "al_fikree_customizations.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "al_fikree_customizations.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"al_fikree_customizations.tasks.all"
# 	],
# 	"daily": [
# 		"al_fikree_customizations.tasks.daily"
# 	],
# 	"hourly": [
# 		"al_fikree_customizations.tasks.hourly"
# 	],
# 	"weekly": [
# 		"al_fikree_customizations.tasks.weekly"
# 	],
# 	"monthly": [
# 		"al_fikree_customizations.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "al_fikree_customizations.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "al_fikree_customizations.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "al_fikree_customizations.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["al_fikree_customizations.utils.before_request"]
# after_request = ["al_fikree_customizations.utils.after_request"]

# Job Events
# ----------
# before_job = ["al_fikree_customizations.utils.before_job"]
# after_job = ["al_fikree_customizations.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"al_fikree_customizations.auth.validate"
# ]


app_include_js = [
    "/assets/al_fikree_customizations/js/ticket_allowance_creation.js",
    "/assets/al_fikree_customizations/js/autofetch_expiry_employee.js",
    "/assets/al_fikree_customizations/js/wage_from_salary_structure.js",
]


fixtures = ["Custom DocPerm","Workspace"]

after_install = "al_fikree_customizations.install.after_install"
after_migrate = [
    "al_fikree_customizations.api.after_migrate",
    "al_fikree_customizations.install.after_migrate",
]


doc_events = {
    "Salary Slip": {
        "validate": "al_fikree_customizations.public.python.salary_slip_ot_calculation.validate",
    },
    "Labour Attendance And Overtime": {
        "on_submit": "al_fikree_customizations.public.python.labour_leave_marking.create_attendance_for_leave",
        "on_cancel": "al_fikree_customizations.public.python.labour_leave_marking.on_cancel",
        "validate": "al_fikree_customizations.public.python.labour_attendance_and_overtime_validate.validate_duplicate_attendance",
    },
}


