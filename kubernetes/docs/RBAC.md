# Control de Acceso Basado en Roles (RBAC) en OpenShift
El **RBAC** en OpenShift determina si un usuario puede realizar ciertas acciones en el clúster o un proyecto. Es importante recordar que la autorización es un paso separado de la autenticación.

## Componentes del Proceso de Autorización
- **Rule:** Define las acciones permitidas sobre objetos o grupos de objetos (ej., crear Pods).
- **Role:** Es un conjunto de Rules. Los usuarios y grupos pueden estar asociados con múltiples Roles.
- **Binding:** Es la asignación de Users o Groups a un Role.

> Aunque a menudo se usan indistintamente en el lenguaje informal, técnicamente:
> - Una **Rule** es una definición muy específica de "permiso atómico".
> - Una **Policy** es el sistema de control de acceso completo, compuesto por `Rules`, `Roles`, `ClusterRoles`, `RoleBindings` y `ClusterRoleBindings`.

## Scope del RBAC
OpenShift define dos niveles para Roles y Bindings, lo que permite flexibilidad y reutilización:
- **Cluster RBAC:** Roles y Bindings que aplican en todo el clúster, es decir, a través de todos los proyectos (ej., `cluster-admin`).
- **Local RBAC:** Roles y Bindings que están limitados a un proyecto específico (Namespace) (ej., edit en mi-proyecto). Los Bindings locales pueden referenciar tanto Roles de clúster como Roles locales.

## Gestión de RBAC con la CLI
- `oc adm policy` **(Para Administradores de Clúster)**: Usado para Roles y Bindings de Clúster, y roles a nivel de proyecto que afecten a usuarios de clúster.
- `oc adm policy add-cluster-role-to-user <rol-cluster> <usuario>:` Asigna un `ClusterRole` a un usuario (ej., cluster-admin).
- `oc adm policy remove-cluster-role-from-user <rol-cluster> <usuario>:` Remueve un `ClusterRole` de un usuario.
- `oc adm policy who-can <acción> <recurso>:` Verifica si un usuario/grupo puede realizar una acción específica.
- `oc policy` **(Para Administradores de Proyecto)**: Usado para Roles y Bindings dentro de un proyecto específico.
- `oc policy add-role-to-user <rol-nombre> <usuario> -n <proyecto>:` Asigna un rol a un usuario dentro de un proyecto. Nota: Si <rol-nombre> es un `ClusterRole` (ej., `basic-user`), el `add-role-to-user -n <proyecto>` lo limita a ese proyecto para ese usuario.

## Roles por Defecto Comunes
OpenShift incluye Roles predefinidos muy útiles:
- `cluster-admin:` Acceso de superusuario a todo el clúster y todos los proyectos.
- `admin:` Administrador de proyecto; puede gestionar todos los recursos y accesos dentro de su proyecto.
- `edit:` Desarrollador en un proyecto; puede crear, cambiar y borrar recursos de aplicación comunes (servicios, deployments). No puede gestionar accesos ni cuotas.
- `view` / `basic-user` / `cluster-reader` / `cluster-status:` Roles de solo lectura con diferentes alcances.
- `self-provisioner:` Permite a un usuario crear sus propios proyectos. Por defecto, se asigna a usuarios autenticados.

## Tipos de Usuarios
- **Regular Users (Usuarios Humanos)**: Representan a personas que interactúan con la plataforma. Los permisos se asignan directamente a su objeto User o a los Group a los que pertenecen. Se crean automáticamente al autenticarse exitosamente.
- **System Users (Usuarios del Sistem**a): Creados automáticamente por la infraestructura para interacciones internas y seguras con la API (ej., `system:admin`, `system:node:`...). Sus nombres inician con `system:`.
- **Service Accounts (SA)**: Identidades para aplicaciones o procesos automáticos que se ejecutan dentro del clúster (ej., Argo CD, Flux). Permiten a las apps interactuar con la API sin usar credenciales de usuario regulares. Se representan con el objeto ServiceAccount. Se crean automáticamente si el Pod no especifica una, o manualmente.

## Gestión de Grupos
Un `Group` representa un conjunto de usuarios. Los administradores de clúster usan oc adm groups para gestionarlos:
- `oc adm groups new <nombre-grupo>`: Crea un nuevo grupo.
- `oc adm groups add-users <nombre-grupo> <usuario1> <usuario2>`: Añade usuarios a un grupo.

Los permisos (Roles) se asignan a los grupos para simplificar la gestión de acceso a múltiples usuarios.

## Consideraciones Importantes sobre Proveedores de Identidad (IdP)
- **HTPasswd IdP**: Útil para aprendizaje y laboratorios por su simplicidad. No es para producción por la falta de MFA, SSO, y gestión centralizada.
- **En Producción**: Se usan IdPs externos (LDAP, Active Directory, Okta) para gestionar usuarios humanos. Ofrecen seguridad avanzada, escalabilidad y funcionalidades empresariales.
- El `kubeconfig` (o `oc login`) es la llave de acceso para usuarios humanos. Debe protegerse rigurosamente, preferentemente usando **tokens de corta duración** y **MFA** para el re-login.

Cuando OpenShift tiene varios proveedores de identidad (IdPs) configurados, es posible que dos IdPs diferentes envíen el mismo nombre de usuario para dos personas distintas. Para evitar estos conflictos, OpenShift usa el parámetro `mappingMethod` en el recurso `kind: OAuth`. Existen tres métodos de mapeo:
- `claim` (**por defecto**): OpenShift crea un usuario con el nombre de usuario que recibe del IdP. Sin embargo, si un usuario con ese mismo nombre ya existe y está asociado a otro IdP, el intento de login fallará. Este es el comportamiento más seguro para evitar ambigüedades.
- `add`: OpenShift crea el usuario si no existe. Pero si un usuario con ese nombre ya existe, OpenShift asocia la nueva identidad al usuario existente. Es útil cuando sabes que los IdPs usan los mismos nombres de usuario para las mismas personas y quieres que se vinculen a una única cuenta en OpenShift.
- `lookup`: OpenShift no crea usuarios ni identidades automáticamente. Simplemente busca un usuario que ya exista con ese nombre. Si no lo encuentra, el login falla. Con este método, los administradores deben crear los usuarios de forma manual (o con un proceso externo) antes de que puedan iniciar sesión. Esto da un control total sobre la creación de usuarios.

## Authentication by Using LDAP

La autenticación mediante LDAP en OpenShift permite que tu clúster valide las credenciales de los usuarios usando un servidor LDAP remoto de tu organización. Esto se configura a través de un Identity Provider (IdP) de tipo LDAP en el recurso `kind: OAuth` de OpenShift.

Para configurar esta conexión, necesitas una URI LDAP (ldap:// o ldaps:// para SSL/TLS). Esta URI especifica el servidor (`host:port`), la ubicación base de la búsqueda (`basedn`), los atributos a buscar (`attributes`), el alcance de la búsqueda (scope, 'one' para un nivel, 'sub' para subárboles) y filtros opcionales (`filter`) para refinar los resultados (ej. (`objectClass=person`). A menudo, se requieren credenciales administrativas (bind DN) dentro de la URI para que OpenShift pueda realizar las consultas.
```
ldapsearch ... ldap://host:port/basedn?attribute?scope?filter
```
Ex: `ldap://ldap.example.com:389/dc=example,dc=com?givenName,sn,cn?(uid=payden.tomcheck)`

