# Confirmación de pagos de bajo monto

## Fuente

- Historia: `payer-low-value-payment-confirmation.sp.md`
- Épica relacionada: `peru-wallet-mvp.sp.md`
- Evidencia: `evidence.md`, que indica que todavía no hay evidencia de ejecución del MVP.

## Contexto actual

La historia requiere que el pagador vea la identidad del destino y el monto antes de confirmar una transferencia de bajo monto. Cada intento debe concluir con un único resultado terminal: exitoso, fallido o expirado. Los estados pueden ser asíncronos, por lo que la confirmación debe comunicar el resultado de forma clara.

La historia también requiere persistir la referencia de una transacción exitosa en el historial, ofrecer una acción clara ante fallos o expiraciones sin generar cobros duplicados, y emitir el evento de activación asociado a transacciones exitosas para el cálculo de MAU. No hay evidencia de ejecución del MVP todavía.

## Problema confirmado

El pagador necesita conocer con confianza el resultado de su transferencia. Sin una confirmación definitiva y comprensible, puede no saber si el pago fue realizado, falló o expiró. Los reintentos no deben ocasionar cobros duplicados. Además, el flujo debe contribuir a reducir la caída en checkout y permitir el seguimiento de MAU para la cohorte MVP en Perú.

## Comportamiento a preservar

- El flujo corresponde a transferencias de bajo monto de la cohorte MVP en Perú.
- Antes de confirmar, el pagador puede revisar la identidad del destino y el monto.
- Cada intento presenta un único resultado terminal: exitoso, fallido o expirado.
- Los estados de pago pueden cambiar de forma asíncrona.
- Los montos deben validarse contra los límites aplicables por proveedor antes del envío.
- Un pago exitoso conserva una referencia de transacción en el historial.
- Ante un fallo o expiración, el pagador recibe una acción clara y reintentar no crea cobros duplicados.
- Una transacción exitosa emite el evento de activación usado para el cálculo de MAU.
- El MVP no debe presuponer un único riel de procesamiento de extremo a extremo.

## Alcance

- Especificar la información mostrada al pagador antes de la confirmación final.
- Especificar los resultados terminales del intento y su presentación, considerando transiciones asíncronas.
- Especificar la referencia y persistencia en historial de una transacción exitosa.
- Especificar las acciones disponibles tras un pago fallido o expirado y la ausencia de cobros duplicados al reintentar.
- Especificar la validación visible del monto antes del envío, de acuerdo con los límites aplicables por proveedor.
- Especificar la emisión del evento de activación para transacciones exitosas y su uso en el reporte de MAU.
- Considerar el objetivo de reducir la caída en checkout de 30% a 8% durante el trimestre posterior al lanzamiento.

## Fuera de alcance

- Definir la regla inicial de monto bajo por proveedor o canal; está pendiente.
- Definir los nombres o etiquetas de los estados terminales que verá el usuario; están pendientes con producto.
- Especificar pagos QR para comercios, reversos o disputas que no estén cubiertos por esta historia.
- Definir la arquitectura, los rieles específicos, las integraciones técnicas o el contrato técnico del evento de activación.
- Añadir objetivos de negocio distintos de los documentados en la historia y la épica.

## Criterios de aceptación

1. Antes de la confirmación final, la pantalla de pago muestra la identidad del destino y el monto de la transferencia.
2. Cada intento de pago presenta un único resultado terminal: exitoso, fallido o expirado.
3. Cuando el pago es exitoso, se muestra una referencia de transacción y esta queda persistida en el historial.
4. Cuando el pago falla o expira, el pagador recibe una acción clara para reintentar o volver, y reintentar no crea cobros duplicados.
5. Antes del envío, el flujo valida el monto contra los límites aplicables por proveedor y muestra al pagador el resultado de la validación.
6. Para la cohorte MVP en Perú, la tasa de caída en checkout de este flujo se reduce de 30% a 8% dentro del trimestre posterior al lanzamiento.
7. Las transacciones exitosas del pagador emiten el evento de activación usado en el cálculo de MAU, de modo que el reporte de los meses 1 a 3 permita verificar el objetivo de MAU de 1,000 a 2,000.

## Contratos afectados/protegidos

- **Afectados a nivel de comportamiento:** información previa a la confirmación, resultados terminales por intento, referencia e historial de transacciones exitosas, acciones ante fallos o expiraciones, validación del monto y evento de activación.
- **Protegidos:** no se identifican contratos técnicos de API o integración en la fuente. No se deben inferir cambios a los contratos de pagos ni asumir un único riel de procesamiento.
- Las etiquetas de estados y el contrato del evento de activación quedan pendientes; esta especificación no fija sus detalles técnicos.

## Riesgos, supuestos y preguntas abiertas

- **Riesgo:** las transiciones asíncronas pueden perjudicar la confianza si el usuario no recibe un resultado claro.
- **Riesgo:** reintentos sin prevención de duplicados pueden generar cobros duplicados y problemas de conciliación.
- **Supuesto:** el rango objetivo de MAU de 1,000 a 2,000 y el objetivo de CAC de PEN 10 fueron definidos por el Product Owner; esta historia requiere el evento asociado a MAU, no define el cálculo de CAC.
- **Pregunta abierta:** ¿qué regla inicial define “monto bajo” para cada proveedor o canal del lanzamiento MVP?
- **Pregunta abierta:** ¿qué etiquetas de los estados terminales verá el usuario?
- **Pregunta abierta:** ¿qué definición y contrato tiene el evento de activación del pagador, y cómo se verifica su inclusión en el reporte mensual de MAU?