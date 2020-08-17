# -*- coding: utf-8 -*-

from odoo import models, fields


class ErtracCompany(models.Model):
    _name = 'ertrac.company'
    _description = "Ertrac Company"

    name = fields.Char(string="Ertrac Company", required=True)

