'''
add file churn with the script inside the dirctory 
'''

from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
from datetime import date

class Restapi(http.Controller):    
    @http.route('/pays',type='json',auth='none')
    def churn(self,base_location=None):
        employees = request.env['hr.employee'].sudo().search([])
        rule_id = request.env['hr.salary.rule'].sudo().search([('name','=','Basic Salary')]).id
        date_from = date(2020, 8, 1)
        date_to = date(2020, 8, 31)
        res = []
        for employee in employees:
           total = 0
           domain = [('salary_rule_id','=',rule_id),('employee_id','=',employee.id),('date_from','=',date_from),('date_to','=',date_to)]
           pays = request.env['hr.payslip.line'].sudo().search(domain)
           for pay in pays:
                slip = request.env['hr.payslip'].sudo().search([('id','=',pay.slip_id.id)],limit=1)
                if slip.state == 'verify':
                    total += pay.amount
           employee.write({'tax_base':total})
           res.append({'employee':employee.name,'amount':total})
        return res
            

       