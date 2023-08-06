# AlegraPy

Este paquete nos permite consumir el API del la plataforma de facturacion Alegra mediante python 🐍

## Características

- Permite leer facturas, pagos, productos, contactos
- Permite crear facturas, pagos, productos, contactos
- Permite borrar facturas, pagos, productos, contactos

## Instalación y uso

### 1. Obtener token de acceso
Debes seguir los siguientes pasos para obtener el token de acceso:

- Ingresar a la aplicación de [Alegra](https://www.alegra.com/).
- Haz clic sobre el vínculo "Configuración" en la parte superior derecha de la pantalla de Alegra y haz clic en la sección "API - Integraciones con otros sistemas"
- En la nueva pantalla puedes encontrar el correo con el cual debes acceder al API y el token. Si aún no cuentas con un token puedes generarlo también.

### 2. Instalación

En construcción...

### 3. Uso

Un ejemplo para usar este paquete

```py
from alegra import invoices,contacts, session

session.user = "your_email@domnain.com"
session.token = "your_token"

invoice = invoices()
invoice.read(1,fields='pdf')
invoice.list(0,3)

contact = contacts()
contact.read(12)
contact.list(0,2)
```

## Créditos

- Camilo Andrés Rodriguez

## referencias

- https://developer.alegra.com/


## Licencia

Este proyecto está bajo la Licencia [MIT].

---

¡Puedes personalizarlo según las necesidades específicas de tu proyecto!

