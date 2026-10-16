This module makes the point of sale use the product categories, so that there
is a single category tree to maintain.

Standard Odoo keeps a separate tree of point of sale categories that has to be
maintained by hand and assigned to every product. With this module:

- every product category gets a point of sale category that mirrors it (same
  name, same parent), created, renamed, moved and deleted along with it;
- the point of sale category of each product is computed from its product
  category;
- the "PoS Product Categories" menu and settings button open the product
  categories.

The point of sale categories still exist as technical records, so the point of
sale interface, self ordering, restaurant printers and the "Restrict
categories" setting keep working unchanged. The module adds no JavaScript.

No configuration is needed: on installation every existing product category is
mirrored and every product, archived ones included, gets its point of sale
category.

This is a reimplementation for Odoo 19 of the idea of the OCA module of the same
name (versions 10.0 and 12.0), which replaced the model loaded by the point of
sale with the product categories. That is not possible anymore: in Odoo 19 the
point of sale interface and the self ordering, restaurant and event modules are
built around `pos.category`.
