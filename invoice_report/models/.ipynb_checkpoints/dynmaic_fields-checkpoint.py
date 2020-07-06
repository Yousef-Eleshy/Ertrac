from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class AcountMove(models.Model):
    _inherit = 'account.move'

    contract = fields.Char(string='العقد')

class IvoiceLine(models.Model):
    _inherit = 'account.move.line'

    allowed_amount = fields.Monetary(string='المبلغ المصرح بصرفه',store=True)
    disc = fields.Char(string='الملاحظات',store=True)
