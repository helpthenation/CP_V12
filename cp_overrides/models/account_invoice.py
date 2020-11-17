from odoo import fields, models, api,_

class AccountInvoiceInherit(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
        message loaded by default
        """
        self.ensure_one()
        custom_template = self.env.ref('cp_overrides.cp_account_template', False)
        if custom_template:
            template = custom_template
        else:
            template = self.env.ref('account.email_template_edi_invoice', False)
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', False)
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

class TranslateName(models.Model):
    _inherit = "mail.template"
    name = fields.Char('Name', translate=True)

