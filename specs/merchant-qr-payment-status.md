# Visibilidad del estado de pagos QR para comercios

## Fuente

- Historia: `merchant-qr-payment-status-visibility.sp.md`
- Épica relacionada: `peru-wallet-mvp.sp.md`
- Evidencia: `evidence.md`, que indica que todavía no hay evidencia de ejecución del MVP.

## Contexto actual

La historia describe una necesidad de visibilidad operativa para pequeños comercios que cobran con QR. El comercio debe poder consultar cada intento mediante una referencia única, conocer su estado actual, recibir actualizaciones cuando el proveedor informe cambios y filtrar el historial por fecha y referencia.

El canal de consulta —app, web o ambos— y el conjunto mínimo de estados para el lanzamiento están pendientes de definición. No hay evidencia de ejecución del MVP todavía.

## Problema confirmado

El comercio necesita información confiable y consultable sobre cada pago QR para decidir cuándo entregar el producto o servicio. La dependencia de terceros y la confiabilidad de la confirmación se identifican en la épica como riesgos relevantes para el MVP.

## Comportamiento a preservar

- La visibilidad descrita aplica a los pagos QR de comercios del MVP en Perú.
- Cada intento de pago QR debe poder identificarse mediante una referencia única de transacción.
- El estado mostrado corresponde al estado actual disponible para ese intento.
- Los cambios de estado comunicados por callbacks o eventos del proveedor deben reflejarse en la vista.
- El historial debe poder filtrarse por fecha y referencia de transacción.
- El MVP no debe asumir un único riel de procesamiento de extremo a extremo.

## Alcance

- Especificar cómo el comercio identifica cada intento de pago QR y consulta su estado actual.
- Especificar la actualización de la vista ante cambios de estado informados por el proveedor.
- Especificar la consulta del historial mediante filtros por fecha y referencia de transacción.
- Limitar el comportamiento a los canales y estados que se definan para el lanzamiento MVP.

## Fuera de alcance

- Elegir entre app, web o ambos como canal de consulta.
- Definir el conjunto de estados del lanzamiento; está pendiente de definición.
- Cambiar el contrato API publicado o definir integraciones, mecanismos de recepción de callbacks/eventos o detalles de almacenamiento que no estén descritos en el contrato.
- Definir conciliación, reversos, disputas u otros procesos operativos no descritos en la historia.
- Añadir flujos de pago distintos de la visibilidad de pagos QR para comercios.

## Criterios de aceptación

1. El comercio puede visualizar cada intento de pago QR con una referencia única de transacción.
2. Cada intento muestra un estado actual perteneciente al conjunto habilitado para el MVP.
3. Cuando un callback o evento del proveedor cambia el estado de una transacción, la vista refleja el estado comunicado.
4. El comercio puede filtrar el historial de estados por fecha y referencia de transacción.

## Contratos afectados/protegidos

- **Afectados a nivel de comportamiento:** identificación de intentos QR, consulta y actualización de estado, y filtros del historial.
- **Contrato API asociado:** [Swagger de mocks, grupo 5](https://bcp-ai-labs.pages.dev/dia-04/mocks/swagger?group=5), operación asignada W2 - Pago a contacto. El método, la ruta, los esquemas y los errores deben tomarse del contrato publicado; no se deben inferir ni modificar.
- **Protegidos:** no cambiar contratos de pago u otros flujos. La asociación a W2 sigue la asignación aprobada y no modifica por sí sola los criterios funcionales de visibilidad QR definidos en esta especificación.
- El conjunto de estados y el canal de consulta quedan pendientes; esta especificación no fija sus detalles.

## Riesgos, supuestos y preguntas abiertas

- **Riesgo:** la dependencia de terceros puede afectar la disponibilidad y oportunidad de las actualizaciones de estado.
- **Riesgo:** mostrar un estado desactualizado o no confiable puede llevar al comercio a tomar una decisión incorrecta sobre la entrega del producto o servicio.
- **Supuesto:** el canal de consulta del comercio (app, web o ambos) queda por definir.
- **Pregunta abierta:** ¿cuál es el conjunto mínimo de estados necesario para la operación de comercios en el lanzamiento MVP?

**Detenido para revisión humana.**