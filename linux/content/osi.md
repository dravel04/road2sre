# Modelo OSI

## Capa de Aplicación (Capa 7):
- **HTTP/HTTPS:** Protocolo de transferencia de hipertexto utilizado para la comunicación en la World Wide Web.
    - `HTTPS = HTTP + SSL/TLS`
- **SMTP:** Protocolo simple de transferencia de correo electrónico utilizado para enviar correos electrónicos.
    - a
- **FTP:** Protocolo de transferencia de archivos utilizado para la transferencia de archivos entre sistemas.
    - `SFTP = FTP + SSH`
    - `FTPS = FTP + SSL`
- **DNS:** Sistema de nombres de dominio que traduce nombres de dominio legibles por humanos en direcciones IP numéricas.
- **SSH:** Protocolo que proporcionar una conexión segura y cifrada a un sistema remoto a través de una línea de comandos.

## Capa de Presentación (Capa 6):
- **SSL/TLS:** Protocolos de seguridad que proporcionan cifrado y autenticación para la comunicación segura a través de la red, comúnmente utilizado en `HTTPS`, `SMTPS`, `FTPS`, entre otros. Utiliza un intercambio de claves asimétricas para establecer una clave de sesión compartida, que luego se utiliza para el cifrado y el descifrado simétrico de los datos transmitidos entre el cliente y el servidor.
- `TLS` se considera la evolución y la versión más segura de `SSL`. A menudo se usan indistintamente y están estrechamente relacionados en el contexto de la ciberseguridad.

## Capa de Sesión (Capa 5):
   - **RPC (Remote Procedure Call):** Protocolo que actúa como un puente para la interoperabilidad entre aplicaciones distribuidas, permitiendo la ejecución de funciones o procedimientos en un servidor remoto como si fueran invocados localmente.
   - **SIP (Session Initiation Protocol):** Protocolo utilizado para establecer, modificar y finalizar sesiones de comunicación multimedia, como llamadas de voz y video sobre IP.

## Capa de Transporte (Capa 4):
- **TCP (Transmission Control Protocol):** Protocolo de transporte confiable orientado a la conexión utilizado para la comunicación de datos en redes de computadoras.
- **UDP (User Datagram Protocol):** Protocolo de transporte sin conexión que ofrece una comunicación más rápida pero menos confiable en comparación con `TCP`.

## Capa de Red (Capa 3):
   - **IP (Internet Protocol):** Protocolo utilizado para enrutar paquetes de datos a través de redes de computadoras, identificando direcciones IP de origen y destino.
   - **ICMP (Internet Control Message Protocol):** Protocolo utilizado para diagnóstico o control de errores, como la comprobación de la conectividad de red mediante ping.

## Capa de Enlace de Datos (Capa 2):
- **Ethernet:** Protocolo de red ampliamente utilizado que define el formato de los paquetes de datos y las reglas para su transmisión en redes locales.
- **PPP (Point-to-Point Protocol):** Protocolo utilizado para establecer conexiones directas entre dos nodos de una red, comúnmente utilizado en conexiones de banda ancha como DSL y cable.
- **Wi-Fi:** Estándar de comunicación inalámbrica utilizado para redes locales (LAN) y conexión a Internet.

## Capa Física (Capa 1):
- **Ethernet PHY (10BASE-T, 100BASE-TX, 1000BASE-T):** Estándares de cableado físico y conectores utilizados en redes Ethernet.
- **DSL (Digital Subscriber Line):** Tecnología de acceso a Internet que utiliza líneas telefónicas existentes para la transmisión de datos.
- **Fibra óptica:** Medio de transmisión que utiliza hilos de vidrio o plástico para transmitir datos a través de pulsos de luz.