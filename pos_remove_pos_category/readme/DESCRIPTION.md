Este módulo hace que el punto de venta use las categorías de producto, así
que hay un solo árbol de categorías para mantener.

Odoo trabaja con dos árboles por separado: las categorías de producto (las de
Inventario, Contabilidad y los informes) y las categorías del punto de venta
(los botones de la caja). Hay que mantener los dos a mano y asignarle a cada
producto su categoría del punto de venta. Con este módulo:

- cada categoría de producto tiene una categoría del punto de venta "espejo",
  con el mismo nombre y como padre el espejo del padre, que se crea, se
  renombra, se mueve y se borra junto con la categoría de producto;
- la categoría del punto de venta de cada producto se calcula sola a partir
  de su categoría de producto;
- el menú "Categorías de producto de PdV" y el botón de Ajustes del punto de
  venta abren las categorías de producto.

Las categorías del punto de venta siguen existiendo como registros técnicos,
así que la caja, el autoservicio, las impresoras del modo restaurante y la
opción "Restringir categorías" siguen funcionando sin cambios. El módulo no
agrega JavaScript.

No hay nada que configurar: al instalarlo crea el espejo de todas las
categorías de producto existentes y le asigna su categoría del punto de venta
a cada producto, incluidos los archivados.

Es una reimplementación para Odoo 19 de la idea del módulo de OCA del mismo
nombre (versiones 10.0 y 12.0), que reemplazaba el modelo que carga la caja
por las categorías de producto. En la 19 eso ya no se puede: la pantalla de la
caja y los módulos de autoservicio, restaurante y eventos dependen de
`pos.category`.
