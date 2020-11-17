from odoo import models,fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    use_plm_pdf = fields.Boolean(string='Use plm pdf')
