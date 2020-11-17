# -*- coding: utf-8 -*-
{
    # Module information
    'name': 'C&P Overrides',
    'summary': 'Contains general overrides and customizations. Additional extra fields and custom reports were added.',
    'description': """
C&P Overrides 
     This addon contains lots of customizations and overrides in general. Custom fields and reports were added, as well as website adjustments.
     The trusted shop badge and similar website related things (e.g. google tag manager snippet) are added to website and many more.
     Please refer to the README.md file. 
    """,

    # Author
    'author': 'git GmbH',
    'developer': 'Guido Palacios',
    'website': 'https://www.ketchup-mayo-senf.de',
    'maintainer': 'git GmbH',
    "support": "info@gitgmbh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale,Website',
    'version': '12.0.8',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'delivery',
        'mrp',
        'portal',
        'product',
        'purchase',
        'sale',
        'stock',
        'website',
        'website_sale',
        'mrp_workorder'
    ],

    # always loaded
    'data': [
        'data/ir_sequences.xml',
        'templates/product_qrcode.xml',
        'templates/res_company.xml',
        'templates/stock_deliveryslip.xml',
        'templates/stock_location_qrcode.xml',
        'templates/stock_location_qrcode_small.xml',
        'templates/stock_pickingoperations.xml',
        'reports/paperformat.xml',
        'reports/product_qrcode.xml',
        'reports/stock_report.xml',
        'views/delivery.xml',
        'views/email_template.xml',
        'views/product.xml',
        'views/product_producers.xml',
        'views/purchase_order.xml',
        'views/res_company.xml',
        'views/res_config.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'views/website.xml',
        'views/work_order.xml',
        'views/mrp_workorder.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv',
        'static/src/xml/web_assets.xml',
        'wizard/stock_move_location.xml',
        'wizard/pdf_created_message.xml',
        'wizard/pdf_failed_message.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        #'views/demo.xml',
    ],
    'images': ['static/description/icon.png',],

    # Technical
    'installable': True,
    'application': True,
    'auto_install': False,
    "price": 15,
    "currency": "EUR"
}
