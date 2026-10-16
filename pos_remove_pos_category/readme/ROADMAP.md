- El informe de cierre de sesión (*Detalles de ventas*) agrupa las ventas por
  el nombre de la categoría del punto de venta, como hace Odoo de por sí: dos
  categorías con el mismo nombre bajo padres distintos se juntan en ese
  informe.
- Las categorías del punto de venta creadas a mano, que no son espejo de
  ninguna categoría de producto, se conservan pero no tienen productos.
- Los escenarios de bienvenida del punto de venta (restaurante, bar, etc.) les
  asignan sus propias categorías del punto de venta a los productos que crean.
  Esos productos las conservan hasta que se les cambie la categoría de
  producto.
- La caja muestra una categoría solo si tiene productos cargados. Odoo 19 carga
  al abrir la caja hasta `point_of_sale.limited_product_count` productos (5.000
  por defecto): con más productos que ese límite, alguna categoría puede no
  aparecer hasta que se busquen sus productos.
