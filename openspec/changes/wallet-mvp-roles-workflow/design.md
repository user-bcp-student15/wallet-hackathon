# Design

## Context

Consulta `proposal.md` para conocer la motivación. Las tres épicas de la wallet están registradas en `wallet-hackathon/docs/epics.md`, pero el proyecto aún no tiene especificaciones de capacidades, una pila tecnológica seleccionada ni una implementación de la aplicación. Este cambio define un flujo desde el producto hasta la entrega y el comportamiento observable; no selecciona una arquitectura de ejecución.

## Goals / Non-Goals

**Objetivos:**

- Asignar a cada rol responsabilidades, entradas, resultados y funciones de revisión claramente definidos.
- Mantener los contratos de comportamiento en las especificaciones, las decisiones técnicas en el diseño y el trabajo ejecutable en las tareas.
- Asegurar que el estado de los pagos, el manejo de duplicados, los resultados no resueltos y las decisiones de entrega de los comercios se validen antes de la publicación.
- Permitir que Backend y Frontend trabajen sobre comportamientos y contratos acordados.

**Fuera de alcance:**

- Seleccionar frameworks, servicios en la nube, proveedores de pago, bases de datos o plataformas de agentes.
- Implementar el registro, el procesamiento de pagos, los pagos QR, los controles de seguridad o las interfaces de usuario.
- Considerar a un agente de IA como aprobador de decisiones financieras o de seguridad.

## Decisions

### Usar un cambio guiado por especificaciones para las tres capacidades relacionadas de la wallet

Los contratos de registro y activación, confirmación de pagos y estado de pagos QR para comercios se agrupan en un mismo cambio porque el resultado central del MVP es ofrecer una experiencia de pago coherente. Cada capacidad conserva su propio archivo de especificación para que su comportamiento pueda evolucionar de forma independiente.

Alternativa considerada: crear un cambio por épica. Esto agregaría coordinación entre cambios para los resultados de pago y las revisiones compartidas, antes de aprobar una pila tecnológica o un plan de entrega.

### Asignar responsabilidades por rol según los artefactos OpenSpec y los puntos de revisión

| Rol | Actividades principales | Contribución / resultado en OpenSpec | Responsabilidad de aprobación |
|---|---|---|---|
| PO | Refinar los recorridos de usuario, el alcance, las prioridades, los criterios de aceptación y las siguientes acciones visibles para el usuario; acordar lo que queda fuera del alcance. | Es responsable de `proposal.md`; redacta en conjunto el comportamiento y los escenarios de las especificaciones; confirma la evidencia de aceptación. | Aprueba el alcance y el comportamiento del producto antes de la implementación y valida la demostración. |
| Arquitectura | Definir los límites del sistema, el modelo de datos y estados, los contratos de API, las opciones de integración, los supuestos operativos y la secuencia de implementación. | Es responsable de `design.md`; contribuye tareas de contratos y viabilidad. | Aprueba la coherencia técnica y confirma la decisión sobre la pila tecnológica antes de la implementación. |
| Seguridad preventiva | Identificar amenazas y controles requeridos para el registro, la autorización de pagos, los duplicados y reintentos, la asociación de códigos QR, los datos sensibles, los secretos y la auditabilidad. | Contribuye restricciones y escenarios de seguridad verificables en las especificaciones y el diseño; crea tareas de seguridad. | Confirma que los controles estén planificados y puedan verificarse antes de iniciar la implementación. |
| Backend | Definir e implementar, tras la aprobación, los contratos del servidor, la persistencia, la validación, la autorización, los estados de operación, la idempotencia y el manejo de errores. | Agrega tareas de implementación y pruebas automatizadas a `tasks.md`; proporciona el comportamiento de la API y evidencia de pruebas. | Confirma que los resultados del servidor satisfagan las especificaciones; no aprueba el alcance del producto ni las excepciones de seguridad. |
| Frontend | Implementar, conforme a los contratos aprobados, el registro guiado, el envío de pagos, la presentación de estados, las acciones de recuperación y las vistas de transacciones para comercios. | Agrega tareas de interfaz y pruebas automatizadas a `tasks.md`; proporciona evidencia de los recorridos de usuario. | Confirma que los estados y las acciones mostrados coincidan con los resultados de Backend y las especificaciones. |
| Revisión independiente de Seguridad | Revisar la cobertura de amenazas, la implementación, la configuración, las dependencias, la evidencia de pruebas y los hallazgos no resueltos, con independencia de quien implementó. | Agrega tareas de revisión y corrección, y registra hallazgos y evidencia mediante el proceso de revisión acordado por el proyecto. | Recomienda la publicación solo cuando los hallazgos requeridos estén resueltos o hayan sido aceptados explícitamente por la persona autorizada. |

Las dos funciones de Seguridad se consideran responsabilidades distintas: diseño preventivo y verificación independiente. En un equipo pequeño puede desempeñarlas una misma persona, pero la revisión debe seguir siendo un punto de control separado y no debe presentarse como independiente si quien revisa diseñó el control evaluado.

### Mantener las decisiones de comportamiento e implementación en los artefactos correspondientes

Las especificaciones de capacidades definen el comportamiento observable externamente y sus escenarios. `design.md` registra las decisiones sobre el sistema y el flujo de trabajo, junto con sus alternativas. `tasks.md` descompone el comportamiento y el diseño aprobados en trabajo de implementación, pruebas, seguridad y revisión. Las responsabilidades por rol se registran en el diseño y las tareas, en lugar de incluirse como requisitos para los usuarios finales.

Alternativa considerada: incluir todo el proceso por roles en las especificaciones de capacidades. Esto mezclaría la gobernanza de entrega con el comportamiento de la wallet visible para el usuario y dificultaría las pruebas de los contratos de capacidades.

### Condicionar la implementación a la aprobación de requisitos, contratos y criterios de seguridad

PO aprueba el alcance y los escenarios de aceptación; Arquitectura define la pila tecnológica y los contratos; Seguridad preventiva confirma los controles requeridos. Después, Backend y Frontend implementan en paralelo cuando los contratos lo permiten. La aceptación de extremo a extremo y la revisión independiente de Seguridad preceden a la decisión de demostración o publicación.

El flujo de pago no debe tratar un tiempo de espera agotado como éxito o rechazo definitivo. El contrato de Backend y la interfaz deben conservar el estado «no resuelto» hasta que haya un resultado definitivo; los reintentos no deben producir un débito adicional para la misma operación.

Alternativa considerada: dejar que los equipos de implementación deduzcan durante la programación la semántica de pago que falta. Esto arriesga generar comportamientos de estado inconsistentes entre la API, la interfaz del pagador y la vista del comercio.

### Mantener el uso de agentes como apoyo y dentro de límites definidos

Los agentes pueden preparar borradores de artefactos, proponer escenarios, generar casos de prueba y resumir evidencia. Las personas responsables de cada rol conservan la autoridad para aprobar el alcance del producto, las decisiones técnicas, los hallazgos de seguridad y la preparación para la publicación.

Alternativa considerada: permitir que un agente apruebe cambios automáticamente. Esto no es apropiado para decisiones que afecten la corrección de los pagos, la seguridad o los fondos de los clientes.

## Risks / Trade-offs

- **Riesgo:** Las épicas no especifican suficientemente las verificaciones de activación, la finalización del pago ni la asociación de transacciones QR. → **Mitigación:** PO y Arquitectura resuelven estos puntos antes de la implementación; no se debe inferir comportamiento regulatorio o específico de un proveedor.
- **Riesgo:** Una misma persona asume ambas responsabilidades de seguridad, lo que reduce la independencia. → **Mitigación:** Mantener listas de verificación separadas para prevención y revisión, y revelar cualquier superposición entre quien revisa y quien implementa.
- **Riesgo:** Backend y Frontend interpretan de forma distinta los estados de pago. → **Mitigación:** Acordar los nombres y significados de los estados y el contrato de API antes de la implementación en paralelo; probar de extremo a extremo los mismos escenarios.
- **Riesgo:** Una actualización del estado se retrasa o no está disponible. → **Mitigación:** Mantener la operación visiblemente «no resuelta» hasta verificarla y proporcionar una acción segura para consultar el estado o recuperarse.

## Migration Plan

No se requiere migración de la aplicación. Antes de la implementación, PO aprueba los requisitos refinados, Arquitectura registra las decisiones sobre la pila tecnológica y los contratos, y Seguridad confirma los controles planificados. Después, la implementación continúa según las tareas aprobadas. Los detalles de despliegue y reversión deberán diseñarse una vez seleccionados el entorno de ejecución y la integración de pagos.

## Open Questions

No hay preguntas abiertas para este flujo de planificación. La pila tecnológica, el proveedor, las verificaciones de identidad y las opciones de despliegue son decisiones explícitas que deben resolverse durante la actividad de Arquitectura antes de la implementación, no supuestos implícitos en este diseño.
