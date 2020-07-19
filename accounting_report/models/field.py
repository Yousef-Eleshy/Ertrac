from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class acounting_report(models.Model):
    _inherit = "account.payment"

    permission_number = fields.Char(string='رقم اذن التوريد')

