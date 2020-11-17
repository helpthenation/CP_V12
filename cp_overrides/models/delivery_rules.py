from odoo import api, fields, models, _
import base64
import io
from odoo.exceptions import ValidationError, UserError
import logging
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp


class DeliveryMethodRule(models.Model):
    _inherit = "delivery.price.rule"

    condition_extra = fields.Selection([('or', 'or'), ('and', 'and')], string="Condition")
    variable_extra = fields.Selection(
        [('weight', 'Weight'), ('volume', 'Volume'), ('wv', 'Weight * Volume'), ('price', 'Price'),
         ('quantity', 'Quantity')], required=True, default='weight')
    operator_extra = fields.Selection([('==', '='), ('<=', '<='), ('<', '<'), ('>=', '>='), ('>', '>')], required=True,
                                      default='<=')
    max_value_extra = fields.Float('Maximum Value', required=True)
    add_additional_condition = fields.Boolean()

    # list_base_price_extra = fields.Float(string='Sale Base Price', digits=dp.get_precision('Product Price'), required=True,
    #                                default=0.0)
    # list_price_extra = fields.Float('Sale Price', digits=dp.get_precision('Product Price'), required=True, default=0.0)
    # variable_factor_extra = fields.Selection(
    #     [('weight', 'Weight'), ('volume', 'Volume'), ('wv', 'Weight * Volume'), ('price', 'Price'),
    #      ('quantity', 'Quantity')], 'Variable Factor', required=True, default='weight')

    @api.multi
    @api.onchange('add_additional_condition')
    def _onchange_add_additional_condition(self):
        if self.add_additional_condition == False:
            self.condition_extra = False
            self.variable_extra = False
            self.operator_extra = False
            self.max_value_extra = False


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def _get_price_from_picking(self, total, weight, volume, quantity):
        price = 0.0
        criteria_found = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity}
        for line in self.price_rule_ids:
            test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
            test2 = safe_eval(line.variable_extra + line.operator_extra + str(line.max_value_extra), price_dict)
            print("************************TEST***********************%s,%s" % (test, test2))
            if line.condition_extra == 'and':
                if test and test2:
                    price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                    criteria_found = True
                    break
                print("LINE CONDITION ======%s" % line.condition_extra)
            elif line.condition_extra == 'or':
                if test or test2:
                    price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                    criteria_found = True
                    break
            else:
                if test:
                    price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                    criteria_found = True
                    break

        if not criteria_found:
            raise UserError(_("No price rule matching this order; delivery cost cannot be computed."))

        return price
