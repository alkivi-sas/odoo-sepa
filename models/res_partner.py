# -*- coding: utf-8 -*-

import re
import logging

from openerp import models, fields, api

logger = logging.getLogger(__name__)

class sepa_res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    iban = fields.Char(string='International Bank Account Number (IBAN)', size=34)
    bic = fields.Char(string='Bank Identifier Code (BIC)', size=12)
    rum = fields.Char(string='Référence Unique de Mandat', size=35)
    sepa_name = fields.Char(string='Name in bank', size=128)
    mandat_creation_date = fields.Datetime(string='Mandant creation date')

    @api.multi
    def can_sepa(self):
        """
        A res.partner can sepa if the following fields are set:
        - iban
        - bic
        - rum
        - sepa_name
        - mandat_creation_date
        """

        self.ensure_one()
        return (self.iban or self.bic or self.rum
                or self.sepa_name or self.mandat_creation_date)


    @api.constrains('iban')
    def _check_description(self):
        """
        From Wikipedia
        - Enlever les caractères indésirables (espaces, tirets)
        - Supprimer les 4 premiers caractères et les replacer à la fin du compte
        - Remplacer les lettres par des chiffres au moyen d'une table de conversion (A=10, B=11, C=12 etc.)
        - Diviser le nombre ainsi obtenu par 97.
        - Si le reste n'est pas égal à 1 l'IBAN est incorrect : Modulo de 97 égal à 1
        """

        for record in self:
            iban = self.iban

            # Enlever les caractères indésirables (espaces, tirets)
            iban = '{0}'.format(iban).translate(None, ' -')
            logger.debug('IBAN check step 1: {0}'.format(iban))

            # Supprimer les 4 premiers caractères et les replacer à la fin du compte
            iban_beg = iban[0:4]
            iban_end = iban[4:]
            iban = '{0}{1}'.format(iban_end, iban_beg)
            logger.debug('IBAN check step 2: {0}'.format(iban))

            # Remplacer les lettres par des chiffres au moyen d'une table de conversion (A=10, B=11, C=12 etc.)
            digits = ""
            for ch in iban.upper():
                if ch.isdigit():
                    digits += ch
                else:
                    digits += str(ord(ch) - ord("A") + 10)
            logger.debug('IBAN check step 3: {0}'.format(digits))

            # Modulo = 1
            check = long(digits) % 97
            logger.debug('IBAN check step 4: {0}'.format(check))

            if check != 1:
                raise ValidationError('Wrong IBAN {0}'.format(self.iban))
