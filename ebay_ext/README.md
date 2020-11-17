# eBay connector

This addon implements an interface to synchronize your products with ebay.com. All what is needed is an valid ebay seller account and maybe some fancy template to be ready to sell your products on ebay.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See the following notes on how to clone and deploy the project onto gitlab.

### Prerequisites

What things you need to install the software and how to install them?

- You need to have a local odoo test installation up & running (docker, hyper-v or any other virtualisation software) 
- You need to clone this project into the directory wich is getting loaded by the odoo container so you can activate this addon in odoo to work on it.
- You need to deploy your changes within your own (feature/bugfix) branch which initiates a merge request at gitlab.

For example you do the following:

```
cd Desktop/Project-1
git clone git@gitlab.gitgmbh.com:cpgmbh/kms-odoo/v12/addons-int/ebay_ext.git extra-addons
cd extra-addons/ebay_ext
git checkout feature/xyz or bugfix/xyz
make some changes
git add . | git commit -am
git push -u origin feature/xyz or bugfix/xyz
```

NOTE: This module is a submodule of the addons_int.git main repository:
If you want to clone a local copy of all submodules within the main module you only have to clone the main repository where the .gitmodules file is located:

```
git clone --recurse-submodules git@gitlab.gitgmbh.com:cpgmbh/kms-odoo/v12/addons_int.git extra-addons
```


### Installing

Inside odoo go to Apps and search for the addon name ebay_ext.
Just hit the install button to get the addon activated or the actualize button to update the addon with your changes.


## Overrides in General

- Version 1.0:
    Implementing correct image handling attachment plus additional fallback to product image if no attachments have been added.
- Version 1.5:
    Little code adjustments, adding readme, adding to git repo and so on.

### Website Backend
Within the products view, as enterprise user you can sell your product on eBay by clicking the checkbox 'Sell on eBay'. Ebay product images should get attached via ir.attachments what causes an error with the standard addon. This sale_ebay addon extension fixes that error when hitting the 'List Item On Ebay' button. Additionally it is now possible to bypass attachments. As fallback the standard product image will be used for the upload.

### Website Frontend
not affected

