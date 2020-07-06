# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class hrScreen(models.Model):
    
    _name = "hr.screen"
    _inherit = ['mail.thread']
        
    
    current_month = fields.Char(string = "Month" , required = True , default = datetime.now().strftime("%B"))
    ### if it didnot work use .strftime("%B") instead of .month()
    external_employee = fields.Char(string = "Ext. Employee" , required = True)
    external_Department = fields.Char(string = "Ext. Department" , required = True)
    amount = fields.Float(string = "Amount" , store = True)
    tax = fields.Float(string = "Tax" , default = 0.10 , store = True , readonly = True )
    net = fields.Float(string = "NET"  , store = True , compute = '_compute_net_amount')
    notes = fields.Char(string = "Notes")
    
    
    @api.depends('amount','tax')
    def _compute_net_amount(self):
        self.net = (self.amount - (self.amount*self.tax))    
    
    @api.onchange('amount')
    def _on_change_amount(self):
        self.net = (self.amount - (self.amount*self.tax))
    
    
    

