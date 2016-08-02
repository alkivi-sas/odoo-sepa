# -*- coding: utf-8 -*-

from openerp import models, fields, api

class sepa_res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    iban = fields.Char(string='International Bank Account Number (IBAN)', size=34)
    bic = fields.Char(string='Bank Identifier Code (BIC)', size=12)
    rum = fields.Char('Référence Unique de Mandat', size=35)
    sepa_name = fields.Char('Name in bank', size=128)

