# Spec Delta

## Purpose

Permite que un comercio que recibe un pago QR de un cliente consulte un estado confiable de la transacción y decida si es seguro entregar el producto o prestar el servicio.

## ADDED Requirements

### Requirement: Mostrar al comercio un estado confiable del pago QR
Para cada pago QR asociado al comercio, la wallet DEBE (MUST) mostrar un estado que distinga entre la finalización confirmada, el rechazo y un resultado no resuelto.

#### Scenario: Se confirma el pago QR
- **WHEN** se confirma que un pago QR se completó
- **THEN** el comercio DEBE poder ver que la transacción está completada

#### Scenario: Se rechaza el pago QR
- **WHEN** se rechaza un pago QR
- **THEN** el comercio DEBE poder ver que la transacción no se completó

#### Scenario: El pago QR no está resuelto
- **WHEN** todavía no se puede confirmar el resultado del pago
- **THEN** el comercio DEBE ver que la transacción no está resuelta y NO DEBE mostrarse como completada

### Requirement: Facilitar una decisión segura de entrega al comercio
La wallet DEBE (MUST) dejar claro si el comercio tiene un estado de pago confirmado que le permita entregar el producto o si debe esperar una actualización.

#### Scenario: El comercio consulta un pago completado
- **WHEN** el comercio consulta una transacción cuya finalización está confirmada
- **THEN** la wallet DEBE indicar que el pago está confirmado

#### Scenario: El comercio consulta un pago no completado o no resuelto
- **WHEN** el comercio consulta una transacción rechazada o no resuelta
- **THEN** la wallet DEBE indicar que el pago no está confirmado y NO DEBE sugerir que se entregue el producto basándose en esa transacción

### Requirement: Limitar la información de pago visible para el comercio
La wallet DEBE (MUST) mostrar al comercio únicamente la información de la transacción necesaria para identificar el pago QR y comprender su estado.

#### Scenario: El comercio consulta una transacción QR
- **WHEN** el comercio abre el estado de una transacción
- **THEN** la wallet DEBE evitar exponer información del pagador que no sea necesaria para identificar la transacción o actuar según su estado
