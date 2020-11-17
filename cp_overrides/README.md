# C&P Overrides
This tiny addon allows to override or redifine just some basic html/css/js declarations or customizations. Within this addon custom e-mail templates, pdf reports and general views are getting served as well.

Getting Started
===================================
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See the following notes on how to clone and deploy the project onto gitlab.

### Prerequisites
What things you need to install the software and how to install them?

- You need to have a local docker environment with an installed odoo installation running
- You need to clone this project into the directory wich is getting loaded by the odoo container so you can activate this addon in odoo to work on it.
- You need to deploy your changes within your own (feature/bugfix) branch which initiates a merge request at gitlab.

For example you do the following:

```
cd Desktop/Project-1
git clone git@gitlab.gitgmbh.com:cpgmbh/kms-odoo/v12/addons-int/cp_overrides.git extra-addons
cd extra-addons/cp_overrides
git checkout feature/xyz or bugfix/xyz
make some changes
git add . | git commit -am
git push -u origin feature/xyz or bugfix/xyz
```

If you want to clone a local copy of all submodules within a main module you only have to clone the main repository where the .gitmodules file is located:

```
git clone git@gitlab.gitgmbh.com:cpgmbh/kms-odoo/v12/addons_int.git extra-addons
```


### Installing
Inside odoo go to Apps and remove the default filter setting 'Apps' and search for the addon name.
Just hit the install button to get the addon activated or the actualize button to update the addon with your changes.

Overrides in General
===================================

Following adjustments are made by this addon:
- Adding custom html tags and snippets to the website (Google Site Verification, GTM, custom style sheet for css overrides...)
- Custom field implementation website_description_short
- Adding reference field sale order to purchase order and vice a versa
- Adding the ability to set colors on the work order tiles
- Adding custom barcodes and corresponding print link


### Odoo Backend
views/product_template.xml
- implementing new field website_description_short

views/purchase_order_view.xml
- adding a new field for linking corresponding sale order to a purchase order

views/sale_order.xml
- adding a new field which displays the information about linked purchase orders

views/work_order_view.xml
- adding the ability to set colors on work order tiles


### Website Frontend
views/template.xml
- google site verification custom meta tag added (Row: 6)
- google tag manager code added (Row: 9-11, 38-44)
- trusted shops code implemented (Row: 14-36, 46-59)
- new field website_description_short added (Row: 61-67)


### Reports
reports/product_barcode_template.xml
- adding new print button for customized barcode prints

reports/stock_location_qrcode_template.xml
- adding custom stock location barcode template using an own layout

reports/stock_location_qrcode.xml
- adding definition for new stock location report


Release Notes
===================================

### Version 12.0.0.1 - 	02 May 2019
1. Initial release
    - New custom field website_description_short
    - Adding purchase order information to sales orders an vice a versa
    - Adding colors functionality to work order kanban view

### Version 12.0.0.2 - 	03 September 2019
1. Task - Adding barcode functionality for product and stock location
2. Fix - Qrcode reference to own module name

### Version 12.0.0.3 - 	07 October 2019
1. Fixed - Lots of code optimizations
2. Task - Adding barcode/qrcode print buttons and own templates
3. Task - Adding translation file de.po
4. Fixed - Switching fields zip and city to german order

### Version 12.0.0.4 - 	04 November 2019
1. Task - Implementing custom e-mail templates
2. Fixed - Lots of template adjustments
3. Fixed - Removing/Replacling studio adjustments by code

### Version 12.0.0.5 - 	03 December 2019
1. Task - Refactoring addon name from cp_website_override to cp_overrides
2. Task - Adding ebay description template
3. Fixed - Smaller code issues like removing duplicate ids from within different addons

### Version 12.0.0.6 - 	30 Dezember 2019
1. Task - Adding addional Inventory fields: width, height and depth. Usefull for shippings.
2. Fixed - Renaming website_description_short to description_short (visible in product general settings)
3. Task - Adjusting existing pricerules - adding the possibility to add multiple conditions

### Version 12.0.0.7 - 	29 January 2020
1. [TASK] adding new columns active and id to res.users view (b578cbc38a9d8b84b0466fda0ea80c1a7dbefaff)
2. [UPDATE] adjusting kms ebay template (cb2489ef236d514afe7bb42ffa9515328a0254ad)

### Version 12.0.0.8 - 	24 February 2020
1. [TASK] adding sh_cookie_notice content to addon ()
