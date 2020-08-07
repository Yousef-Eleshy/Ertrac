from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class AcountMove(models.Model):
    _inherit = 'account.move'

    contract = fields.Char(string='العقد')
    current = fields.Char(string='جاري')
    pure_amount = fields.Float(string='صافي المستخلص',compute='_pure_amount')
    total_line = fields.Float(string='total',compute='_compute_total')
    pure = fields.Float(string='pure',compute='_compute_total')
    ten_perc = fields.Float(string='ten perc',compute='_compute_total')
    total_machine_rent = fields.Float(string='ten perc',compute='_compute_total')

    @api.depends('invoice_line_ids.price_subtotal','invoice_line_ids')
    def _pure_amount(self):
        invoices = self.invoice_line_ids
        total = 0
        self.pure_amount = total
        self._compute_total()
        
    @api.depends('invoice_line_ids')
    def _compute_total(self):
        total = 0
        products_start = 1
        products_end = 0
        machine_rent_start  = 0
        total_machine_rent = 0
        invoices = self.invoice_line_ids
        for i in range(0,len(invoices)):
            if invoices[i].name ==  'خصم ضمان اعمال% 10':
                products_end = i
            if invoices[i].name ==  'خصم ايجار الماكينات':
                machine_rent_start = i + 1
            
        for i in range(products_start,products_end):
            total += invoices[i].price_subtotal
        for i in range(machine_rent_start,len(invoices)):
            total_machine_rent += invoices[i].price_subtotal
        
        self.total_machine_rent = total_machine_rent
        self.total_line = total
        self.ten_perc = self.total_line * 0.10
        self.pure = self.total_line - self.ten_perc
        self.pure_amount = self.pure - self.total_machine_rent  
        
        
            
            
            





