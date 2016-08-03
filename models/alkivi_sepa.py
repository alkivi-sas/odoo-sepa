# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.addons import account

class alkivi_sepa(models.Model):
    _name = 'alkivi.sepa'
    _description = 'SEPA Report'

    name = fields.Text(string='Description')
    date = fields.Datetime(string='Mandat creation date', required=True)


class alkivi_sepa_line(models.Model):
    _name = 'alkivi.sepa.line'
    _description = 'SEPA Line'

    sepa_id = fields.Many2one('alkivi.sepa', string='SEPA Report Reference',
                        ondelete='cascade', index=True)
    invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
                        ondelete='cascade', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
        related='invoice_id.partner_id', store=True, readonly=True)
