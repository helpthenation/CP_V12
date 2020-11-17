# -*- coding: utf-8 -*-
{
    # Module information
    'name': 'eBay Connector (DE)',
    'description': """
eBay Connector (DE)
     This addon just overrides the upload image handling of the odoo enterprise addon sale_ebay.
     With the standard module there is an issue bypassing the images via ir.attachments.
     This addon additionally implements a fallback to standard product image if no attachments were found.
     There are also some adjustments regarding required fields coming from eBay Germany rules like required EAN and UPC.
    """,

    # Author
    'author': 'git GmbH',
    'developer': 'Vipin Kumar, Guido Palacios',
    'website': 'https://www.gitgmbh.com',
    'maintainer': 'git GmbH',
    "support": "info@gitgmbh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '12.0.2.0',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'product',
        'sale_ebay',
        'stock',
        'website_sale'
    ],

    # always loaded
    'data': [
        'static/src/xml/web_assets.xml',
        'views/email_template.xml',
        'views/product_view.xml',
        'views/res_config_settings.xml'
    ],

    'demo': [
    ],

    # Technical
    'installable': True,
    'application': True,
    'auto_install': False
}