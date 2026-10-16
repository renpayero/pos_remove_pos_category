# pos_remove_pos_category

Odoo 19 Community module: the point of sale uses the **product categories**, so
there is a single category tree to maintain. Every product category is mirrored
as a point of sale category and every product gets its point of sale category
from its product category. No JavaScript, no configuration.

See [the module README](pos_remove_pos_category/README.rst) for the details.

## Installation

Add this repository to the `addons_path` of an Odoo 19 server (branch `19.0`)
and install *POS Remove POS Category*. It depends only on `point_of_sale`.

## License

[AGPL-3.0 or later](LICENSE).

Based on the idea of the OCA module of the same name for Odoo 10.0 and 12.0, by
Akretion, Camptocamp and ACSONE SA/NV.
