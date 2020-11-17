from odoo import models, fields, api

class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    ebay_enable_ext_stylesheet = fields.Boolean("Enable ext. stylesheet")
    ebay_external_stylesheeturl = fields.Char("Ext. stylesheet URL")

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsInherit, self).get_values()
        res.update(
            ebay_enable_ext_stylesheet = self.env['ir.config_parameter'].sudo().get_param('ebay_ext.ebay_enable_ext_stylesheet'),
            ebay_external_stylesheeturl = self.env['ir.config_parameter'].sudo().get_param('ebay_ext.ebay_external_stylesheeturl'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettingsInherit, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        field1 = self.ebay_enable_ext_stylesheet and self.ebay_enable_ext_stylesheet or False
        field2 = self.ebay_external_stylesheeturl and self.ebay_external_stylesheeturl or False

        param.set_param('ebay_ext.ebay_enable_ext_stylesheet', field1)
        param.set_param('ebay_ext.ebay_external_stylesheeturl', field2)
