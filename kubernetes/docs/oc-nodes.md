# Gestión de Nodos

## Arquitectura Básica del Clúster
El clúster está dividido en dos tipos de nodos:
- Nodos de plano de control: Gestionan y orquestan el clúster.
- Nodos de cómputo: Ejecutan las cargas de trabajo (aplicaciones).

Un node pool es un grupo lógico de nodos de cómputo. Se usan labels para asignar nodos a un pool específico.

## Gestión de Nodos y Configuración (MCO)
El **Machine Config Operator** (MCO) es la herramienta central para gestionar la configuración y las actualizaciones del sistema operativo de los nodos (RHCOS).

El MCO utiliza dos recursos personalizados (CRs):
- `MachineConfig` (MC): Declara los cambios de configuración que quieres aplicar a un nodo (ej. archivos en /etc, servicios de systemd).
- `MachineConfigPool` (MCP): Agrupa los nodos que deben recibir la misma configuración. Los labels se usan para que un MC se aplique a un MCP.

## Operadores para Casos de Uso Especiales
Se utilizan operadores de alto nivel para tareas específicas en lugar de aplicar cambios manualmente:
- Node Tuning Operator (NTO): Se utiliza para ajustar el kernel de los nodos para aplicaciones de alto rendimiento.