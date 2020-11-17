from odoo import models,fields,_

class IrActionsReportInherit(models.Model):
    _inherit = 'ir.actions.report'
    print_report_name = fields.Char('Print Report Name',translate=True,help="This is the filename of the report going to download. Keep empty to not change the report filename. You can use a python expression with the 'object' and 'time' variables.")
