from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class AcountMove(models.Model):
    _inherit = 'account.move'

    contract = fields.Char(string='العقد')
    current = fields.Char(string='جاري')
    pure_amount = fields.Float(string='صافي المستخلص',compute='_pure_amount')

    @api.depends('invoice_line_ids.price_subtotal')
    def _pure_amount(self):
        invoices = self.invoice_line_ids
        total = 0
        for invoice in invoices:
            total += invoice.price_subtotal
        self.pure_amount = total





