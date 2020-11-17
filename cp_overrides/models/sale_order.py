from odoo import fields, models, api
from datetime import datetime,timedelta

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    purchase_reference = fields.Many2many('purchase.order', string='Purchase Reference')

    @api.multi
    def get_expected_delivery_date(self):
        """
        Function for calculating the delivery date + 60 days calling from the xml
        """
        for record in self:
            order_date = record.date_order
            delivery_date = order_date + timedelta(days=60)
            print("ORDER DATE ==%s"%order_date)
            print("EXPECTED DATE ====%s"%delivery_date)
            return delivery_date

    @api.multi
    def _get_cart_recovery_template(self):
        """
        Return the cart recovery template record for a set of orders.
        If they all belong to the same website, we return the website-specific template;
        otherwise we return the default template.
        If the default is not found, the empty ['mail.template'] is returned.
        """
        if self.env.ref('cp_overrides.cp_sale_template'):
            return self.env.ref('cp_overrides.cp_sale_template')
        websites = self.mapped('website_id')
        template = websites.cart_recovery_mail_template_id if len(websites) == 1 else False
        template = template or self.env.ref('website_sale.mail_template_sale_cart_recovery', raise_if_not_found=False)
        return template or self.env['mail.template']

    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.ref('cp_overrides.cp_sale_template'):
                template_id = self.env.ref('cp_overrides.cp_sale_template').id
            else:
                template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }