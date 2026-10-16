# Implementacion de visibilidad de pagos QR para comercios

## Fuente

- Historia: `issues/merchant-qr-payment-status-visibility.sp.md`
- Especificacion funcional: `specs/merchant-qr-payment-status.md`
- Agente de implementacion: `.github/agents/developer.agent.md`

## Contexto actual

El repositorio contiene la estructura inicial del MVP y no hay evidencia de ejecucion. La historia requiere que el comercio identifique cada intento QR, consulte su estado actual, vea los cambios comunicados por el proveedor y filtre el historial por fecha y referencia.

## Objetivo

Implementar la consulta de estado e historial de pagos QR para comercios del MVP en Peru, con informacion suficientemente confiable para apoyar la decision de entrega del producto o servicio.

## Stack y limites

- **Interfaz:** React; el canal de consulta (app, web o ambos) debe aprobarse antes de definir la experiencia.
- **Backend:** Python con Flask.
- **Persistencia:** PostgreSQL.
- **Mensajeria:** RabbitMQ y Kafka forman parte del stack, pero no esta asignado cual —si alguno— participara en la actualizacion de estados.
- **Coordinacion de Kafka:** Zookeeper; no define comportamiento funcional de Pagos QR.
- **Contenedores:** Docker y Docker Compose.

No asumir un unico riel de procesamiento. No definir ni cambiar contratos HTTP, de proveedor, de persistencia o de eventos sin aprobacion.

## Comportamiento a preservar

- Cada intento de pago QR se identifica mediante una referencia unica.
- La consulta muestra el estado actual del intento dentro del conjunto habilitado para el MVP.
- Los cambios de estado comunicados por callbacks o eventos del proveedor se reflejan en la vista.
- El historial se puede filtrar por fecha y referencia.
- La funcionalidad se limita a pagos QR de comercios de la cohorte MVP en Peru.

## Alcance

- Mostrar cada intento QR con su referencia y estado actual.
- Reflejar los cambios de estado comunicados por el proveedor.
- Permitir consultar el historial mediante filtros por fecha y referencia.
- Limitar los estados y el canal de consulta a las decisiones aprobadas para el lanzamiento.

## Fuera de alcance

- Elegir app, web o ambos como canal.
- Definir el conjunto de estados o sus transiciones.
- Diseñar APIs, integraciones, callbacks, eventos o esquemas de almacenamiento.
- Elegir un riel de procesamiento o asignar responsabilidades entre RabbitMQ y Kafka.
- Definir conciliacion, reversos, disputas u otros procesos no cubiertos por la historia.

## Criterios de aceptacion

1. El comercio puede consultar cada intento QR mediante una referencia unica.
2. Cada intento muestra un estado actual perteneciente al conjunto aprobado para el MVP.
3. Cuando un callback o evento valido del proveedor informa un cambio, la vista refleja el estado comunicado.
4. El comercio puede filtrar el historial por fecha y referencia de transaccion.

## Pruebas requeridas

- Pruebas de interfaz para referencia, estado actual y filtros, una vez aprobado el canal.
- Pruebas de backend para consultar intentos e historial con los filtros acordados.
- Pruebas de integracion con PostgreSQL para persistir y consultar el estado e historial requeridos.
- Pruebas de actualizacion de estado a partir de callbacks o eventos cuando se aprueben sus contratos y mecanismo de recepcion.
- Prueba de arranque con Docker Compose cuando los servicios del MVP esten configurados.

## Riesgos y decisiones pendientes

- Aprobar el canal de consulta: app, web o ambos.
- Definir el conjunto minimo de estados y las transiciones validas para el lanzamiento.
- Definir los contratos y la validacion de callbacks o eventos de proveedor, incluyendo como tratar mensajes repetidos o fuera de orden.
- Acordar que broker, si alguno, participa en la actualizacion de estados.
- Definir el alcance de acceso de cada comercio a sus intentos e historial.
- Acordar la semantica de los filtros de fecha y referencia.