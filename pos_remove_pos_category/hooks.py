# Copyright 2026 Renzo Payero, DakoDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    # Mirror every product category, reusing the point of sale categories left
    # by a previous installation instead of duplicating them.
    env["product.category"].search([])._pos_remove_sync_pos_category(adopt=True)
    # The relation table of pos_categ_ids already exists, so the ORM does not
    # compute the field on the existing products by itself.
    templates = env["product.template"].with_context(active_test=False).search([])
    env.add_to_compute(templates._fields["pos_categ_ids"], templates)
    templates._recompute_recordset(["pos_categ_ids"])


def uninstall_hook(env):
    # Give the "PoS Product Categories" menu back to the point of sale
    # categories, which stay in place with their products.
    action = env.ref(
        "point_of_sale.product_pos_category_action", raise_if_not_found=False
    )
    if action:
        action.write({"res_model": "pos.category", "view_mode": "list,kanban,form"})
