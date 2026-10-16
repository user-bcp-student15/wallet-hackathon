# Wallet Hackathon

Base del proyecto para demostrar de inicio a fin una wallet simple y segura: registro, pagos a personas o comercios y consulta clara del resultado de cada operacion.

## Objetivo del MVP

Una persona debe poder completar un pago de bajo monto y entender inmediatamente si fue realizado, rechazado, duplicado o si fallo y requiere una accion. Los agentes se incorporaran donde agreguen valor al flujo; su framework y arquitectura siguen pendientes de definicion.

## Stack tecnologico acordado

- **Backend:** Python con Flask.
- **Persistencia:** PostgreSQL.
- **Mensajeria:** RabbitMQ y Kafka, con Zookeeper para la coordinacion de Kafka.
- **Frontend:** React.
- **Contenedores:** Docker y Docker Compose.

El stack queda registrado como contexto del proyecto. Las versiones, responsabilidades concretas de cada broker y configuraciones de servicios siguen pendientes de definicion.

## Epicas de contexto

1. **Registro y activacion del MVP de wallet**  
   Como usuario de smartphone que realiza transferencias diarias de bajo monto, quiero completar el onboarding de la wallet con un flujo guiado y señales claras de siguiente paso, para poder empezar a pagar sin abandonar el proceso.
2. **Confirmacion de pagos**  
   Como pagador, quiero completar una transferencia de bajo monto y recibir una confirmacion definitiva del resultado, para confiar en si el pago se realizo o no.
3. **Pagos QR para comercios**  
   Como pequeño comercio que cobra con QR, quiero ver el estado confiable de cada transaccion de cliente, para decidir correctamente cuando entregar el producto o servicio.

El detalle original de estas epicas esta en [docs/epics.md](./docs/epics.md).

## Servicios locales

```text
wallet-db        PostgreSQL en localhost:5432
wallet-services  Flask en localhost:5000; GET /health verifica PostgreSQL
wallet-front     React/Vite en localhost:5173
```

Copiar `.env.example` a `.env` y cambiar la contrasena local antes de iniciar. La contrasena de respaldo definida en Compose es solo para desarrollo local.

Con Podman, desde la carpeta `wallet-hackathon`:

```powershell
podman machine start
podman compose up --build
```

`podman compose` requiere que haya un proveedor Compose instalado, como `podman-compose` o `docker-compose`.

## Estado

La base local de tres servicios esta configurada para desarrollo. Los contratos funcionales, las reglas de pago, el comportamiento de los agentes y los servicios de mensajeria siguen pendientes de definicion.
