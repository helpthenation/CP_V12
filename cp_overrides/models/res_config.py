from odoo import api, fields, models

class WebsiteInherit(models.Model):
    _inherit = 'website'

    cp_is_cookie_notice = fields.Boolean(string="Cookie Notice")
    cp_message = fields.Text(string="Message", translate=True, default="This website uses cookies to ensure you get the best experience on our website.")
    cp_btn_text = fields.Char(string="Button Text", translate=True, default="Got It")
    cp_policy_link_text = fields.Char(string="Policy Link Text", translate=True, default="Learn more")
    cp_policy_url = fields.Char(string="Policy URL")
    cp_position = fields.Selection([
        ('bottom','Banner bottom'),
        ('top','Banner top'),
        ('bottom-left','Floating left'),
        ('bottom-right','Floating right'),
        ('static_top','Banner top (pushdown)'),
    ], string="Position", default='bottom')

class ResConfigSettingsInherit(models.TransientModel):
    _inherit="res.config.settings"

    cp_is_cookie_notice = fields.Boolean(related="website_id.cp_is_cookie_notice", string="Cookie Notice",readonly=False)
    cp_message = fields.Text(related="website_id.cp_message", translate=True, string="Message", readonly=False)
    cp_btn_text = fields.Char(related="website_id.cp_btn_text", translate=True, string="Button Text", readonly=False)
    cp_policy_link_text = fields.Char(related="website_id.cp_policy_link_text", translate=True, string="Policy Link Text", readonly=False)
    cp_policy_url = fields.Char(related="website_id.cp_policy_url", string="Policy URL", readonly=False)
    cp_position = fields.Selection([
        ('bottom','Banner bottom'),
        ('top','Banner top'),
        ('bottom-left','Floating left'),
        ('bottom-right','Floating right'),
        ('static_top','Banner top (pushdown)'),
    ], string="Position", related="website_id.cp_position", readonly=False,)
