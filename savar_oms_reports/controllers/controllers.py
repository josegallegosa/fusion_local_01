# -*- coding: utf-8 -*-
# from odoo import http


# class ReportTransfers(http.Controller):
#     @http.route('/savar_oms_reports/savar_oms_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/savar_oms_reports/savar_oms_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('savar_oms_reports.listing', {
#             'root': '/savar_oms_reports/savar_oms_reports',
#             'objects': http.request.env['savar_oms_reports.savar_oms_reports'].search([]),
#         })

#     @http.route('/savar_oms_reports/savar_oms_reports/objects/<model("savar_oms_reports.savar_oms_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('savar_oms_reports.object', {
#             'object': obj
#         })
