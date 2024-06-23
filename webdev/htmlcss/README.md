# HTML y CSS

### Como se comporta los script JS en la web
![JS rendering](./img/image.png)

## CSS: Box Model
Por defecto, el tamaño de nuestros elementos en bloque vienen definidos por las propiedaes: `width/height + padding + boder`, pero si queremos forzar que los elementos tengan el tamaño que definimos en las propiedades `width/height` solo tendríamos que añadir el propiedad `box-sizing: border-box;`. El valor por defecto de esta propiedad es `box-sizing: content-box;`

### CSS: Overflow
Cuando el contenido de un elemento es mayor que el tamaño de la caja del elemento y desborda, ya que por defecto los elementos tienen la propierdad `overflow: visible`. Apoyandonos en el ejemplo:

| HTML | CSS |
| ---- | --- |
| `<section class="container">`<br>`    CSS ES INCREIBLE pero este texto no se ve`<br>`</section>` | `.container {`<br>`    width: 150px;`<br>`    height: 150px;`<br>`    background: white;`<br>`    padding: 10px;`<br>`    box-sizing: border-box;`<br>`    font-size: 48px;`<br>`    overflow: visible;`<br>`}` |

Algunas soluciones serían:
- `overflow: hidden` recorta el contenido para ajustarse al elemento, pero deja de ser accesible
    - Podemos añadir la propiedad `text-overflow: ellipsis;` para que el texto acabe con puntos suspensivos
- `overflow: scroll` recorta el contenido para ajustarse al elemento y el se puede acceder a este vía scroll
    - Si queremos usar `scroll`, lo recomendado es usar `overflow: auto` para no forzar al navegador que muestre las barras

### CSS: Position
Por defecto, `positin: static` según sea etiqueta de `block` o `inline` tendrá el compartamiento normal de "apilamiento"
- `positin: absolute` -> Nos permite definir la posicion con coordenadas respecto a todo el documento
```css
top: 0px;
bottom: 0px; 
right: 0px; 
left: 0px; 
```
- `positin: relative` -> Similar al `absolute` nos permite definir la posicion con coordenadas, pero esta vez en relación al padre del elemento que estamos estilando
> Aunque no es una buena práctica, podríamos centrar una modal en el centro de la página simplemente poniendo `margin: auto; inset: 0;`
> `inset: 0;` seria similar a poner todas las posiciones `top,bottom,right,left` a `0`
- `position: fixed` -> parecido al `absolute` nos permite definir la posicion con coordenadas, pero esta vez en relación al `viewport`, es decir, cuando hagamos scroll es elemento "nos acompaña"
- `position: sticky` -> permite que el elemento "nos acompañe", pero solo dentro de los limite del padre, es decir, se mueve relativo a las dimensiones del elemento padre y luego "desaparece"

#### [Contexto de apilamiento](https://developer.mozilla.org/es/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context)
El contexto de apilamiento es la conceptualización tridimensional de los elementos HTML a lo largo de un `eje-Z imaginario` relativo al usuario que se asume está de cara al viewport o página web. Los elementos HTML ocupan este espacio por orden de prioridad basado en sus atributos.

`z-index` solo aplica en contextos de apilamiento. Ejemplo: [Z-index and stacking contexts](https://web.dev/learn/css/z-index)

### CSS: Flex





## Links
- [CSS desde cero](https://www.youtube.com/watch?v=TlJbu0BMLaY&t=1947s&ab_channel=midulive)
- [Manz CSS](https://lenguajecss.com/css/)
- [Curso Google CSS](https://web.dev/learn/css)