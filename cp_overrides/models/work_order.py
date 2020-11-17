from odoo import fields, models, api


class WorkOrderInherit(models.Model):
    _inherit = 'mrp.workorder'
    color_test = fields.Integer('Color')

    def return_to_from(self):
        self.compute_plm_pdf_img()
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.workorder',
            'res_id': self.id,
            'view_id': self.env.ref('mrp.mrp_production_workorder_form_view_inherit').id,
            'type': 'ir.actions.act_window',
            'context': {}
        }
