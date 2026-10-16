=======================
POS Remove POS Category
=======================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge2| image:: https://img.shields.io/badge/github-renpayero%2Fpos__remove__pos__category-lightgray.png?logo=github
    :target: https://github.com/renpayero/pos_remove_pos_category/tree/19.0
    :alt: renpayero/pos_remove_pos_category

|badge1| |badge2|

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
built around ``pos.category``.

**Table of contents**

.. contents::
   :local:

Usage
=====

- Manage the categories from *Inventory > Configuration > Product Categories*
  or *Point of Sale > Configuration > PoS Product Categories*.
- Uncheck *Available in the Point of Sale* on a category to hide it and all its
  children from the point of sale, whatever their own setting. Their products
  can still be sold: they are listed with all the products and found by
  search, without category.
- Set an image on a product category to show it on its point of sale button
  (point of sale setting *Show category images*).
- The point of sale category of a product is read-only. In developer mode it is
  shown on the *Point of Sale* tab of the product form.
- Uninstalling the module keeps the point of sale categories and the products
  linked to them, as regular point of sale categories. Installing it again
  reuses them instead of creating duplicates.

Known issues / Roadmap
======================

- The session closing report (*Sales Details*) groups the sales by point of
  sale category name, as standard Odoo does: two categories with the same name
  under different parents are merged in that report.
- Point of sale categories created by hand, that mirror no product category,
  are kept but no product is linked to them.
- The point of sale onboarding scenarios (restaurant, bar, ...) set their own
  point of sale categories on the products they create. Those products keep
  them until their product category changes.

Changelog
=========

19.0.1.0.0
----------

- First version for Odoo 19, rewritten as a mirror of the product categories.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/renpayero/pos_remove_pos_category/issues>`_.

Credits
=======

Authors
-------

- Renzo Payero
- DakoDev

Contributors
------------

- Renzo Payero <rpayerodev@gmail.com> (DakoDev)

Other credits
-------------

Based on the idea of the OCA module ``pos_remove_pos_category`` for Odoo 10.0
and 12.0, by Akretion, Camptocamp and ACSONE SA/NV (Sylvain Calador, Simone
Orsi and Cédric Pigeon).
