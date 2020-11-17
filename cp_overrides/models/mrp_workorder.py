from odoo import models, fields


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    view_plm_pdf = fields.Boolean() # Field for know the check box in product template in enabled, then only button plm pdf is enable
    view_plm_image = fields.Boolean() # Field for know the check box in product template in enabled, then only button plm pdf is enable
    use_plm_pdf = fields.Boolean(related='product_id.use_plm_pdf') # Field for know the check box in product template in enabled, then only button plm pdf is enable
    plm_pdf1 = fields.Binary(compute='compute_plm_pdf_img', store=True)
    plm_pdf2 = fields.Binary(compute='compute_plm_pdf_img', store=True)
    plm_pdf3 = fields.Binary(compute='compute_plm_pdf_img', store=True)
    plm_image1 = fields.Binary(compute='compute_plm_pdf_img', store=True)
    plm_image2 = fields.Binary(compute='compute_plm_pdf_img', store=True)
    plm_image3 = fields.Binary(compute='compute_plm_pdf_img', store=True)
    index_value = fields.Integer()

    def compute_plm_pdf_img(self):
        for workorder in self:
            pdfs = self.env['ir.attachment'].search([('res_model', '=', 'product.template'),
                                                     ('mimetype', '=', 'application/pdf'),
                                                     ('res_id', '=', workorder.product_id.product_tmpl_id.id)], limit=3)
            workorder.plm_pdf1 = pdfs[0].datas if len(pdfs) > 0 else False
            workorder.plm_pdf2 = pdfs[1].datas if len(pdfs) > 1 else False
            workorder.plm_pdf3 = pdfs[2].datas if len(pdfs) > 2 else False

            jpegs = self.env['ir.attachment'].search([('res_model', '=', 'product.template'),
                                                      ('mimetype', '=', 'image/jpeg'),
                                                      ('res_id', '=', workorder.product_id.product_tmpl_id.id)], limit=3)
            workorder.plm_image1 = jpegs[0].datas if len(jpegs) > 0 else False
            workorder.plm_image2 = jpegs[1].datas if len(jpegs) > 1 else False
            workorder.plm_image3 = jpegs[2].datas if len(jpegs) > 2 else False
