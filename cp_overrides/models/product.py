from odoo import api, fields, models, _
import base64
import qrcode
from io import BytesIO
from odoo.exceptions import ValidationError

# ########################################################################################
# TODO: Uncomment this if ecommerce and website_sale is not in use anymore!
#class ProductImage(models.Model):
## Another model then product.image should get used here or inheritance of product.image???
##    _name = 'product.image'
##    _description = 'CP Product Image'
## OR ???
##    _inherit = 'product.image'
#
#    name = fields.Char('Name')
#    image = fields.Binary('Image', attachment=True)
#    product_tmpl_id = fields.Many2one('product.template', 'Related Product', copy=True)
# ########################################################################################

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    _description = "CP Product Template"

    description_short = fields.Html(String="Product Short Description", translate=True, sanitize_attributes=False, help="A short description of the product.")
# ############################################################################################
# TODO: Uncomment this if ecommerce and website_sale is not in use anymore!
#    image_ids = fields.One2many('product.image', 'product_tmpl_id', string='Product Images')
# ############################################################################################
    width = fields.Float(String="Width", help="The width of the product. Important for shipping!")
    height = fields.Float(String="Height", help="The height of the product. Important for shipping!")
    depth = fields.Float(String="Depth", help="The depth of the product. Important for shipping!")
    qr_code = fields.Binary(attachmnet=True)

    @api.multi
    def qr_code_generator(self):
        if self.default_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=1,
            )
            qr.add_data(self.default_code)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_code = base64.b64encode(temp.getvalue())
            self.write({'qr_code' : qr_code})

    @api.onchange('width', 'height', 'depth')
    def _volume_calculation(self):
        self.ensure_one()
        width, height, depth = 0, 0, 0
        if self.width:
            width = self.width
        if self.height:
            height = self.height
        if self.depth:
            depth = self.depth
        self.volume = width * depth * height

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    _description = "CP Product Variants Template"
    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)', 'Internal Reference already exists and must be unique across the database!'),
    ]

    width = fields.Float(String="Width", help="The width of the product. Important for shipping!")
    height = fields.Float(String="Height", help="The height of the product. Important for shipping!")
    depth = fields.Float(String="Depth", help="The depth of the product. Important for shipping!")
    qr_code = fields.Binary(attachmnet=True)

    """
    If the internal reference field is not set in the product, this method will set it automatically.
    """
    @api.model
    def create(self,vals):
        sequence = self.env.ref('cp_overrides.cp_sequence_default_code')
        default_code = vals.get('default_code')
        if not default_code:
            name = sequence.next_by_code(sequence.code)
            vals['default_code'] = name
        return super(ProductProductInherit,self).create(vals)

    @api.constrains('default_code')
    def _check_default_code(self):
        default_code = self.search([('default_code','=',self.default_code)])
        if len(default_code) > 1:
            raise ValidationError(_("Duplicate Record! Internal Reference already exists and must be unique across the database!"))

    @api.multi
    def qr_code_generator(self):
        if self.default_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=1,
            )
            qr.add_data(self.default_code)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_code = base64.b64encode(temp.getvalue())
            self.write({'qr_code' : qr_code})

    @api.onchange('width', 'height', 'depth')
    def _volume_calculation(self):
        self.ensure_one()
        width, height, depth = 0, 0, 0
        if self.width:
            width = self.width
        if self.height:
            height = self.height
        if self.depth:
            depth = self.depth
        self.volume = width * depth * height

#class ProductAttributeInherit(models.Model):
#    _inherit = 'product.attribute'
#
#    @api.multi
#    def name_get(self):
#        if self:
#            return [(value.id, "%s [%s]" % (value.name, value.category_id.name)) for value in self]
