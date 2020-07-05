# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime



class ProjectTask(models.Model):
    _inherit = 'project.task'

    planned_hours = fields.Float(string='Quantity')

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    machine = fields.Char(string='Machine')
    region = fields.Char(string='Region')
    employee_id = fields.Many2one('hr.employee', "Employee", check_company=True)
    unit_amount = fields.Float(string='Quantity')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    #solved_qty = fields.Float(string ='Solved Qty',store=True)
    rated = fields.Float(string = 'Rate',store = True , compute = '_compute_rate_value')

    @api.depends('qty_delivered','product_uom_qty')
    def _compute_rate_value(self):
        for line in self:
            if line.product_uom_qty == 0 :
                line.rated = 0
            else:
                line.rated = (line.qty_delivered*100)/line.product_uom_qty


    @api.onchange('qty_delivered')
    def _on_change_rate_value(self):
        for line in self:
            if line.product_uom_qty == 0 :
                line.rated = 0
            else:
                line.rated = (line.qty_delivered*100)/line.product_uom_qty


    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        report_invoice_document
        """
        self.ensure_one()
        return {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'rated': self.rated,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }



#    @api.depends('analytic_line_ids.project_id')
#    def _compute_qty_delivered(self):
#        super(SaleOrderLine, self)._compute_qty_delivered()

#        lines_by_timesheet = self.filtered(lambda sol: sol.qty_delivered_method == 'timesheet')
#        domain = lines_by_timesheet._timesheet_compute_delivered_quantity_domain()
#        mapping = lines_by_timesheet.sudo()._get_delivered_quantity_by_analytic(domain)
#        for line in lines_by_timesheet:
#            line.qty_delivered = line.planned_hours

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    rated = fields.Float(string = 'Rate',store = True)

# class AccountMove(models.Model):
#     _inherit = 'account.move'

#     short_date = fields.Char(compute='month_year',store = True)

#     @api.depends('invoice_date')
#     def month_year(self):
#         short_date_val = ''
#         if self.invoice_date:
#             month_name = self.invoice_date.strftime("%b")
#             year = self.invoice_date.year
#             short_date_val = f'{month_name} {year}'
#         self.short_date = short_date_val
