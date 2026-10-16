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
``pos.category``.

**Índice**

.. contents::
   :local:

Uso
===

- Las categorías se administran desde *Inventario > Configuración >
  Categorías de productos* o desde *Punto de venta > Configuración >
  Categorías de producto de PdV*.
- Destildar *Disponible en el punto de venta* en una categoría la oculta de la
  caja junto con todas sus hijas, sin importar lo que tenga marcado cada hija.
  Sus productos se siguen vendiendo: aparecen en la lista de todos los
  productos y al buscar, sin categoría.
- Una imagen en la categoría de producto se muestra en su botón de la caja
  cuando está activada la opción *Mostrar imágenes de categorías* del punto de
  venta.
- La categoría del punto de venta de un producto es de solo lectura. En modo
  desarrollador se ve en la pestaña *Punto de venta* del producto.
- Si alguien intenta cambiar el nombre o el padre de un espejo directamente, o
  borrarlo, el sistema le indica que lo haga desde la categoría de producto.
- Al desinstalar el módulo, las categorías del punto de venta y la asignación
  de cada producto se conservan como categorías comunes del punto de venta. Si
  se instala de nuevo, las reutiliza y no las duplica.

Limitaciones conocidas
======================

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
  al abrir la caja hasta ``point_of_sale.limited_product_count`` productos
  (5.000 por defecto): con más productos que ese límite, alguna categoría puede
  no aparecer hasta que se busquen sus productos.

Historial de cambios
====================

19.0.1.0.0
----------

- Primera versión para Odoo 19, reescrita como espejo de las categorías de
  producto.

Reporte de errores
==================

Los errores se reportan en `GitHub Issues <https://github.com/renpayero/pos_remove_pos_category/issues>`_.

Créditos
========

Autores
-------

- Renzo Payero
- DakoDev

Colaboradores
-------------

- Renzo Payero <rpayerodev@gmail.com> (DakoDev)

Otros créditos
--------------

Basado en la idea del módulo ``pos_remove_pos_category`` de OCA para Odoo 10.0
y 12.0, de Akretion, Camptocamp y ACSONE SA/NV (Sylvain Calador, Simone Orsi y
Cédric Pigeon).
