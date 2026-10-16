# Implementacion de OnBoarding del MVP Wallet

## Fuente

- Historia: `issues/user-onboarding-mvp-completion.sp.md`
- Especificacion funcional: `specs/onboarding.md`
- Agente de implementacion: `.github/agents/developer.agent.md`

## Objetivo

Implementar el onboarding guiado para la cohorte MVP de Peru, de modo que el usuario pueda completar el flujo, activar su wallet y acceder al punto de entrada de pagos de bajo monto.

## Stack y limites

- **Interfaz:** React.
- **Backend:** Python con Flask.
- **Persistencia:** PostgreSQL.
- **Contenedores y entorno local:** Docker y Docker Compose.
- **Mensajeria:** RabbitMQ y Kafka forman parte del stack del proyecto. No se define cual transportara los eventos de onboarding ni si ambos participan en este flujo.
- **Coordinacion de Kafka:** Zookeeper; no introduce comportamiento funcional de onboarding.

No agregar contratos HTTP, esquemas de datos ni contratos de eventos hasta que se aprueben explicitamente.

## Alcance

- Mostrar la secuencia de pasos y el paso actual.
- Bloquear el avance ante datos obligatorios faltantes o invalidos y mostrar como corregirlos, segun las reglas aprobadas por Producto y Cumplimiento.
- Al completar el flujo, dejar la wallet activa y permitir el acceso al punto de entrada de pagos de bajo monto.
- Registrar el inicio, la finalizacion de cada paso y el cierre del onboarding.
- Proveer los datos analiticos requeridos para los conteos mensuales de usuarios activos y la atribucion del gasto de adquisicion.

## Fuera de alcance

- Definir requisitos KYC, documentacion o campos obligatorios que aun no hayan sido acordados.
- Cambiar los contratos de pagos u otros flujos de la wallet.
- Elegir el broker, definir nombres y esquemas de eventos, o decidir la arquitectura de analitica sin aprobacion.
- Tratar los objetivos de duracion, MAU y CAC como garantias verificables mediante pruebas unitarias.

## Criterios de aceptacion

1. El usuario identifica los pasos requeridos y el paso actual durante el flujo.
2. Datos obligatorios faltantes o invalidos impiden avanzar y producen un mensaje accionable.
3. Completar el onboarding activa la wallet y da acceso al punto de entrada de pagos de bajo monto.
4. Se registran los eventos de inicio, finalizacion de pasos y cierre para analitica.
5. La analitica permite evaluar los objetivos definidos para duracion, MAU y CAC, una vez acordadas sus reglas de calculo.

## Pruebas requeridas

- Pruebas de interfaz para progresion, validacion y mensajes de correccion.
- Pruebas de integracion del backend para completar el onboarding y activar la wallet.
- Pruebas de persistencia del estado en PostgreSQL.
- Pruebas de registro y disponibilidad de eventos, una vez aprobados su contrato y transporte.
- Prueba de arranque del entorno con Docker Compose cuando sus servicios esten definidos.

## Decisiones pendientes antes de implementar

- Pasos, campos obligatorios y reglas de validacion, incluidos los requisitos KYC.
- Contrato HTTP y modelo de persistencia del onboarding.
- Eventos y timestamps que delimitan la duracion, y definicion de usuario activo.
- Regla de atribucion del gasto para CAC.
- Responsabilidad de RabbitMQ y Kafka en este flujo y contrato de eventos.
- Servicios y configuracion concretos del entorno Docker Compose.