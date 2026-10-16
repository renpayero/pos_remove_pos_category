- The session closing report (*Sales Details*) groups the sales by point of
  sale category name, as standard Odoo does: two categories with the same name
  under different parents are merged in that report.
- Point of sale categories created by hand, that mirror no product category,
  are kept but no product is linked to them.
- The point of sale onboarding scenarios (restaurant, bar, ...) set their own
  point of sale categories on the products they create. Those products keep
  them until their product category changes.
