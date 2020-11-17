from odoo import api, fields, models, _
import base64
import io
from odoo.exceptions import ValidationError
import logging

class ProducerList(models.Model):
    _name = "cp_product_producer"
    _description = "Producer description via odoo attribute values"
    name = fields.Char()
    description = fields.Html(string="Description")

class ProductAttributeInherit(models.Model):
    _inherit = 'product.attribute'
    enable_product_producer = fields.Boolean()

class ProductAttributeValueInherit(models.Model):
    _inherit = 'product.attribute.value'
    producer = fields.Many2one('cp_product_producer')
    enable_product_producer = fields.Boolean()
