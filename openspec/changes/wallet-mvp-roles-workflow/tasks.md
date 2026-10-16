# Tasks

## 1. Producto, Arquitectura y Seguridad preventiva

- [ ] 1.1 PO refina los recorridos de registro, pagador y comercio; verifica que cada especificación de capacidad tenga escenarios de aceptación aprobados para resultados normales, rechazados, duplicados y no resueltos, cuando corresponda.
- [ ] 1.2 Arquitectura selecciona la pila tecnológica, los límites de integración de pagos e identidad, el modelo de estados de operación y los contratos de API; verifica que `design.md` registre las decisiones, alternativas y ejemplos de contrato antes de iniciar la implementación.
- [ ] 1.3 Seguridad preventiva realiza un análisis de amenazas para el registro, la autorización de pagos, los reintentos, la asociación QR, los datos sensibles y la auditabilidad; verifica que cada amenaza material esté vinculada a un control y a una actividad de prueba o revisión en las especificaciones o el diseño.
- [ ] 1.4 PO, Arquitectura y Seguridad preventiva revisan y aprueban la línea base de requisitos y diseño; verifican que las aprobaciones y las decisiones diferidas estén registradas antes de iniciar las tareas de implementación.

## 2. Entrega de Backend

- [ ] 2.1 Backend implementa los contratos aprobados de pagos y estados de transacción, incluida la autorización, la validación, la persistencia de estados de operación y los reintentos idempotentes; verifica con pruebas automatizadas que repetir una operación no genere un débito adicional.
- [ ] 2.2 Backend implementa el manejo de rechazos definitivos y resultados no resueltos, así como la consulta de estados; verifica con pruebas automatizadas el rechazo, el tiempo de espera agotado, la resolución posterior del estado y la recuperación segura sin informar un éxito falso.
- [ ] 2.3 Backend documenta el contrato de API aprobado y la semántica de errores y estados; verifica que la documentación coincida con el contrato implementado e incluya ejemplos de resultados exitosos, rechazados, duplicados y no resueltos.

## 3. Entrega de Frontend

- [ ] 3.1 Frontend implementa el registro guiado, la retroalimentación de validación, el estado de activación y las siguientes acciones; verifica con pruebas automatizadas de interfaz la continuación, los datos inválidos, la activación y los estados que requieren acción.
- [ ] 3.2 Frontend implementa el envío de pagos del pagador y las pantallas de resultado y recuperación; verifica con pruebas automatizadas de interfaz que se distingan los estados completado, rechazado, duplicado y no resuelto, y que el estado no resuelto nunca se muestre como éxito definitivo.
- [ ] 3.3 Frontend implementa la vista de transacciones QR del comercio y la orientación para la entrega; verifica con pruebas automatizadas de interfaz que se muestren los estados confirmado, rechazado y no resuelto, y que no se recomiende entregar el producto ante un pago no confirmado.

## 4. Revisión independiente de Seguridad y aceptación del MVP

- [ ] 4.1 Revisión independiente de Seguridad evalúa el diseño, la implementación, la configuración, las dependencias y la evidencia de pruebas; verifica que los hallazgos se registren con severidad, evidencia, responsable y disposición requerida.
- [ ] 4.2 Las personas responsables de Backend y Frontend resuelven los hallazgos de seguridad requeridos; verifican que pasen las pruebas automatizadas afectadas y que la persona revisora independiente confirme el cierre o registre una aceptación de riesgo autorizada explícitamente.
- [ ] 4.3 PO, Backend y Frontend ejecutan los escenarios de aceptación de extremo a extremo para el registro, los resultados para el pagador, los reintentos duplicados y los estados QR del comercio; verifican que los resultados observados cumplan las especificaciones aprobadas.
- [ ] 4.4 PO registra los pasos de demostración y la evidencia de pruebas en `wallet-hackathon/evidence.md`; verifica que la evidencia identifique cada escenario, operación y resultado, y cualquier acción del usuario o comercio, sin incluir secretos reales ni datos sensibles de clientes.
