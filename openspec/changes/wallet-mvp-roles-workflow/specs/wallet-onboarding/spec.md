# Spec Delta

## Purpose

Guía a la persona durante el registro y la activación de la wallet, y le muestra claramente el progreso, los bloqueos y la siguiente acción requerida antes de que pueda empezar a pagar.

## ADDED Requirements

### Requirement: Registro guiado de la wallet
La wallet DEBE (MUST) guiar a la persona por los pasos requeridos de registro y activación, y mostrar el progreso actual y la siguiente acción.

#### Scenario: Continuar el registro
- **WHEN** la persona completa un paso requerido del registro
- **THEN** la wallet DEBE mostrar el siguiente paso requerido y conservar el progreso completado

#### Scenario: La información requerida no es válida
- **WHEN** la persona envía información requerida incompleta o no válida
- **THEN** la wallet DEBE indicar el campo o paso que debe corregirse y NO DEBE señalar que el registro está completo

### Requirement: Resultado claro de activación
La wallet DEBE (MUST) comunicar si el registro está activo, todavía se está procesando o está bloqueado, e indicar cualquier acción necesaria antes de que se pueda empezar a pagar.

#### Scenario: El registro queda activado
- **WHEN** todas las verificaciones de activación requeridas se completan correctamente
- **THEN** la wallet DEBE confirmar la activación e indicar que la persona puede empezar a pagar

#### Scenario: La activación requiere una acción adicional
- **WHEN** la activación no se puede completar sin información adicional o una revisión
- **THEN** la wallet DEBE comunicar que la activación está incompleta e indicar la siguiente acción, sin dar a entender que ya se puede pagar
