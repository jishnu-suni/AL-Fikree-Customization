import frappe
import subprocess
import sys




@frappe.whitelist()
def after_migrate():
    # update_version()
    try:
        package_names = ["geopy==2.4.1"]
        for p in package_names:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])
            frappe.logger().info(f"Successfully installed {p}")

    except Exception as ex:
        frappe.logger().error(f"An unexpected error occurred: {ex}")



# def update_version():
#     version = get_versions()['qatar_hr']['version']
#     if not frappe.db.exists("Version LIst",version):
#         version_doc = frappe.new_doc("Version LIst")
#         version_doc.version = version
#         version_doc.app  = 'qatar_hr'
#         version_doc.save()

@frappe.whitelist()
def get_versions():
	"""Get versions of all installed apps.

	Example:

	        {
	                "frappe": {
	                        "title": "Frappe Framework",
	                        "version": "5.0.0"
	                }
	        }"""
	versions = {}
	for app in frappe.get_installed_apps(_ensure_on_bench=True):
		app_hooks = frappe.get_hooks(app_name=app)
		versions[app] = {
			"branch": get_app_branch(app),
		}

		if versions[app]["branch"] != "master":
			branch_version = app_hooks.get("{}_version".format(versions[app]["branch"]))
			if branch_version:
				versions[app]["branch_version"] = branch_version[0] + f" ({get_app_last_commit_ref(app)})"

		try:
			versions[app]["version"] = frappe.get_attr(app + ".__version__")
		except AttributeError:
			versions[app]["version"] = "0.0.1"

	return versions


def get_app_branch(app):
    from frappe import _, safe_decode
    import os
    """Returns branch of an app"""
    try:
        with open(os.devnull, "wb") as null_stream:
            result = subprocess.check_output(
                f"cd ../apps/{app} && git rev-parse --abbrev-ref HEAD",
                shell=True,
                stdin=null_stream,
                stderr=null_stream,
            )
        result = safe_decode(result)
        result = result.strip()
        return result
    except Exception:
        return ""
    


def get_app_last_commit_ref(app):
    from frappe import _, safe_decode
    import os
    try:
        with open(os.devnull, "wb") as null_stream:
            result = subprocess.check_output(
                f"cd ../apps/{app} && git rev-parse HEAD --short 7",
                shell=True,
                stdin=null_stream,
                stderr=null_stream,
            )
        result = safe_decode(result)
        result = result.strip()
        return result
    except Exception:
        return ""
