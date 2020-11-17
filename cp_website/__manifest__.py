# -*- coding: utf-8 -*-
{
    # Module information
    'name': 'C&P Website',
    'summary': 'Contains general website overrides and customizations.',
    'description': """
C&P Website
     This addon serves default website pages and overrides the default header and footer.
     Please refer to the README.md file. 
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
    'category': 'Website',
    'version': '12.0.1.0',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'portal',
        'website'
    ],

    # always loaded
    'data': [
        'data/aboutus_data.xml',
        'data/contactus_data.xml',
        'data/customer-projects_data.xml',
        'data/elift-pro_data.xml',
        'data/homepage_data.xml',
        'data/how-to-order_data.xml',
        'data/imprint_data.xml',
        'data/jobs_data.xml',
        'data/new-office-furniture_data.xml',
        'data/payment-delivery_data.xml',
        'data/portfolio_data.xml',
        'data/privacy_data.xml',
        'data/renew-office-furniture_data.xml',
        'data/rights-of-widthdrawal_data.xml',
        'data/terms-conditions_data.xml',
        'data/used-office-furniture_data.xml',
        'data/usm-kitos_data.xml',
        'data/website_data.xml',
        'views/website_templates.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
    ],
    'images': ['static/description/icon.png',],

    # Technical
    'installable': True,
    'application': True,
    'auto_install': False
}