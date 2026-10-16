# Copyright 2026 Renzo Payero, DakoDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError

# Context key that lets this module write on the point of sale categories it
# manages, which are otherwise protected against direct changes.
SYNC_CONTEXT_KEY = "pos_remove_pos_category_sync"


class ProductCategory(models.Model):
    _inherit = "product.category"

    available_in_pos = fields.Boolean(
        string="Available in the Point of Sale",
        default=True,
        help="Uncheck to hide this category from the point of sale. Its child "
        "categories are hidden too, whatever their own setting, and their "
        "products are shown without category.",
    )
    pos_visible = fields.Boolean(
        string="Visible in the Point of Sale",
        compute="_compute_pos_visible",
        store=True,
        recursive=True,
        help="Technical field: this category and all its parents are available "
        "in the point of sale.",
    )
    pos_category_id = fields.Many2one(
        comodel_name="pos.category",
        string="Point of Sale Category",
        readonly=True,
        copy=False,
        ondelete="set null",
        help="Technical field: point of sale category kept in sync with this "
        "product category.",
    )
    image_512 = fields.Image(string="Image", max_width=512, max_height=512)
    image_128 = fields.Image(
        string="Image 128",
        related="image_512",
        max_width=128,
        max_height=128,
        store=True,
    )

    _pos_category_id_unique = models.UniqueIndex(
        "(pos_category_id) WHERE pos_category_id IS NOT NULL"
    )

    @api.depends("available_in_pos", "parent_id.pos_visible")
    def _compute_pos_visible(self):
        for category in self:
            category.pos_visible = category.available_in_pos and (
                not category.parent_id or category.parent_id.pos_visible
            )

    @api.model_create_multi
    def create(self, vals_list):
        categories = super().create(vals_list)
        categories._pos_remove_sync_pos_category()
        return categories

    def write(self, vals):
        res = super().write(vals)
        if {"name", "parent_id", "image_512"} & vals.keys():
            self._pos_remove_sync_pos_category()
        return res

    def unlink(self):
        # Deleting a category also deletes its children (ondelete cascade at
        # the database level), so their mirrors are removed here as well.
        mirrors = self.search([("id", "child_of", self.ids)]).pos_category_id
        if mirrors:
            # The mirrors are removed with sudo below: make sure the user may
            # delete these categories before touching them.
            self.check_access("unlink")
            if self.env["pos.session"].sudo().search_count(
                [("state", "!=", "closed")], limit=1
            ):
                raise UserError(
                    self.env._(
                        "You cannot delete a product category while a point of "
                        "sale session is open. Close the sessions first."
                    )
                )
            mirrors.sudo().with_context(**{SYNC_CONTEXT_KEY: True}).unlink()
        return super().unlink()

    def _pos_remove_sync_pos_category(self, adopt=False):
        # Create or update the point of sale category mirroring each category.
        # Parents are processed first, so that a child can point to the mirror
        # of its parent even when both were created in the same transaction.
        # With adopt=True, a point of sale category that mirrors nothing and
        # has the same name and parent is reused instead of creating a new one.
        categories = self.search([("id", "parent_of", self.ids)])
        # sudo: whoever manages product categories (for instance from
        # Inventory) may have no rights on pos.category. Only the mirrors are
        # written, with values taken from the product categories.
        PosCategory = self.env["pos.category"].sudo().with_context(
            **{SYNC_CONTEXT_KEY: True}, lang="en_US"
        )
        orphans = {}
        if adopt:
            for pos_category in PosCategory.search(
                [("product_category_ids", "=", False)], order="id"
            ):
                key = (pos_category.name, pos_category.parent_id.id)
                orphans.setdefault(key, []).append(pos_category)
        by_depth = categories.grouped(lambda c: c.parent_path.count("/"))
        for depth in sorted(by_depth):
            level = by_depth[depth]
            adopted = self.browse()
            to_create = self.browse()
            for category in level.filtered(lambda c: not c.pos_category_id).sorted("id"):
                key = (category.name, category.parent_id.pos_category_id.id)
                if orphans.get(key):
                    category.pos_category_id = orphans[key].pop(0)
                    adopted |= category
                else:
                    to_create |= category
            if to_create:
                mirrors = PosCategory.create(
                    [category._pos_remove_mirror_values() for category in to_create]
                )
                for category, mirror in zip(to_create, mirrors):
                    category.pos_category_id = mirror
            (level - to_create)._pos_remove_update_mirror(reset_translations=adopted)

    def _pos_remove_mirror_values(self):
        self.ensure_one()
        return {
            "name": self.name,
            "parent_id": self.parent_id.pos_category_id.id,
            "image_512": self.image_512,
        }

    def _pos_remove_update_mirror(self, reset_translations=None):
        # Push the name, parent and image of each category to its mirror. The
        # name is written in en_US and the other translations are removed, so
        # that every language shows the product category name.
        # reset_translations holds the categories whose mirror translations
        # must be removed even if the en_US name already matches (adopted
        # mirrors).
        reset_translations = reset_translations or self.browse()
        other_langs = [
            code for code, _name in self.env["res.lang"].get_installed() if code != "en_US"
        ]
        for category in self.filtered("pos_category_id"):
            mirror = category.pos_category_id.sudo().with_context(
                **{SYNC_CONTEXT_KEY: True}, lang="en_US"
            )
            vals = {}
            if mirror.name != category.name:
                vals["name"] = category.name
            if mirror.parent_id != category.parent_id.pos_category_id:
                vals["parent_id"] = category.parent_id.pos_category_id.id
            if mirror.image_512 != category.image_512:
                vals["image_512"] = category.image_512
            if vals:
                mirror.write(vals)
            if other_langs and ("name" in vals or category in reset_translations):
                mirror.update_field_translations("name", dict.fromkeys(other_langs, False))
