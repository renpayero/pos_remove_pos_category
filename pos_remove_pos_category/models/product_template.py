# Copyright 2026 Renzo Payero, DakoDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pos_categ_ids = fields.Many2many(
        compute="_compute_pos_categ_ids",
        store=True,
        readonly=True,
    )

    @api.depends("categ_id.pos_visible", "categ_id.pos_category_id")
    def _compute_pos_categ_ids(self):
        PosCategory = self.env["pos.category"]
        for template in self:
            category = template.categ_id
            template.pos_categ_ids = (
                category.pos_category_id if category.pos_visible else PosCategory
            )
