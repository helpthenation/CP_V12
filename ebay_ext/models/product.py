from odoo import api, fields, models, _
import base64
import io
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductImageInherit(models.Model):
    _inherit = 'product.image'
    ebay_image_url = fields.Char(string="Ebay Image URL", store=True)

class ProductTemplateEbay(models.Model):
    _inherit = "product.template"
    add_product_tax_ebay_price = fields.Boolean(readonly=False)
    ebay_fixed_price = fields.Float()

    @api.multi
    def _create_picture_url(self):
        urls = []
        if self.product_image_ids:
            for pro_image in self.product_image_ids:
                image = io.BytesIO(base64.standard_b64decode(pro_image.image))

                files = {'file': ('EbayImage', image)}
                pictureData = {
                    "WarningLevel": "High",
                    "PictureName": pro_image.name
                }
                response = self.ebay_execute('UploadSiteHostedPictures', pictureData, files=files)
                urls.append(response.dict()['SiteHostedPictureDetails']['FullURL'])
                pro_image.write({'ebay_image_url': response.dict()['SiteHostedPictureDetails']['FullURL']})
            return urls
        else:
            attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'product.template'),
                ('res_id', '=', self.id),
                ('mimetype', 'ilike', 'image'),
            ], order="create_date")

            if attachments:
                for att in attachments:
                    image = io.BytesIO(base64.standard_b64decode(att["datas"]))
                    files = {'file': ('EbayImage', image)}
                    pictureData = {
                        "WarningLevel": "High",
                        "PictureName": self.name
                    }
                    response = self.ebay_execute('UploadSiteHostedPictures', pictureData, files=files)
                    urls.append(response.dict()['SiteHostedPictureDetails']['FullURL'])
                self.write({'ebay_image_url': urls})
                return urls

    @api.multi
    def _prepare_non_variant_dict(self):
        item = self._prepare_item_dict()
        # Set default value to UPC
        item['Item']['ProductListingDetails']['UPC'] = 'Nicht zutreffend'
        # Check the length of the barcode field to guess its type.
        if self.barcode:
            if len(self.barcode) == 12 and self.check_encoding(self.barcode, 'upc'):
                item['Item']['ProductListingDetails']['UPC'] = self.barcode
            elif len(self.barcode) == 13 and self.check_encoding(self.barcode, 'ean13'):
                item['Item']['ProductListingDetails']['EAN'] = self.barcode
        return item

    @api.multi
    def _prepare_item_dict(self):
        if self.ebay_sync_stock:
            self.ebay_quantity = max(int(self.virtual_available), 0)
        country_id = self.env['ir.config_parameter'].sudo().get_param('ebay_country')
        country = self.env['res.country'].browse(int(country_id))
        currency_id = self.env['ir.config_parameter'].sudo().get_param('ebay_currency')
        currency = self.env['res.currency'].browse(int(currency_id))
        comp_currency = self.env.user.company_id.currency_id
        item = {
            "Item": {
                "Title": self._ebay_encode(self.ebay_title),
                "PrimaryCategory": {"CategoryID": self.ebay_category_id.category_id},
                "StartPrice": comp_currency._convert(self.ebay_price, currency, self.env.user.company_id,
                                                     fields.Date.today())
                if self.ebay_listing_type == 'Chinese'
                else comp_currency._convert(self.ebay_fixed_price, currency, self.env.user.company_id,
                                            fields.Date.today()),
                "CategoryMappingAllowed": "true",
                "Country": country.code,
                "Currency": currency.name,
                "ConditionID": self.ebay_item_condition_id.code,
                "ListingDuration": self.ebay_listing_duration,
                "ListingType": self.ebay_listing_type,
                "PostalCode": self.env['ir.config_parameter'].sudo().get_param('ebay_zip_code'),
                "Location": self.env['ir.config_parameter'].sudo().get_param('ebay_location'),
                "Quantity": self.ebay_quantity,
                "BestOfferDetails": {'BestOfferEnabled': self.ebay_best_offer},
                "PrivateListing": self.ebay_private_listing,
                "SellerProfiles": {
                    "SellerPaymentProfile": {
                        "PaymentProfileID": self.ebay_seller_payment_policy_id.policy_id,
                    },
                    "SellerReturnProfile": {
                        "ReturnProfileID": self.ebay_seller_return_policy_id.policy_id,
                    },
                    "SellerShippingProfile": {
                        "ShippingProfileID": self.ebay_seller_shipping_policy_id.policy_id,
                    }
                },
            }
        }

        if self.ebay_subtitle:
            item['Item']['SubTitle'] = self._ebay_encode(self.ebay_subtitle)
        picture_urls = self._create_picture_url()
        if picture_urls:
            item['Item']['PictureDetails'] = {'PictureURL': picture_urls}
            if self.env['ir.config_parameter'].sudo().get_param('ebay_gallery_plus'):
                item['Item']['PictureDetails']['GalleryType'] = 'Plus'
        if self.ebay_listing_type == 'Chinese' and self.ebay_buy_it_now_price:
            item['Item']['BuyItNowPrice'] = comp_currency._convert(self.ebay_buy_it_now_price, currency,
                                                                   self.env.user.company_id, fields.Date.today())
        if self.ebay_description and self.ebay_template_id:
            description = self.ebay_template_id._render_template(self.ebay_template_id.body_html, 'product.template',
                                                                 self.id)
            item['Item']['Description'] = '<![CDATA[' + description + ']]>'

        NameValueList = []
        variant = self.product_variant_ids.filtered('ebay_use')
        # We set by default the brand and the MPN because of the new eBay policy
        # That make them mandatory in most category
        item['Item']['ProductListingDetails'] = {'BrandMPN': {'Brand': 'Nicht zutreffend'}}
        item['Item']['ProductListingDetails']['BrandMPN']['MPN'] = 'Nicht zutreffend'
        # If only one variant selected to be published, we don't create variant
        # but set the variant's value has an item specific on eBay
        if len(variant) == 1 \
                and self.ebay_listing_type == 'FixedPriceItem':
            if self.ebay_sync_stock:
                variant.ebay_quantity = max(int(variant.virtual_available), 0)
            item['Item']['Quantity'] = variant.ebay_quantity
            item['Item']['StartPrice'] = variant.ebay_fixed_price
        # We use the attribute to set the attributes linked to computed shipping policies
        # We don't use attributes since this fix has been done in stable release but will be done
        # in master.
        # We don't use the weight attribute due to the fact that eBay handles the English system
        # of measurement which uses Lbs and Oz. Then we cannot just split the weight field.
        ShippingPackageAttributes = [
            'PackageDepth', 'PackageLength', 'PackageWidth', 'WeightMajor',
            'WeightMinor', 'ShippingIrregular', 'ShippingPackage'
        ]
        # If one attribute has only one value, we don't create variant
        # but set the value has an item specific on eBay
        if self.attribute_line_ids:
            for attribute in self.attribute_line_ids:
                if len(attribute.value_ids) == 1:
                    attr_name = attribute.attribute_id.name
                    attr_value = self._ebay_encode(attribute.value_ids.name)
                    # We used the attributes in Odoo to match the Brand and MPN attributes
                    # But since 1st March 2016, eBay separated them from the other attributes
                    if attr_name == 'Hersteller':
                        item['Item']['ProductListingDetails']['BrandMPN']['Brand'] = attr_value
                    elif attr_name == 'Herstelllernummer':
                        item['Item']['ProductListingDetails']['BrandMPN']['MPN'] = attr_value
                    elif attr_name in ShippingPackageAttributes:
                        if 'ShippingPackageDetails' not in item['Item']:
                            item['Item']['ShippingPackageDetails'] = {}
                        item['Item']['ShippingPackageDetails'][self._ebay_encode(attr_name)] = attr_value
                    else:
                        NameValueList.append({
                            'Name': self._ebay_encode(attr_name),
                            'Value': attr_value,
                        })

        # We add the Brand and the MPN at the end of the loop
        # because these attributes are mandatory since 1st March 2016
        # but some eBay site are not taking into account the ProductListingDetails.
        # This avoid to loop in the NameValueList array to ensure that it contains
        # Brand and MPN attributes
        brand_mpn = [
            {'Name': 'Hersteller', 'Value': item['Item']['ProductListingDetails']['BrandMPN']['Brand']},
            {'Name': 'Herstellernummer', 'Value': item['Item']['ProductListingDetails']['BrandMPN']['MPN']}
        ]

        # Set default value to UPC and EAN
        item['Item']['ProductListingDetails']['UPC'] = 'Nicht zutreffend'
        item['Item']['ProductListingDetails']['EAN'] = 'Nicht zutreffend'
        # Override UPC or EAN with barcode value if barcode length matches
        if self.barcode:
            if len(self.barcode) == 12:
                item['Item']['ProductListingDetails']['UPC'] = self.barcode
            elif len(self.barcode) == 13:
                item['Item']['ProductListingDetails']['EAN'] = self.barcode

        NameValueList += brand_mpn
        if NameValueList:
            item['Item']['ItemSpecifics'] = {'NameValueList': NameValueList}
        if self.ebay_category_2_id:
            item['Item']['SecondaryCategory'] = {'CategoryID': self.ebay_category_2_id.category_id}
        if self.ebay_store_category_id:
            item['Item']['Storefront'] = {
                'StoreCategoryID': self.ebay_store_category_id.category_id,
                'StoreCategoryName': self._ebay_encode(self.ebay_store_category_id.name),
            }
            if self.ebay_store_category_2_id:
                item['Item']['Storefront']['StoreCategory2ID'] = self.ebay_store_category_2_id.category_id
                item['Item']['Storefront']['StoreCategory2Name'] = self._ebay_encode(self.ebay_store_category_2_id.name)
        return item

    @api.one
    def create_sale_order(self, transaction):
        if not self.env['sale.order'].search([
            ('client_order_ref', '=', transaction['OrderLineItemID'])]):
            # After 15 days eBay doesn't send the email anymore but 'Invalid Request'.
            # If 2 transactions are synchronized with 2 different buyers with 'Invalid Request',
            # the second buyer information will override the firs one. So we make the search
            # on the ebay_id instead.
            email = transaction['Buyer']['Email']
            if email == "Invalid Request":
                email = False
                partner = self.env['res.partner'].search([
                    ('ebay_id', '=', transaction['Buyer']['UserID'])])
            else:
                partner = self.env['res.partner'].search([
                    ('email', '=', email)])
            if not partner:
                partner = self.env['res.partner'].create({'name': transaction['Buyer']['UserID']})
            if len(partner) > 1:
                partner = partner[0]
            partner_data = {
                'name': transaction['Buyer']['UserID'],
                'ebay_id': transaction['Buyer']['UserID'],
                'email': email,
                'ref': 'eBay',
            }
            if 'BuyerInfo' in transaction['Buyer'] and \
                    'ShippingAddress' in transaction['Buyer']['BuyerInfo']:
                infos = transaction['Buyer']['BuyerInfo']['ShippingAddress']
                partner_data['name'] = infos.get('Name')
                partner_data['street'] = infos.get('Street1')
                partner_data['street2'] = infos.get('Street2')
                partner_data['city'] = infos.get('CityName')
                partner_data['zip'] = infos.get('PostalCode')
                partner_data['phone'] = infos.get('Phone')
                partner_data['country_id'] = self.env['res.country'].search([
                    ('code', '=', infos['Country'])
                ]).id
                state = self.env['res.country.state'].search([
                    ('code', '=', infos.get('StateOrProvince')),
                    ('country_id', '=', partner_data['country_id'])
                ])
                if not state:
                    state = self.env['res.country.state'].search([
                        ('name', '=', infos.get('StateOrProvince')),
                        ('country_id', '=', partner_data['country_id'])
                    ])
                partner_data['state_id'] = state.id

            partner.write(partner_data)
            fp_id = self.env['account.fiscal.position'].get_fiscal_position(partner.id)
            if fp_id:
                partner.property_account_position_id = fp_id
            if self.product_variant_count > 1:
                if 'Variation' in transaction:
                    variant = self.product_variant_ids.filtered(
                        lambda l:
                        l.ebay_use and
                        l.ebay_variant_url.split("vti", 1)[1] ==
                        transaction['Variation']['VariationViewItemURL'].split("vti", 1)[1])
                # If multiple variants but only one listed on eBay as Item Specific
                else:
                    call_data = {'ItemID': self.ebay_id, 'IncludeItemSpecifics': True}
                    resp = self.ebay_execute('GetItem', call_data)
                    name_value_list = resp.dict()['Item']['ItemSpecifics']['NameValueList']
                    if not isinstance(name_value_list, list):
                        name_value_list = [name_value_list]
                    # get only the item specific in the value list
                    attrs = []
                    # get the attribute.value ids in order to get the variant listed on ebay
                    for spec in (n for n in name_value_list if n['Source'] == 'ItemSpecific'):
                        attr = self.env['product.attribute.value'].search(
                            [('name', '=', spec['Value'])])
                        attrs.append(('attribute_value_ids', '=', attr.id))
                    variant = self.env['product.product'].search(attrs).filtered(
                        lambda l: l.product_tmpl_id.id == self.id)
            else:
                variant = self.product_variant_ids[0]
            variant.ebay_quantity_sold = variant.ebay_quantity_sold + int(transaction['QuantityPurchased'])
            if not self.ebay_sync_stock:
                variant.ebay_quantity = variant.ebay_quantity - int(transaction['QuantityPurchased'])
                variant_qty = 0
                if len(self.product_variant_ids.filtered('ebay_use')) > 1:
                    for variant in self.product_variant_ids:
                        variant_qty += variant.ebay_quantity
                else:
                    variant_qty = variant.ebay_quantity
                if variant_qty <= 0:
                    if self.env['ir.config_parameter'].sudo().get_param('ebay_out_of_stock'):
                        self.ebay_listing_status = 'Out Of Stock'
                    else:
                        self.ebay_listing_status = 'Ended'
            sale_order = self.env['sale.order'].create({
                'partner_id': partner.id,
                'state': 'draft',
                'client_order_ref': transaction['OrderLineItemID'],
                'origin': 'eBay' + transaction['TransactionID'],
                'fiscal_position_id': fp_id if fp_id else False,
            })
            if self.env['ir.config_parameter'].sudo().get_param('ebay_sales_team'):
                sale_order.team_id = int(self.env['ir.config_parameter'].sudo().get_param('ebay_sales_team'))
            currency = self.env['res.currency'].search([
                ('name', '=', transaction['TransactionPrice']['_currencyID'])])
            company_id = self.env.user.company_id
            IrDefault = self.env['ir.default']
            if variant.taxes_id:
                taxes_id = variant.taxes_id.ids
            else:
                taxes_id = IrDefault.get('product.template', 'taxes_id', company_id=company_id.id)
            price_unit = currency._convert(
                float(transaction['TransactionPrice']['value']),
                company_id.currency_id, company_id, fields.Date.today())
            if variant.product_tmpl_id.add_product_tax_ebay_price == True:
                amount_all_tax = sum([x.amount for x in self.env['account.tax'].browse(taxes_id) if taxes_id])
                tax_amount = 0
                if amount_all_tax:
                    amount_all_tax = currency._convert(
                        float(amount_all_tax),
                        company_id.currency_id, company_id, fields.Date.today())
                    tax_amount = price_unit - price_unit / (1 + amount_all_tax / 100)

                sol = self.env['sale.order.line'].create({
                    'product_id': variant.id,
                    'order_id': sale_order.id,
                    'name': self.name,
                    'product_uom_qty': float(transaction['QuantityPurchased']),
                    'product_uom': variant.uom_id.id,
                    'price_unit': price_unit - tax_amount,
                    'tax_id': [(6, 0, taxes_id)] if taxes_id else False,
                })
                sol._compute_tax_id()
            else:
                sol = self.env['sale.order.line'].create({
                    'product_id': variant.id,
                    'order_id': sale_order.id,
                    'name': self.name,
                    'product_uom_qty': float(transaction['QuantityPurchased']),
                    'product_uom': variant.uom_id.id,
                    'price_unit': price_unit,
                    'tax_id': [(6, 0, taxes_id)] if taxes_id else False,
                })
                sol._compute_tax_id()

            # create a sales order line if a shipping service is selected
            if 'ShippingServiceSelected' in transaction:
                taxes_id = IrDefault.get('product.template', 'taxes_id', company_id=company_id.id)
                shipping_name = transaction['ShippingServiceSelected']['ShippingService']
                shipping_product = self.env['product.template'].search([('name', '=', shipping_name)])
                if not shipping_product:
                    shipping_product = self.env['product.template'].create({
                        'name': shipping_name,
                        'uom_id': self.env.ref('uom.product_uom_unit').id,
                        'type': 'service',
                        'categ_id': self.env.ref('sale_ebay.product_category_ebay').id,
                    })
                v_price_unit = currency._convert(
                    float(transaction['ShippingServiceSelected']['ShippingServiceCost']['value']),
                    company_id.currency_id, company_id, fields.Date.today())
                if variant.product_tmpl_id.add_product_tax_ebay_price == True:
                    v_amount_all_tax = sum([x.amount for x in self.env['account.tax'].browse(taxes_id) if taxes_id])
                    v_tax_amount = 0
                    if v_amount_all_tax:
                        v_amount_all_tax = currency._convert(
                            float(v_amount_all_tax),
                            company_id.currency_id, company_id, fields.Date.today())
                        v_tax_amount = v_price_unit - (v_price_unit / (1 + v_amount_all_tax / 100))

                    so_line = self.env['sale.order.line'].create({
                        'order_id': sale_order.id,
                        'name': shipping_name,
                        'product_id': shipping_product.product_variant_ids[0].id,
                        'product_uom_qty': 1,
                        'product_uom': self.env.ref('uom.product_uom_unit').id,
                        'price_unit': v_price_unit - v_tax_amount,
                        'tax_id': [(6, 0, taxes_id)] if taxes_id else False,
                        'is_delivery': True,
                    })
                    so_line._compute_tax_id()
                else:
                    so_line = self.env['sale.order.line'].create({
                        'order_id': sale_order.id,
                        'name': shipping_name,
                        'product_id': shipping_product.product_variant_ids[0].id,
                        'product_uom_qty': 1,
                        'product_uom': self.env.ref('uom.product_uom_unit').id,
                        'price_unit': v_price_unit,
                        'tax_id': [(6, 0, taxes_id)] if taxes_id else False,
                        'is_delivery': True,
                    })
                    so_line._compute_tax_id()

            sale_order.action_confirm()
            if 'BuyerCheckoutMessage' in transaction:
                sale_order.message_post(body=_('The Buyer Posted :\n') + transaction['BuyerCheckoutMessage'])
                sale_order.picking_ids.message_post(
                    body=_('The Buyer Posted :\n') + transaction['BuyerCheckoutMessage'])
            if 'ShippingServiceSelected' in transaction:
                sale_order.picking_ids.message_post(
                    body=_('The Buyer Chose The Following Delivery Method :\n') + shipping_name)
            sale_order.action_invoice_create(final=True)

    @api.multi
    @api.onchange('add_product_tax_ebay_price')
    def _onchange_add_ebay_fixed_price(self):
        print(self.add_product_tax_ebay_price)
        if self.add_product_tax_ebay_price == True:
            print("tax adding")
            if self.taxes_id:
                all_amount = sum([x.amount for x in self.taxes_id if self.taxes_id])
                if self.ebay_price:
                    tax_amount = (self.ebay_price * all_amount) / 100
                    print(tax_amount, "tax amount")
                    self.update({'ebay_price': self.ebay_price + tax_amount})
                if self.ebay_buy_it_now_price:
                    tax_amount = (self.ebay_buy_it_now_price * all_amount) / 100
                    self.update({'ebay_buy_it_now_price': self.ebay_buy_it_now_price + tax_amount})
                if self.ebay_fixed_price:
                    tax_amount = (self.ebay_fixed_price * all_amount) / 100
                    self.update({'ebay_fixed_price': self.ebay_fixed_price + tax_amount})
                if self.product_variant_ids:
                    for value in self.product_variant_ids:
                        tax_amount = (value.ebay_fixed_price * all_amount) / 100
                        value.update({'ebay_fixed_price': value.ebay_fixed_price + tax_amount})
        else:
            self._ebay_fixed_price()

    @api.multi
    @api.onchange('ebay_listing_type', 'list_price')
    def _ebay_fixed_price(self):
        if self.ebay_listing_type == 'Chinese':
            self.ebay_buy_it_now_price = self.list_price
            self.ebay_price = self.list_price
        if self.ebay_listing_type == 'FixedPriceItem':
            print(len(self.product_variant_ids), "length")
            if len(self.product_variant_ids) >= 2:
                try:
                    id_record = self._origin.id
                except:
                    id_record = self.id
                if id_record:
                    product_product = self.env['product.product'].search([('product_tmpl_id', '=', id_record)])
                    if product_product:
                        for product in product_product:
                            attribute = product.attribute_value_ids
                            amount = 0
                            for line in attribute:
                                search_attribute_price = self.env['product.template.attribute.value'].search(
                                    [('product_tmpl_id', '=', id_record), ('name', '=', line.name),
                                     ('attribute_id', '=', line.attribute_id.id)])
                                amount = amount + sum(
                                    [price.price_extra for price in search_attribute_price if search_attribute_price])
                            print(amount, "amount")
                            product.write({'ebay_fixed_price': self.list_price + amount})
                    else:
                        if self.product_variant_ids:
                            for value in self.product_variant_ids:
                                value.write({'ebay_fixed_price': value.lst_price})
            else:
                self.write({'ebay_fixed_price': self.list_price})
        self.write({'add_product_tax_ebay_price': False})

    @api.multi
    @api.onchange('ebay_use')
    def _ebay_use_onchange(self):
        if self.ebay_use:
            self._ebay_fixed_price()

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    ebay_variant_listing = fields.Boolean(String="eBay variant")

    @api.model
    def create(self, vals):
        create_data = super(ProductProductInherit, self).create(vals)
        if len(create_data.product_tmpl_id.product_variant_ids) > 1:
            for product in create_data.product_tmpl_id.product_variant_ids:
                attribute = product.attribute_value_ids
                amount = 0
                for line in attribute:
                    search_attribute_price = self.env['product.template.attribute.value'].search(
                        [('product_tmpl_id', '=', create_data.product_tmpl_id.id), ('name', '=', line.name),
                         ('attribute_id', '=', line.attribute_id.id)])
                    amount = amount + sum(
                        [price.price_extra for price in search_attribute_price if search_attribute_price])

                product.write({'ebay_fixed_price': product.product_tmpl_id.list_price + amount})
                self.env.cr.commit()
        else:
            create_data.ebay_fixed_price = create_data.list_price
        return create_data

class ProductAttributeInherit(models.Model):
    _inherit = 'product.attribute'
    ebay_attr_is_variant = fields.Boolean(String="Attribute is a eBay variant")

class ProductTemplateValues(models.Model):
    _inherit = 'product.template.attribute.value'

    @api.model
    def create(self, vals):
        create_data = super(ProductTemplateValues, self).create(vals)
        create_data.product_tmpl_id._ebay_fixed_price()

    @api.multi
    def write(self, vals):
        write_data = super(ProductTemplateValues, self).write(vals)
        self.product_tmpl_id._ebay_fixed_price()
