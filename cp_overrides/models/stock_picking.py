from odoo import fields, models, api

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'
    location_source_id = fields.Many2one('stock.location', 'Storage Location (Source)', related="location_id", readonly="False", help="Fetches the source location of the inventory warehouse.")
