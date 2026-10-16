# Registro y activación del MVP de wallet

## Fuente

- Historia: `user-onboarding-mvp-completion.sp.md`
- Épica relacionada: `peru-wallet-mvp.sp.md`
- Evidencia: `evidence.md`, que indica que todavía no hay evidencia de ejecución del MVP.

## Contexto actual

La historia define un onboarding guiado para usuarios de smartphone que realizan transferencias diarias de bajo monto. El flujo debe mostrar los pasos y el avance, impedir que se avance con información obligatoria faltante o inválida, y permitir el acceso al punto de entrada de pagos de bajo monto cuando la wallet quede activa.

También requiere registrar eventos para analítica del MVP y medir duración, activación y gasto de adquisición. La épica establece como objetivo reducir el tiempo de finalización del onboarding de 8 a 3 minutos. No se ha documentado todavía evidencia de ejecución del flujo.

## Problema confirmado

La historia identifica la necesidad de completar el onboarding con menos fricción y con señales claras del siguiente paso, para que los usuarios puedan empezar a pagar sin abandonar el proceso. También requiere instrumentación que permita evaluar la finalización y activación del onboarding, así como las métricas de negocio indicadas para el MVP.

## Comportamiento a preservar

- El onboarding corresponde a la cohorte MVP de Perú.
- El usuario debe poder entender en qué paso está y qué debe hacer a continuación.
- La activación de la wallet al completar el onboarding habilita el acceso al punto de entrada de pagos de bajo monto.
- Los errores por información obligatoria faltante o inválida deben impedir el avance e indicar una acción correctiva.
- La instrumentación debe permitir medir inicio, finalización de pasos y cierre del flujo.
- No se prescriben cambios a los contratos de pago ni a otros flujos de la wallet.

## Alcance

- Especificar el recorrido guiado de onboarding y la visualización de sus pasos y del paso actual.
- Especificar el bloqueo ante datos obligatorios faltantes o inválidos y los mensajes accionables de corrección.
- Especificar el resultado observable de completar el onboarding: wallet activa y acceso al punto de entrada de pagos de bajo monto.
- Especificar el registro analítico del inicio, la finalización de cada paso y el cierre del flujo.
- Especificar la salida analítica con conteos mensuales de nuevos usuarios activos y atribución del gasto de adquisición para evaluar las métricas indicadas en la historia.
- Considerar los objetivos de duración, MAU y CAC definidos para la cohorte MVP en Perú.

## Fuera de alcance

- Definir requisitos de KYC o documentación; la historia indica que deben acordarse con cumplimiento y producto antes de implementar.
- Diseñar la solución técnica o definir componentes, clases, APIs o esquemas de almacenamiento.
- Modificar los flujos o contratos de pagos, QR, transferencias u otros países.
- Añadir objetivos de negocio distintos de los documentados en la historia y la épica.

## Criterios de aceptación

1. Durante el onboarding, el usuario puede identificar la secuencia de pasos requeridos y el paso actual.
2. Si falta información obligatoria o algún dato es inválido, el flujo no permite avanzar y muestra un mensaje que indica cómo corregirlo.
3. Al completar correctamente el onboarding, el estado de la wallet pasa a activo y el usuario puede acceder al punto de entrada de pagos de bajo monto.
4. Se registran eventos de inicio del onboarding, finalización de cada paso y cierre del flujo, disponibles para la analítica del MVP.
5. Para la cohorte MVP en Perú, el tiempo mediano de finalización del onboarding baja de 8 minutos a 3 minutos dentro del trimestre posterior al lanzamiento.
6. La salida analítica presenta conteos mensuales de nuevos usuarios activos y atribución del gasto de adquisición que permiten verificar MAU de 1,000 a 2,000 y CAC de PEN 10 por usuario nuevo durante los primeros tres meses posteriores al lanzamiento.

## Contratos afectados/protegidos

- **Afectados a nivel de comportamiento:** progresión del onboarding, activación de la wallet, acceso al punto de entrada de pagos de bajo monto y eventos/salida analítica descritos en esta especificación.
- **Protegidos:** no se identifican contratos técnicos de API o integración en la fuente. No se deben inferir ni cambiar contratos de pagos u otros flujos a partir de esta historia.

## Riesgos, supuestos y preguntas abiertas

- **Riesgo:** los requisitos de KYC y documentación no están definidos y pueden afectar los pasos requeridos y los bloqueos del flujo.
- **Supuesto:** los objetivos de MAU de 1,000–2,000 y CAC de PEN 10 fueron definidos por el Product Owner.
- **Pregunta abierta:** ¿qué eventos o timestamps definen oficialmente el inicio y el fin usados para medir la duración del onboarding?
- **Pregunta abierta:** ¿qué definición de “usuario activo” y qué regla de atribución del gasto de adquisición se usarán para verificar MAU y CAC?