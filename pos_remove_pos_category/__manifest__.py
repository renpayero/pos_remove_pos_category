# Copyright 2026 Renzo Payero, DakoDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Remove POS Category",
    "summary": "Use the product categories as the point of sale categories",
    "version": "19.0.1.0.0",
    "category": "Sales/Point of Sale",
    "author": "Renzo Payero, DakoDev",
    "website": "https://github.com/renpayero/pos_remove_pos_category",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_category_views.xml",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
}
