import frappe
from frappe.utils.jinja import validate_template
from frappe.utils.pdf import get_pdf
from frappe.www.printview import get_print_style

from erpnext import get_company_currency
from erpnext.accounts.party import get_party_account_currency
from erpnext.accounts.report.general_ledger.general_ledger import execute as get_soa


@frappe.whitelist()
def download_statement(company, customer, from_date, to_date, subject, message):
    statement_dict = {}
    ageing = ""

    # for entry in doc.customers:
    # 	if doc.include_ageing:
    # 		ageing = set_ageing(doc, entry)

    # 	tax_id = frappe.get_doc("Customer", customer).tax_id

    filters = get_common_filters(company, customer, from_date, to_date)

    col, res = get_soa(filters)
    for x in [0, -2, -1]:
        res[x]["account"] = res[x]["account"].replace("'", "")
    if len(res) == 3:
        return

    statement_dict[customer] = get_html(filters, col, res, customer)

    if not bool(statement_dict):
        return False
    else:
        for customer, statement_html in statement_dict.items():
            statement_dict[customer] = get_pdf(statement_html, {"orientation": ""})
        return statement_dict


def get_common_filters(company, customer, from_date, to_date):
    return frappe._dict(
        {
            "company": company,
            "party_type": "Customer",
            "party": [customer],
            "from_date": from_date,
            "to_date": to_date,
        }
    )


def get_html(filters, col, res, customer):
    base_template_path = "frappe/www/printview.html"
    template_path = "erpnext/accounts/doctype/process_statement_of_accounts/process_statement_of_accounts_accounts_receivable.html"

    # if doc.letter_head:
    # 	from frappe.www.printview import get_letter_head

    # 	letter_head = get_letter_head(doc, 0)

    html = frappe.render_template(
        template_path,
        {
            "filters": filters,
            "data": res,
            "report": {"report_name": "General Ledger", "columns": col},
            "ageing": None,
            "letter_head": None,
            "terms_and_conditions": None,
        },
    )

    html = frappe.render_template(
        base_template_path,
        {"body": html, "css": get_print_style(), "title": "Statement For " + customer},
    )
    return html
