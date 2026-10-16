# Implementacion de pagos de bajo monto

## Fuente

- Historia: `issues/payer-low-value-payment-confirmation.sp.md`
- Especificacion funcional: `specs/payer-low-contact-payment.md`
- Agente de implementacion: `.github/agents/developer.agent.md`

## Contexto actual

El repositorio contiene la estructura inicial del MVP, pero todavia no hay implementacion ni evidencia de ejecucion. La spec requiere confirmacion de pagos con estados posiblemente asincronos, persistencia de referencias exitosas y prevencion de cobros duplicados al reintentar.

## Objetivo

Implementar el flujo de pago de bajo monto para la cohorte MVP en Peru, mostrando al pagador el resultado de cada intento y preservando la integridad de pagos e historial.

## Stack y limites

- **Interfaz:** React.
- **Backend:** Python con Flask.
- **Persistencia:** PostgreSQL.
- **Mensajeria:** RabbitMQ y Kafka forman parte del stack; no esta definido cual transportara el evento de activacion ni si ambos participan en este flujo.
- **Coordinacion de Kafka:** Zookeeper; no define comportamiento funcional del pago.
- **Contenedores:** Docker y Docker Compose.

No asumir un unico riel de procesamiento. No agregar ni cambiar contratos HTTP, esquemas de persistencia o contratos de eventos sin aprobacion.

## Comportamiento a preservar

- Mostrar la identidad del destino y el monto antes de la confirmacion final.
- Cada intento termina con un solo resultado: exitoso, fallido o expirado. El flujo puede mostrar estados intermedios mientras espera una respuesta asincrona.
- Validar el monto frente a los limites aplicables por proveedor antes del envio.
- Un pago exitoso muestra y persiste una referencia en el historial.
- Un fallo o expiracion ofrece una accion clara; reintentar no debe generar un cobro duplicado.
- Las transacciones exitosas emiten el evento de activacion requerido para el calculo de MAU.
- Preservar la compatibilidad de contratos existentes; la fuente no identifica contratos tecnicos que deban cambiarse.

## Alcance

- Presentar destino, monto y validacion antes de confirmar.
- Comunicar el estado del intento y su resultado terminal, contemplando transiciones asincronas.
- Persistir y mostrar la referencia de una transaccion exitosa.
- Permitir reintentar o volver ante fallos y expiraciones sin duplicar cobros.
- Emitir el evento de activacion de transacciones exitosas conforme al contrato que se apruebe.

## Fuera de alcance

- Definir el limite de "monto bajo" por proveedor o canal.
- Definir las etiquetas visibles de los estados terminales.
- Elegir rieles, diseñar integraciones tecnicas o asignar responsabilidades entre RabbitMQ y Kafka.
- Definir el contrato del evento de activacion o la arquitectura de analitica.
- Implementar pagos QR, reversos o disputas no cubiertos por esta historia.

## Criterios de aceptacion

1. Antes de confirmar, el pagador puede revisar la identidad del destino y el monto.
2. El monto se valida contra los limites configurados para el proveedor o canal antes del envio, y el resultado se comunica al pagador.
3. Cada intento presenta un unico resultado terminal: exitoso, fallido o expirado.
4. Un pago exitoso muestra una referencia y la conserva en el historial.
5. Ante fallo o expiracion, el pagador recibe una accion clara; reintentar no genera cobros duplicados.
6. Las transacciones exitosas emiten el evento de activacion definido para el reporte de MAU.
7. La medicion del flujo permite evaluar la reduccion de caida en checkout de 30% a 8% y el objetivo de MAU de 1,000 a 2,000 durante los meses 1 a 3 posteriores al lanzamiento, una vez acordadas las reglas de medicion.

## Pruebas requeridas

- Pruebas de interfaz para revision previa, validacion del monto y presentacion de estados.
- Pruebas de backend para transiciones asincronas y un unico resultado terminal por intento.
- Pruebas de reintento e idempotencia que verifiquen que no se creen cobros duplicados.
- Pruebas de integracion con PostgreSQL para la referencia e historial de pagos exitosos.
- Pruebas de emision del evento de activacion cuando se aprueben su contrato y transporte.
- Prueba de arranque con Docker Compose cuando los servicios del MVP esten configurados.

## Riesgos y decisiones pendientes

- Definir el limite de monto bajo por proveedor o canal.
- Acordar con Producto las etiquetas visibles de los estados terminales.
- Definir los estados intermedios, tiempos de espera y regla que determina una expiracion.
- Aprobar el contrato del evento de activacion y la responsabilidad de RabbitMQ/Kafka en su transporte.
- Definir como se mediran caida en checkout y MAU para evaluar los objetivos de negocio.