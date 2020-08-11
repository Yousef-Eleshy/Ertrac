# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class ParentTaskHeader(models.Model):
    _name = 'project.task.header'
    _description = "Task Header"

    name = fields.Char("Task Header")
    line_ids = fields.One2many('project.task.header.line', 'header_id', "Columns")
    previous = fields.Float("النسب  السابقة المنصرفة")
    new = fields.Float("النسب المستجدة")
    total = fields.Float("إجمالى النسبة المستحقة الصرف")


class ParentTaskHeaderLine(models.Model):
    _name = 'project.task.header.line'
    _description = "Task Header Line"

    header_id = fields.Many2one('project.task.header', "Header")
    name = fields.Char("Head")
    percent = fields.Float("Percent(%)")


class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    task_header_id = fields.Many2one('project.task.header', "Header")
    report_description = fields.Char('الوصف في التقرير')
    
    # Allowing up to 4 decimal places in Quantity
    planned_hours = fields.Float("Planned Hours", digits=(12,4), help='It is the time planned to achieve the task. If this document has sub-tasks, it means the time needed to achieve this tasks and its childs.',tracking=True)


    def print_report(self):
        # Method to print parent tasks ercac report
        task_ids = self.search([('parent_id', '=', False)]).ids
        return self.env.ref('egymentors_ertrack_report.task_ertrack_report').report_action(task_ids)

# Ahmed Salama Code End.
