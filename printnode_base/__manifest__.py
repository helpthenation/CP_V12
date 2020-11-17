# Copyright 2019 VentorTech OU
# License OPL-1.0 or later.

{
    'name': 'Odoo direct print',
    'summary': 'Print any reports or shipping labels directly to any local, Wi-Fi or Bluetooth printer without downloading PDF or ZPL!',
    'version': '12.0.1.2.0',
    'category': 'Tools',
    "images": ["static/description/images/image1.gif"],
    'author': 'VentorTech',
    'website': 'https://ventor.tech',
    'support': 'support@ventor.tech',
    'license': 'OPL-1',
    'live_test_url': 'https://odoo.ventor.tech/',
    'price': 199.00,
    'currency': 'EUR',
    'depends': [
        'base_setup',
        'web',
        'stock',
        'delivery',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/printnode_views.xml',
        'data/printnode_data.xml',
        'wizard/printnode_report_abstract_wizard.xml',
    ],
    'installable': True,
    'application': False,
}
