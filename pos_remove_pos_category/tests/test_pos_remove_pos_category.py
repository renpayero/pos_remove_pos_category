# Copyright 2026 Renzo Payero, DakoDev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.point_of_sale.tests.common import TestPoSCommon

from ..hooks import post_init_hook
from ..models.product_category import SYNC_CONTEXT_KEY

# 1x1 transparent PNG
IMAGE = (
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    b"YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


@tagged("post_install", "-at_install")
class TestPosRemovePosCategory(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env["product.category"]
        cls.Template = cls.env["product.template"]
        cls.parent = cls.Category.create({"name": "Plumbing"})
        cls.child = cls.Category.create({"name": "Fittings", "parent_id": cls.parent.id})
        cls.product_parent = cls.Template.create(
            {"name": "Pipe", "categ_id": cls.parent.id, "available_in_pos": True}
        )
        cls.product_child = cls.Template.create(
            {"name": "Elbow", "categ_id": cls.child.id, "available_in_pos": True}
        )

    def _rel_count(self, pos_categories):
        self.env.flush_all()
        self.env.cr.execute(
            "SELECT count(*) FROM pos_category_product_template_rel"
            " WHERE pos_category_id IN %s",
            [tuple(pos_categories.ids)],
        )
        return self.env.cr.fetchone()[0]

    def test_mirror_tree(self):
        parent_mirror = self.parent.pos_category_id
        child_mirror = self.child.pos_category_id
        self.assertEqual(parent_mirror.name, "Plumbing")
        self.assertFalse(parent_mirror.parent_id)
        self.assertEqual(child_mirror.name, "Fittings")
        self.assertEqual(child_mirror.parent_id, parent_mirror)
        self.assertEqual(child_mirror.product_category_ids, self.child)
        self.assertEqual(self.product_parent.pos_categ_ids, parent_mirror)
        self.assertEqual(self.product_child.pos_categ_ids, child_mirror)

    def test_create_parent_and_child_together(self):
        # The child is created inside the create of its parent, before the
        # parent itself is synchronised.
        parent = self.Category.create(
            {"name": "Gas", "child_id": [Command.create({"name": "Valves"})]}
        )
        self.assertTrue(parent.pos_category_id)
        self.assertEqual(
            parent.child_id.pos_category_id.parent_id, parent.pos_category_id
        )
        self.assertEqual(
            self.env["pos.category"].search_count([("name", "=", "Gas")]), 1
        )

    def test_batch_create(self):
        categories = self.Category.create(
            [{"name": "Taps", "parent_id": self.parent.id}, {"name": "Tools"}]
        )
        self.assertEqual(len(categories.pos_category_id), 2)
        self.assertEqual(
            categories[0].pos_category_id.parent_id, self.parent.pos_category_id
        )
        self.assertFalse(categories[1].pos_category_id.parent_id)

    def test_rename_in_all_languages(self):
        self.env["res.lang"]._activate_lang("es_AR")
        mirror = self.child.pos_category_id
        # A translation left on the mirror (only this module may write it).
        mirror.with_context(**{SYNC_CONTEXT_KEY: True}).update_field_translations(
            "name", {"es_AR": "Accesorios"}
        )
        self.assertEqual(mirror.with_context(lang="es_AR").name, "Accesorios")
        self.child.name = "Connectors"
        self.assertEqual(mirror.with_context(lang="en_US").name, "Connectors")
        self.assertEqual(mirror.with_context(lang="es_AR").name, "Connectors")

    def test_move(self):
        other = self.Category.create({"name": "Heating"})
        self.child.parent_id = other
        self.assertEqual(self.child.pos_category_id.parent_id, other.pos_category_id)
        self.child.parent_id = False
        self.assertFalse(self.child.pos_category_id.parent_id)

    def test_copy(self):
        copy = self.child.copy()
        self.assertTrue(copy.pos_category_id)
        self.assertNotEqual(copy.pos_category_id, self.child.pos_category_id)
        self.assertEqual(copy.pos_category_id.parent_id, self.parent.pos_category_id)

    def test_image_is_copied_to_the_mirror(self):
        category = self.Category.create({"name": "Showers", "image_512": IMAGE})
        self.assertTrue(category.pos_category_id.image_512)
        self.assertEqual(category.pos_category_id.image_512, category.image_512)
        category.image_512 = False
        self.assertFalse(category.pos_category_id.image_512)

    def test_change_product_category(self):
        self.product_child.categ_id = self.parent
        self.assertEqual(self.product_child.pos_categ_ids, self.parent.pos_category_id)

    def test_product_without_category(self):
        template = self.Template.create({"name": "Loose", "categ_id": False})
        self.assertFalse(template.pos_categ_ids)

    def test_archived_product(self):
        template = self.Template.create(
            {"name": "Old", "categ_id": self.child.id, "active": False}
        )
        self.assertEqual(template.pos_categ_ids, self.child.pos_category_id)

    def test_hide_parent_hides_branch(self):
        self.parent.available_in_pos = False
        self.assertFalse(self.child.pos_visible)
        self.assertFalse(self.product_parent.pos_categ_ids)
        self.assertFalse(self.product_child.pos_categ_ids)
        self.parent.available_in_pos = True
        self.assertEqual(self.product_parent.pos_categ_ids, self.parent.pos_category_id)
        self.assertEqual(self.product_child.pos_categ_ids, self.child.pos_category_id)

    def test_hide_child_only(self):
        self.child.available_in_pos = False
        self.assertEqual(self.product_parent.pos_categ_ids, self.parent.pos_category_id)
        self.assertFalse(self.product_child.pos_categ_ids)

    def test_hidden_child_stays_hidden_when_parent_comes_back(self):
        self.child.available_in_pos = False
        self.parent.available_in_pos = False
        self.parent.available_in_pos = True
        self.assertTrue(self.parent.pos_visible)
        self.assertFalse(self.child.pos_visible)
        self.assertFalse(self.product_child.pos_categ_ids)

    def test_move_under_hidden_category(self):
        hidden = self.Category.create({"name": "Hidden", "available_in_pos": False})
        self.child.parent_id = hidden
        self.assertFalse(self.child.pos_visible)
        self.assertFalse(self.product_child.pos_categ_ids)
        self.child.parent_id = self.parent
        self.assertEqual(self.product_child.pos_categ_ids, self.child.pos_category_id)

    def test_unlink_category_with_products(self):
        mirrors = self.parent.pos_category_id | self.child.pos_category_id
        # Deleting the parent deletes the child too (ondelete cascade).
        self.parent.unlink()
        self.env.invalidate_all()
        self.assertFalse(mirrors.exists())
        self.assertFalse(self.child.exists())
        self.assertFalse(self.product_child.categ_id)
        self.assertFalse(self.product_child.pos_categ_ids)
        self.assertEqual(self._rel_count(mirrors), 0)

    def test_mirror_is_protected(self):
        mirror = self.child.pos_category_id
        with self.assertRaises(UserError):
            mirror.name = "Renamed"
        with self.assertRaises(UserError):
            mirror.parent_id = False
        with self.assertRaises(UserError):
            mirror.unlink()
        mirror.color = 3
        self.assertEqual(mirror.color, 3)
        self.assertEqual(mirror.name, "Fittings")

    def test_unmirrored_pos_category_is_free(self):
        free = self.env["pos.category"].create({"name": "Manual"})
        free.name = "Manual 2"
        free.unlink()
        self.assertFalse(free.exists())

    def test_product_manager_without_pos_rights(self):
        user = new_test_user(
            self.env,
            login="catalog_manager",
            groups="base.group_user,product.group_product_manager",
        )
        category = self.Category.with_user(user).create({"name": "Tools"})
        self.assertTrue(category.sudo().pos_category_id)
        category.with_user(user).name = "Hand tools"
        self.assertEqual(category.sudo().pos_category_id.name, "Hand tools")
        category.with_user(user).unlink()
        self.assertFalse(
            self.env["pos.category"].search_count(
                [("name", "in", ["Tools", "Hand tools"])]
            )
        )

    def test_unlink_without_rights_keeps_the_mirror(self):
        user = new_test_user(self.env, login="plain_user", groups="base.group_user")
        mirror = self.child.pos_category_id
        with self.assertRaises(AccessError):
            self.child.with_user(user).unlink()
        self.assertTrue(mirror.exists())

    def test_post_init_hook_adopts_mirrors(self):
        mirrors = self.parent.pos_category_id | self.child.pos_category_id
        count = self.env["pos.category"].search_count([])
        # Simulate a reinstallation: the mirrors are there but not linked.
        (self.parent | self.child).write({"pos_category_id": False})
        post_init_hook(self.env)
        self.assertEqual(self.env["pos.category"].search_count([]), count)
        self.assertEqual(
            self.parent.pos_category_id | self.child.pos_category_id, mirrors
        )
        self.assertEqual(
            self.child.pos_category_id.parent_id, self.parent.pos_category_id
        )
        self.assertEqual(self.product_child.pos_categ_ids, self.child.pos_category_id)

    def test_post_init_hook_duplicate_names(self):
        first = self.Category.create({"name": "Twin"})
        second = self.Category.create({"name": "Twin"})
        mirrors = first.pos_category_id | second.pos_category_id
        (first | second).write({"pos_category_id": False})
        post_init_hook(self.env)
        self.assertEqual(first.pos_category_id | second.pos_category_id, mirrors)
        self.assertNotEqual(first.pos_category_id, second.pos_category_id)

    def test_post_init_hook_repairs_products(self):
        archived = self.Template.create(
            {"name": "Old", "categ_id": self.child.id, "active": False}
        )
        self.env.flush_all()
        self.env.cr.execute(
            "DELETE FROM pos_category_product_template_rel"
            " WHERE product_template_id IN %s",
            [tuple((self.product_child | archived).ids)],
        )
        self.env.invalidate_all()
        self.assertFalse(archived.pos_categ_ids)
        post_init_hook(self.env)
        self.assertEqual(self.product_child.pos_categ_ids, self.child.pos_category_id)
        self.assertEqual(archived.pos_categ_ids, self.child.pos_category_id)


@tagged("post_install", "-at_install")
class TestPosRemovePosCategorySession(TestPoSCommon):
    def setUp(self):
        super().setUp()
        self.config = self.basic_config
        self.category = self.env["product.category"].create({"name": "Counter"})
        self.product = self.env["product.template"].create(
            {"name": "Tap", "categ_id": self.category.id, "available_in_pos": True}
        )

    def test_unlink_with_open_session(self):
        self.open_new_session()
        with self.assertRaises(UserError):
            self.category.unlink()
        self.assertTrue(self.category.exists())
        self.assertTrue(self.category.pos_category_id.exists())

    def test_pos_data_has_mirror(self):
        templates = (
            self.env["product.template"]
            .with_context(pos_limited_loading=False)
            ._load_pos_data_search_read({}, self.config)
        )
        data = next(t for t in templates if t["id"] == self.product.id)
        self.assertEqual(data["pos_categ_ids"], self.category.pos_category_id.ids)

    def test_restrict_categories(self):
        self.config.write(
            {
                "limit_categories": True,
                "iface_available_categ_ids": [
                    Command.set(self.category.pos_category_id.ids)
                ],
            }
        )
        PosCategory = self.env["pos.category"]
        loaded = PosCategory.search(
            PosCategory._load_pos_data_domain({"pos.printer": []}, self.config)
        )
        self.assertEqual(loaded, self.category.pos_category_id)
        Template = self.env["product.template"]
        domain = Template._load_pos_data_domain({}, self.config)
        self.assertIn(self.product, Template.search(domain))
