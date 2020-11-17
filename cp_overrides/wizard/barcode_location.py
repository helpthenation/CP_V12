from itertools import groupby
from odoo import api, fields, models

class BarcodeLocation(models.TransientModel):
    _name = "barcode.location"

    def barcode_creation(self):
        existing_location = self.env['stock.location'].search([('usage','=','internal')])
        for location in existing_location:
            parent_locations = []
            posx = str(location.posx) or ''
            posy = str(location.posy) or ''
            posz = str(location.posz) or ''
            name = str(location.name)

            if location.location_id:
                locationobj = location.location_id
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
            if location_name != '':
                location_name = location_name + '/' + name + '/' + 'G' + posx + '/' + 'F' + posy + '/' + 'E' + posz
            else:
                location_name = name + '/' + 'G' + posx + '/' + 'F' + posy + '/' + 'E' + posz
            location.write({'barcode':location_name})
        return True
