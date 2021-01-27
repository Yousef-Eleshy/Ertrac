# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    date_approve = fields.Datetime('Confirmation Date', readonly=0, index=True, copy=False)
