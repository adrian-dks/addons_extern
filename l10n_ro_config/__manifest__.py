# Copyright (C) 2014 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Romania - Localization Config",
    "summary": "Romania - Localization Install and Config Applications",
    "license": "AGPL-3",
    "version": "13.0.1.0.0",
    "author": "NextERP Romania,"
    "Forest and Biomass Romania,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-romania",
    "depends": ["l10n_ro", "l10n_ro_partner_create_by_vat"],
    "data": [
        "views/report_templates.xml",
        "views/res_config_view.xml",
        "views/res_bank_view.xml",
    ],
    "development_status": "Mature",
    "maintainers": ["feketemihai"],
    "installable": True,
    "auto_install": True,
}
