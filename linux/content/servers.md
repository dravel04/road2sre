# Servidores

## Firewall
Un `Firewall` es una barrera de seguridad diseñada para proteger una red de computadoras, dispositivos o sistemas contra amenazas externas e internas al controlar y filtrar el tráfico de red que entra y sale de la red. Funciona como una puerta de entrada que supervisa y regula el flujo de datos entre la red interna y externa, permitiendo o bloqueando el acceso según reglas predefinidas

## Forward Proxy
`Forward Proxy` es un sistema que proporciona una puerta de enlace entre usuarios e internet, es decir, se situa en medio de las comunicaciones y hace de intermediario. Se suele utilizar para:
- **Acceso a Internet controlado:** En entornos empresariales, un forward proxy puede utilizarse para controlar y filtrar el acceso a Internet. El proxy puede bloquear el acceso a ciertos sitios web o tipos de contenido no deseados, como sitios de redes sociales o contenido para adultos.
- **Anonimización de la dirección IP:** Los forward proxies también pueden utilizarse para ocultar la dirección IP real del cliente al acceder a sitios web. Esto puede ser útil para proteger la privacidad del usuario y evitar la identificación del cliente por parte del servidor de destino.
- **Optimización del rendimiento:** Almacenamiento en caché de contenido web: Los forward proxies pueden almacenar en caché el contenido web solicitado por los clientes. Cuando un cliente solicita un recurso que ya está almacenado en la caché del proxy, el proxy puede devolver el recurso almacenado en lugar de reenviar la solicitud al servidor de destino. Esto puede mejorar el rendimiento y reducir el tiempo de carga de las páginas web para los clientes.
- **Control de ancho de banda:** Un forward proxy puede utilizarse para controlar y limitar el ancho de banda utilizado por los clientes al acceder a Internet. Esto puede ayudar a evitar la congestión de la red y garantizar un rendimiento óptimo para todos los usuarios.

Una de las soluciones más usadas es `squid` la cual podemos desplegar en [contenedores](https://hub.docker.com/search?q=squid)

## Reverse Proxy
`Reverse Proxy` es un sistema que actúa como intermediario entre los clientes y los servidores de destino. A diferencia de un *forward proxy* que reenvía las solicitudes de los clientes a servidores externos, un *reverse proxy* reenvía las solicitudes de los clientes a servidores internos, y luego reenvía las respuestas de esos servidores de vuelta a los clientes. En resumen, un *reverse proxy* oculta la infraestructura interna y sirve como punto de entrada único para los clientes externos.

Una de las soluciones más usadas es `nginx` la cual podemos desplegar en [contenedores](https://hub.docker.com/_/nginx)

