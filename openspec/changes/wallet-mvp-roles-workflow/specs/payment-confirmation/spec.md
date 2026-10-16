# Spec Delta

## Purpose

Proporciona al pagador un estado confiable de cada pago de bajo monto, para que pueda distinguir las operaciones completadas, rechazadas, repetidas y no resueltas, y saber qué hacer a continuación.

## ADDED Requirements

### Requirement: Comunicar el resultado del pago
Para cada pago, la wallet DEBE (MUST) presentar un estado que distinga correctamente un pago completado de una operación rechazada o no resuelta.

#### Scenario: El pago se completa correctamente
- **WHEN** se confirma que el pago se completó
- **THEN** la wallet DEBE mostrar el resultado como completado e identificar la operación

#### Scenario: El pago es rechazado
- **WHEN** se rechaza el pago
- **THEN** la wallet DEBE mostrar que no se completó y proporcionar el motivo disponible o la siguiente acción

### Requirement: Evitar una ejecución duplicada al reintentar
La wallet DEBE (MUST) garantizar que reintentar la misma operación de pago no ejecute un débito adicional y DEBE devolver el estado asociado a esa operación.

#### Scenario: Se vuelve a enviar la misma operación
- **WHEN** se recibe más de una vez la misma operación de pago
- **THEN** la wallet NO DEBE ejecutar un débito adicional y DEBE informar el estado de la operación existente

#### Scenario: Se inicia un pago independiente
- **WHEN** el pagador inicia intencionalmente una nueva operación de pago
- **THEN** la wallet DEBE tratarla como una operación independiente y NO DEBE representarla silenciosamente como un reintento de la operación anterior

### Requirement: Representar con precisión los resultados de pago no resueltos
Cuando la wallet no pueda determinar si un pago se completó, DEBE (MUST) comunicar que el resultado no está resuelto y proporcionar una siguiente acción segura, sin afirmar que hubo un éxito o un rechazo definitivo.

#### Scenario: No se puede confirmar el resultado del pago
- **WHEN** un tiempo de espera agotado o una falla impide que la wallet obtenga un resultado definitivo del pago
- **THEN** la wallet DEBE mostrar un estado no resuelto e indicar al pagador cómo consultar el resultado o continuar de forma segura

#### Scenario: El estado pasa a ser definitivo
- **WHEN** la wallet obtiene posteriormente un resultado definitivo para una operación no resuelta
- **THEN** la wallet DEBE actualizar el estado de la operación y comunicar el resultado confirmado
