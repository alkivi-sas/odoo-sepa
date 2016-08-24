# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp import SUPERUSER_ID

class sepa_config_settings(osv.osv_memory):
    _name = 'alkivi.sepa.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
            'bank_name': fields.char('Our name in bank', size=48),
            'iban': fields.char('Our IBAN', size=48),
            'bic': fields.char('Our BIC', size=48),
            'creditor_id': fields.char('Our Creditor ID', size=48),
            'currency': fields.char('Our currency', size=48),
            'bank_account_id': fields.char('Our Bank Account ID', size=48),
            'journal_id': fields.char('Our Bank Journal ID', size=48),
    }

    def get_default_bank_name(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'bank_name')

    def set_default_bank_name(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'bank_name')

    def get_default_iban(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'iban')

    def set_default_iban(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'iban')

    def get_default_bic(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'bic')

    def set_default_bic(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'bic')

    def get_default_creditor_id(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'creditor_id')

    def set_default_creditor_id(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'creditor_id')

    def get_default_currency(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'currency')

    def set_default_currency(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'currency')

    def get_default_journal_id(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'journal_id')

    def set_default_journal_id(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'journal_id')
    
    def get_default_bank_account_id(self, cr, uid, ids, context=None):
        return self._get_default(cr, uid, ids, context, 'bank_account_id')
    
    def set_default_bank_account_id(self, cr, uid, ids, context=None):
        return self._set_default(cr, uid, ids, context, 'bank_account_id')

    def _get_default(self, cr, uid, ids, context, param_name):
        """Get default value if already defined"""
        ir_values = self.pool.get('ir.values')
        value = ir_values.get_default(cr, uid, 'alkivi.sepa.config', param_name)
        return { param_name: value }

    def _set_default(self, cr, uid, ids, context, param_name):
        """Set default for alkivi.sepa.config"""
        if uid != SUPERUSER_ID and not self.pool['res.users'].has_group(cr, uid, 'base.group_erp_manager'):
            raise openerp.exceptions.AccessError(_("Only administrators can change the settings"))
        config = self.browse(cr, uid, ids[0], context)
        ir_values = self.pool.get('ir.values')
        value = getattr(config, param_name)
        ir_values.set_default(cr, SUPERUSER_ID, 'alkivi.sepa.config', param_name, value)
