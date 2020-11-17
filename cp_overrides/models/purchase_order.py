from odoo import fields, models, api

class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"
    sale_reference = fields.Many2one("sale.order", string="Sale Order Reference")

    @api.multi
    def add_sale_reference(self):
        if self.sale_reference:
            sale_order = self.env['sale.order'].browse([self.sale_reference.id])
            if sale_order:
                sale_order.write({'purchase_reference':[(4,self.id)]})

    @api.model
    def create(self, vals):
        res = super(PurchaseOrderInherit, self).create(vals)
        res.add_sale_reference()
        return res

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrderInherit, self).write(vals)
        self.add_sale_reference()
        return res
