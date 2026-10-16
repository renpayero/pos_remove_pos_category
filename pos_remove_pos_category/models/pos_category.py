# Copyright 2026 Renzo Payero, DakoDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError

from .product_category import SYNC_CONTEXT_KEY


class PosCategory(models.Model):
    _inherit = "pos.category"

    product_category_ids = fields.One2many(
        comodel_name="product.category",
        inverse_name="pos_category_id",
        string="Product Categories",
        readonly=True,
        help="Technical field: the product category this point of sale "
        "category mirrors.",
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_except_product_category_mirror(self):
        if not self.env.context.get(SYNC_CONTEXT_KEY) and self.sudo().product_category_ids:
            raise UserError(
                self.env._(
                    "This point of sale category mirrors a product category. "
                    "Delete the product category instead."
                )
            )

    def write(self, vals):
        if (
            {"name", "parent_id"} & vals.keys()
            and not self.env.context.get(SYNC_CONTEXT_KEY)
            and self.sudo().product_category_ids
        ):
            raise UserError(
                self.env._(
                    "This point of sale category mirrors a product category. "
                    "Rename or move the product category instead."
                )
            )
        return super().write(vals)
