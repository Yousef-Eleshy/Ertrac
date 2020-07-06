# -*- coding: utf-8 -*-
# from odoo import http


# class AccountCheck(http.Controller):
#     @http.route('/account_check/account_check/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_check/account_check/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_check.listing', {
#             'root': '/account_check/account_check',
#             'objects': http.request.env['account_check.account_check'].search([]),
#         })

#     @http.route('/account_check/account_check/objects/<model("account_check.account_check"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_check.object', {
#             'object': obj
#         })
