from odoo import api, fields, models
class MessageWizard(models.TransientModel):
    _name = 'message.wizard'
    message = fields.Char('Message', required=True,readonly="True")
    
class WizardMessage(models.TransientModel):
    _name = 'wizard.message'
    message = fields.Char('Message', required=True,readonly="True")

