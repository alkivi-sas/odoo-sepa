# -*- coding: utf-8 -*-
from openerp import http

# class AlkiviSepa(http.Controller):
#     @http.route('/alkivi_sepa/alkivi_sepa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alkivi_sepa/alkivi_sepa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alkivi_sepa.listing', {
#             'root': '/alkivi_sepa/alkivi_sepa',
#             'objects': http.request.env['alkivi_sepa.alkivi_sepa'].search([]),
#         })

#     @http.route('/alkivi_sepa/alkivi_sepa/objects/<model("alkivi_sepa.alkivi_sepa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alkivi_sepa.object', {
#             'object': obj
#         })