# CAMT Format Bank Statements Import

Module to import SEPA CAMT.053 and CAMT.054 Format bank statement files.

## Getting Started

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
git clone git@gitlab.gitgmbh.com:cpgmbh/kms-odoo/v12/addons-int/account_bank_statement_import_camt_oca.git extra-addons
cd extra-addons/account_bank_statement_import_camt_oca
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

