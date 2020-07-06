from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class AcountMove(models.Model):
    _inherit = 'account.move'

    contract = fields.Char(string='العقد')



