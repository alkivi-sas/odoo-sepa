# -*- coding: utf-8 -*-
{
    'name': "alkivi_sepa",

    'summary': """
        Use internally to generate SEPA report when generating invoices""",

    'description': """
        Every month, when we generate invoices, it will create a new sepa object,
        with the invoices needed to be in the report.
        To perform that we extended res.partner with extra information such as
        IBAN
        BIC
        RUM (Unique Number assigned by the bank)
        BANK_NAME (If different that its name)
        
    """,

    'author': "Alkivi",
    'website': "https://alkivi.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing & Payments',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
