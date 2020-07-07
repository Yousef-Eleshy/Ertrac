# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class YousefReport(models.AbstractModel):
    _name = 'report.yousef_report.yreport'
    _inherit = 'report.report_xlsx.abstract'