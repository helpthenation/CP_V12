from odoo import fields, models, api
import base64
import qrcode
from io import BytesIO

class StockLocationInherit(models.Model):
    _inherit = 'stock.location'
    qr_code = fields.Binary(attachmnet=True)

    @api.multi
    def create_qrcode(self, vals):
        posx = str(vals.get('posx') or self.posx)
        posy = str(vals.get('posy') or self.posy)
        posz = str(vals.get('posz') or self.posz)
        name = vals.get('name') or self.name
        parent_locations = []
        location_id = vals.get('location_id') or self.location_id.id or False
        if location_id:
            locationobj = self.env['stock.location'].browse(location_id)
        else:
            locationobj = False
        while locationobj is not False:
            if locationobj.location_id:
                parent_locations.append(locationobj.name)
                locationobj = locationobj.location_id
            else:
                locationobj = False
                break
        location_name = ''
        reverse = parent_locations[::-1]
        for o in reverse:
            if location_name != '':
                location_name = location_name + '/' + o
            else:
                location_name = o
        print(parent_locations)
        vals['barcode'] = location_name + '/' + name
        return True

    @api.model
    def create(self, vals):
        self.create_qrcode(vals)
        location_obj = super(StockLocationInherit, self).create(vals)
        return location_obj

    @api.multi
    def write(self, vals):
        self.create_qrcode(vals)
        locationobj = super(StockLocationInherit, self).write(vals)
        return locationobj

    @api.multi
    def qr_generator(self):
        if self.barcode:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=1,
            )
            qr.add_data(self.barcode)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_code = base64.b64encode(temp.getvalue())
            self.write({'qr_code': qr_code})