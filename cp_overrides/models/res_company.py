from odoo import api, fields, models

class ResCompaneyInherit(models.Model):
    _inherit = "res.company"
    website_logo = fields.Binary(string="Website Logo", attachment=True, readonly=False)
