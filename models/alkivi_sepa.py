# -*- coding: utf-8 -*-

import datetime
import logging
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api
from openerp.addons import account

from .tools.PySepaDD import PySepaDD

logger = logging.getLogger(__name__)


class alkivi_sepa(models.Model):
    _name = 'alkivi.sepa'
    _description = 'SEPA Report'

    name = fields.Text(string='Description')
    date = fields.Datetime(string='Mandat creation date', required=True, default=datetime.datetime.today())
    collection_date = fields.Datetime(string='Mandat collection date', required=True, default=lambda self: self._get_collection_date())
    line_ids = fields.One2many('alkivi.sepa.line', 'sepa_id', string="Lines")

    @api.model
    def _get_collection_date(self):
        """
        Set the default collection date at:
        - the 20 of current month
        - ensuring at least 4 days from now
        """
        today = datetime.datetime.today()
        min_interval = datetime.timedelta(days=4)

        wanted_date = today.replace(day = 20)
        if wanted_date - today < min_interval:
            wanted_date = today + min_interval
        return wanted_date

    @api.multi
    def generate_xml(self):
        """Will take all the data and generate a file to download."""
        self.ensure_one()

        config = {
                "name": self.env['ir.values'].get_default('alkivi.sepa.config', 'bank_name'),
                "IBAN": self.env['ir.values'].get_default('alkivi.sepa.config','iban'),
                "BIC": self.env['ir.values'].get_default('alkivi.sepa.config','bic'),
                "batch": True,
                "creditor_id": self.env['ir.values'].get_default('alkivi.sepa.config','creditor_id'),
                "currency": self.env['ir.values'].get_default('alkivi.sepa.config','currency'),
        }
        sepa = PySepaDD(config)

        for line in self.line_ids:
            invoice = line.invoice_id
            partner = line.partner_id

            collection_date = datetime.datetime.strptime(self.collection_date, '%Y-%m-%d %H:%M:%S')
            mandate_date = datetime.datetime.strptime(partner.mandat_creation_date, '%Y-%m-%d %H:%M:%S')

            payment = {
                    "name": partner.sepa_name,
                    "IBAN": partner.iban,
                    "BIC": partner.bic,
                    "amount": int(invoice.amount_total*100),
                    "type": "OOFF",
                    "collection_date": collection_date,
                    "mandate_id": partner.rum,
                    "mandate_date": mandate_date,
                    "description": 'Facture Alkivi {0}'.format(invoice.number),
            }
            sepa.add_payment(payment)

        return sepa.export()

    @api.multi
    def get_xml(self):
        return {
                'type' : 'ir.actions.act_url',
                'url': '/web/binary/download_sepa?id=%s&format=xml'%(self.id),
                'target': 'self',
        }                  


class alkivi_sepa_line(models.Model):
    _name = 'alkivi.sepa.line'
    _description = 'SEPA Line'

    sepa_id = fields.Many2one('alkivi.sepa', string='SEPA Report Reference',
            ondelete='cascade', index=True)
    invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
            ondelete='cascade', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
            related='invoice_id.partner_id', store=True, readonly=True)
    amount_total = fields.Float(related='invoice_id.amount_total',
            store=True, readonly=True)
