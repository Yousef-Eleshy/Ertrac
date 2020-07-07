# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class project_fields(models.Model):
#     _name = 'project_fields.project_fields'
#     _description = 'project_fields.project_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class project_fields(models.Model):
    _inherit='account.analytic.line'
    
    region = fields.Selection(
        [('normal', 'Normal'), ('remote', 'Remote')])
    
    work_type = fields.Selection(
        [('branching', 'Branching'), ('path', 'Path'), ('keys', 'Keys')])