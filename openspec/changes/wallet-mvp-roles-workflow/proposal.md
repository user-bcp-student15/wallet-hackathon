# Proposal

## Why

El MVP de la wallet tiene tres épicas de producto, pero aún no cuenta con requisitos detallados y verificables ni con una transferencia de trabajo acordada entre Producto, Arquitectura, Seguridad, Backend y Frontend. Definir las actividades mediante un flujo guiado por especificaciones permitirá revisar los resultados de pago y las responsabilidades de seguridad antes de iniciar la implementación.

## What Changes

- Establecer responsabilidades por rol y puntos de aprobación para PO, Arquitectura, Seguridad preventiva, Backend, Frontend y revisión independiente de Seguridad.
- Definir especificaciones de comportamiento para el registro y activación de la wallet, la confirmación de pagos y el estado de pagos QR para comercios, incluidos los casos de éxito, rechazo, solicitudes duplicadas y fallas que requieren acción del usuario.
- Definir la secuencia de planificación OpenSpec y las dependencias entre tareas de implementación, con revisiones explícitas de Producto, Arquitectura y Seguridad.
- Mantener fuera del alcance la selección tecnológica y la implementación hasta que se aprueben los requisitos y las decisiones de diseño.

## Capabilities

### New Capabilities

- `wallet-onboarding`: Registro y activación guiados de la wallet, con pasos siguientes claros.
- `payment-confirmation`: Resultados definitivos y comprensibles de un pago de bajo monto, incluidos los casos de duplicación y de resultado incierto o fallido.
- `merchant-qr-payments`: Estado confiable de las transacciones para un comercio que recibe pagos QR de clientes.

### Modified Capabilities

Ninguna. Actualmente el proyecto no tiene especificaciones OpenSpec de capacidades.

## Impact

- Agrega artefactos de cambio OpenSpec y especificaciones de capacidades para las tres épicas de la wallet.
- Usa el archivo existente `wallet-hackathon/docs/epics.md` como contexto de producto.
- Establece responsabilidades de planificación y revisión; no modifica código de aplicación, API, infraestructura, dependencias ni configuración de ejecución.
