# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class ProjectTask(models.Model):
    _inherit = 'project.task'

    planned_hours = fields.Float(string='Quantity')
    effective_hours = fields.Float("Hours Spent", digits=(12,4), compute='_compute_effective_hours', compute_sudo=True, store=True, help="Computed using the sum of the task work done.")

    rate_tasks = fields.Float(string = 'Rate Percentage')
    
    @api.depends('timesheet_ids.unit_amount')
    def _compute_effective_hours(self):
        for task in self:
            task.effective_hours = sum(task.timesheet_ids.mapped('unit_amount'))


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    machine = fields.Char(string='Machine')
    region = fields.Char(string='Region')
    employee_id = fields.Many2one('hr.employee', "Employee", check_company=True)
    unit_amount = fields.Float(string='Quantity')
    parent_id = fields.Many2one('project.task', string='Parent Task')
    child_id = fields.Many2one('project.task', string='Child Task')

    @api.model
    def create(self, vals):
        if vals.get('task_id'):
            task = self.env['project.task'].search([('id','=',vals.get('task_id'))])
            if task.parent_id:
                vals['child_id'] = task.id
            else:
                vals['parent_id'] = task.parent_id.id
        return super(AccountAnalyticLine, self).create(vals)

    def write(self, vals):
        if vals.get('task_id'):
            task = self.env['project.task'].search([('id','=',vals.get('task_id'))])
            if task.parent_id:
                vals['child_id'] = task.id
            else:
                vals['parent_id'] = task.parent_id.id
        return super(AccountAnalyticLine, self).write(vals)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
#     task_id = fields.Many2one(
#         'project.task', 'Generated Task',
#         index=True, copy=False, help="Task generated by the sales order item")
#     is_service = fields.Boolean("Is a Service", compute='_compute_is_service', store=True, compute_sudo=True, help="Sales Order item should generate a task and/or a project, depending on the product settings.")
    
    rated = fields.Float(string = 'Rate',store = True , related='task_id.rate_tasks')
    
    product_uom_qty = fields.Float('Quantity', digits=(12,4))
    qty_delivered = fields.Float('Delivered', digits=(12,4))
    qty_invoiced = fields.Float('Invoiced', digits=(12,4))

    
    @api.depends('task_id.rate_tasks')
    def _fetch_rate_tasks(self):
        for line in self:
            if line.task_id:
                line.rated = line.task_id.rate_tasks
    

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','rated')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            if line.rated !=0 and line.invoice_status == 'to invoice':
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included']*(line.rated/100),
                    'price_subtotal': taxes['total_excluded']*(line.rated/100),
                })
            else:
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included']*(line.rated/100),
                    'price_subtotal': taxes['total_excluded']*(line.rated/100),
                })


    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        return {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'rated': self.rated/100,
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




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    rated = fields.Float(string = 'Rate',store = True)
    rated_once_boolean = fields.Boolean(string='Rated Bool',store=True,default=False)
    allowed_amount = fields.Monetary(string='المبلغ المصرح بصرفه',store=True)
    disc = fields.Char(string='الملاحظات',store=True)
    
    quantity = fields.Float('Quantity', digits=(12,4))


    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        res = super(AccountMoveLine, self)._get_price_total_and_subtotal_model(price_unit, quantity, discount, currency, product, partner, taxes, move_type)
        for line in self:
            if line.rated !=0 and line.rated_once_boolean == False:
                line.rated_once_boolean = True
                res['price_subtotal']= res['price_subtotal'] * line.rated
                #res['price_total'] = res['price_total'] * line.rated
        return res