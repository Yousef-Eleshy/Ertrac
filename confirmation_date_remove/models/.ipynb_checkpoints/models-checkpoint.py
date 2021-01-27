# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    date_approve = fields.Datetime('Confirmation Date', index=True, copy=False)
