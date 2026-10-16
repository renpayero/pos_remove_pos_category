# pos_remove_pos_category

Módulo para **Odoo 19 Community**: el punto de venta usa las **categorías de producto**, así que
hay un solo árbol de categorías para mantener.

## El problema

Odoo trabaja con dos árboles de categorías por separado:

- las **categorías de producto**, las que se usan en Inventario, en Contabilidad y en los informes;
- las **categorías del punto de venta**, las que se ven como botones en la caja.

Hay que mantener los dos a mano y asignarle a cada producto su categoría del punto de venta. En un
catálogo de miles de productos, eso es mucho trabajo y los dos árboles terminan desfasados.

## Cómo funciona

No es un port literal del módulo `pos_remove_pos_category` de OCA (versiones 10.0 y 12.0). Aquel
reemplazaba el modelo que carga la caja por las categorías de producto. En la 19 eso ya no se
puede: la pantalla de la caja y los módulos de autoservicio, restaurante y eventos dependen de las
categorías propias del punto de venta (`pos.category`).

En su lugar, **cada categoría de producto tiene una categoría del punto de venta "espejo"** que el
módulo mantiene solo:

- **El espejo.** Tiene el mismo nombre y, como padre, el espejo del padre. Se crea, se renombra, se
  mueve y se borra junto con la categoría de producto. Si alguien intenta cambiarle el nombre o el
  padre directamente, o borrarlo, el sistema le indica que lo haga desde la categoría de producto.
- **La categoría del producto en la caja se calcula sola** a partir de su categoría de producto.
  En el formulario del producto queda de solo lectura y solo se muestra en modo desarrollador.
- **La casilla "Disponible en el punto de venta"**, en la categoría de producto, oculta la rama
  entera: la categoría y todas sus hijas, sin importar lo que tenga marcado cada hija. Los productos
  de esa rama se siguen vendiendo: aparecen en la lista de todos los productos y al buscar, sin
  categoría.
- **El menú "Categorías de producto de PdV"** y el botón de Ajustes del punto de venta abren las
  categorías de producto.
- **Imagen.** La categoría de producto admite una imagen, que se usa en el botón de la caja cuando
  está activada la opción "Mostrar imágenes de categorías".

Como las categorías del punto de venta siguen existiendo como registros técnicos, la caja, el
autoservicio, las impresoras del modo restaurante y la opción "Restringir categorías" siguen
funcionando sin cambios. **No agrega JavaScript y no hay nada que configurar.**

## Instalación

1. Agregar este repositorio, rama `19.0`, al `addons_path` de un servidor Odoo 19.
2. Instalar el módulo *POS Remove POS Category*. Depende solo de `point_of_sale`.

Al instalarlo:

- crea el espejo de todas las categorías de producto existentes;
- asigna la categoría del punto de venta a todos los productos, incluidos los archivados;
- si encuentra categorías del punto de venta que no son espejo de nada y coinciden en nombre y
  padre con una categoría de producto, las reutiliza en lugar de duplicarlas. Pasa, por ejemplo, al
  reinstalarlo.

Las categorías del punto de venta que no coinciden con ninguna categoría de producto no se tocan:
quedan, pero sin productos.

## Desinstalación

Las categorías del punto de venta y la asignación de cada producto se conservan, y pasan a ser
categorías comunes del punto de venta. El menú vuelve a abrir las categorías del punto de venta. Si
el módulo se instala de nuevo, reutiliza esas categorías y no las duplica.

## Limitaciones conocidas

- El informe de cierre de sesión (*Detalles de ventas*) agrupa las ventas por el **nombre** de la
  categoría del punto de venta, como hace Odoo de por sí. Dos categorías con el mismo nombre bajo
  padres distintos se juntan en una sola fila de ese informe.
- Los escenarios de bienvenida del punto de venta (restaurante, bar, etc.) les asignan sus propias
  categorías del punto de venta a los productos que crean. Esos productos las conservan hasta que se
  les cambie la categoría de producto.
- La caja muestra una categoría solo si tiene productos cargados. Odoo 19 carga al abrir la caja
  hasta `point_of_sale.limited_product_count` productos (5.000 por defecto): con más productos que
  ese límite, alguna categoría puede no aparecer hasta que se busquen sus productos.

## Pruebas

El módulo incluye 25 tests automáticos: el espejo y su árbol, crear en lote, renombrar en varios
idiomas, mover, copiar, ocultar y volver a mostrar ramas, borrar con y sin sesión abierta, permisos,
la reutilización al reinstalar y los datos que recibe la caja. Para correrlos:

```
odoo -d <base_de_prueba> -i pos_remove_pos_category --test-enable \
     --test-tags /pos_remove_pos_category --stop-after-init
```

## Créditos

- Autores: Renzo Payero y DakoDev.
- Basado en la idea del módulo `pos_remove_pos_category` de OCA para Odoo 10.0 y 12.0, de
  Akretion, Camptocamp y ACSONE SA/NV (Sylvain Calador, Simone Orsi y Cédric Pigeon).

La ficha del módulo, la que muestra Odoo en Aplicaciones, está en
[pos_remove_pos_category/README.rst](pos_remove_pos_category/README.rst).

## Licencia

[AGPL-3.0 o posterior](LICENSE).
