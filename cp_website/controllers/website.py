# -*- coding: utf-8 -*-
import base64
import json
import pytz
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
# from odoo.addons.website.controllers.main import Website, WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL

# Home Page
class Website(Website):

    @http.route(auth='public')
    def index(self, data={}, **kwargs):
        super(Website, self).index(**kwargs)
        return http.request.render('website.homepage')
