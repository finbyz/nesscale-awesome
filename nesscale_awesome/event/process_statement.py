import frappe


@frappe.whitelist()
def send_process_statement(process_statement, customer, email, from_date, to_date):
    process_statement_doc = frappe.get_doc(
        "Process Statement Of Accounts", process_statement
    )
    copy_process_statement_doc = frappe.copy_doc(process_statement_doc)
    copy_process_statement_doc.enable_auto_email = 0
    copy_process_statement_doc.sender = ""
    copy_process_statement_doc.__newname = f"{from_date}-{to_date}-{customer}"
    copy_process_statement_doc.from_date = from_date
    copy_process_statement_doc.to_date = to_date
    copy_process_statement_doc.customers = []
    copy_process_statement_doc.append(
        "customers", dict(customer=customer, billing_email=email)
    )
    res = copy_process_statement_doc.insert(ignore_permissions=True)
    from erpnext.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts import (
        send_emails,
    )

    send_emails(res.name)
    frappe.delete_doc("Process Statement Of Accounts", res.name, force=True)
    frappe.msgprint("Statement Queued")
    return True
