# -*- coding: utf-8 -*-
from odoo import http

# class PmMvp(http.Controller):
#     @http.route('/pm_mvp/pm_mvp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pm_mvp/pm_mvp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pm_mvp.listing', {
#             'root': '/pm_mvp/pm_mvp',
#             'objects': http.request.env['pm_mvp.pm_mvp'].search([]),
#         })

#     @http.route('/pm_mvp/pm_mvp/objects/<model("pm_mvp.pm_mvp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pm_mvp.object', {
#             'object': obj
#         })