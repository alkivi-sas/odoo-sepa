# -*- coding: utf-8 -*-

from openerp import models, fields, api

class sepa_res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    iban = fields.Char(string='International Bank Account Number (IBAN)', size=34)
    bic = fields.Char(string='Bank Identifier Code (BIC)', size=12)
    rum = fields.Char(string='Référence Unique de Mandat', size=35)
    sepa_name = fields.Char(string='Name in bank', size=128)
    mandat_creation_date = fields.Datetime(string='Mandant creation date')


class alkivi_sepa(models.Model):
    _name = 'alkivi.sepa'
    _description = 'SEPA Report'

    date = fields.Datetime(string='Mandat creation date')


class alkivi_sepa_line(models.Model):
    _name = 'alkivi.sepa.line'
    _description = 'SEPA Line'

    sepa_id = fields.Many2one('alkivi.sepa', string='SEPA Report Reference',
                        ondelete='cascade', index=True)
    invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
                        ondelete='cascade', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
            related='invoice_id.partner_id', store=True, readonly=True)
