# Tarea 1 - Implementación del Manejo de Acceso

**Aplicación Elegida:** Presupuesto Estudiantil  
**Estudiante:** Carmen Jenifer Aranibar Fernandez  
**Materia:** Interacción Humano-Computador (IHC) - Proyecto 2  
**Modalidad:** P2 (con IA)  

---

## 1. Decisiones de Arquitectura y Tecnologías

* **Frontend: Vue 3 con Vite y Vue Router.** Se implementó una Single Page Application (SPA) con Single File Components (`.vue`). Vue Router maneja la ruta pública, las pantallas de acceso y la ruta privada sin recargar la página.
* **Backend: FastAPI (Python) con SQLAlchemy.** API REST rápida, con validación de datos mediante Pydantic y documentación interactiva automática en `/docs`.
* **Base de Datos: PostgreSQL 16.** Modelo relacional con las tablas `usuarios`, `categorias` y `movimientos`. Cada movimiento pertenece a un usuario, por lo que cada persona solo ve sus propios datos.
* **Contraseñas:** se guardan cifradas (hash scrypt con Werkzeug), nunca en texto plano.
* **Sesión:** al iniciar sesión el backend entrega un token JWT que se guarda en el navegador (`localStorage`). Al recargar la página, la guardia de Vue Router valida ese token con el backend (`GET /auth/me`) antes de abrir la ruta privada; si no existe, es falso o venció, se borra y se redirige al login.
* **Recuperación de contraseña con código por correo:** el backend genera un código aleatorio de 4 dígitos y lo envía al correo de la cuenta por SMTP (Gmail). El código se guarda cifrado, vence a los 10 minutos, permite máximo 5 intentos y solo sirve una vez. La respuesta es la misma exista o no la cuenta, para no revelar qué correos están registrados. Si no se configura un correo en el `.env`, el código se muestra en la terminal del backend.
* **Modo demo de solo lectura:** el botón "Ver Demo" entra con una cuenta de ejemplo que muestra datos, pero no puede registrar movimientos ni cambiar su contraseña. Esta restricción se aplica en el frontend (botón deshabilitado) y también en el backend.
* **Configuración segura:** las contraseñas de PostgreSQL y de Gmail van en el archivo `.env`, que no se sube al repositorio. Se incluye la plantilla `.env.example`.
* **Estilos y Usabilidad (IHC):** paleta de azul marino (`#154C86`, `#10233F`) y verde azulado (`#2E7D9A`), con fondos en degradado celeste y lila en las pantallas de acceso. Se usan ilustraciones e íconos (estudiante, billetera, gráficos, campana, monedas) y un logo propio (birrete sobre una moneda). Los mensajes de error y de éxito son claros, y el diseño se adapta a pantallas grandes y pequeñas.

---

## 2. Archivos Principales del Proyecto

### Base de Datos (`PRESUPUESTO ESTUDIANTIL/BASE DE DATOS/`)
* `schema.sql`: crea las tablas `usuarios` (incluye las columnas del código de recuperación: `token_recuperacion`, `codigo_expira` y `codigo_intentos`), `categorias` y `movimientos`.
* `seed.sql`: carga las categorías de gastos e ingresos, la cuenta demo (`estudiante@demo.com`) y sus movimientos de ejemplo.

### Backend (`PRESUPUESTO ESTUDIANTIL/BACKEND/`)
* `main.py`: punto de entrada de FastAPI, configuración de CORS para `http://localhost:5173` y registro de las rutas.
* `database.py`: conexión a PostgreSQL y generador de sesiones `get_db`.
* `models.py`: modelos de las tablas y la propiedad `es_demo` que identifica la cuenta demo.
* `schemas.py`: validación de los datos que entran y salen de la API.
* `security.py`: cifrado y verificación de contraseñas, creación y validación de tokens JWT y la dependencia `get_current_user`.
* `correo.py`: envío del código de recuperación por correo (SMTP) con un mensaje en HTML.
* `routers/usuarios.py`: registro (`POST /auth/registro`), inicio de sesión (`POST /auth/login`), usuario actual (`GET /auth/me`) y recuperación de contraseña en tres pasos (`POST /auth/recuperar/solicitar`, `/auth/recuperar/verificar` y `/auth/recuperar/restablecer`).
* `routers/movimientos.py`: lista de movimientos con el saldo, los ingresos y los gastos (`GET /movimientos`), registro (`POST`) y eliminación (`DELETE`), bloqueados para la cuenta demo.
* `routers/categorias.py`: lista de categorías (`GET /categorias`).
* `.env.example`: plantilla de configuración (base de datos, clave secreta y correo).

### Frontend (`PRESUPUESTO ESTUDIANTIL/FRONTEND/`)
* `src/router/index.js`: rutas de la aplicación y guardia `beforeEach` que valida la sesión con el backend antes de abrir `/movimientos`; si no hay sesión válida, redirige a `/login`.
* `src/App.vue`: barra superior. En las rutas públicas muestra el logo y los botones de acceso; en la ruta privada muestra el saludo "¡Hola, nombre!", un círculo con la inicial de la persona y el botón "Cerrar Sesión".
* `src/style.css`: estilos generales de la aplicación.
* `src/assets/`: logo, ilustración del estudiante e íconos de las tarjetas.
* `src/views/HomeView.vue`: **ruta pública** con la presentación de la app y los botones "Empezar Gratis" y "Ver Demo".
* `src/views/LoginView.vue`: inicio de sesión; con "Ver Demo" se abre en modo demo con los datos de ejemplo.
* `src/views/RegisterView.vue`: registro de una cuenta nueva.
* `src/views/RecuperarView.vue`: recuperación de contraseña en tres pasos: correo, código de 4 dígitos y nueva contraseña.
* `src/views/MovimientosView.vue`: **ruta privada "Mis movimientos"** con las tarjetas de saldo, ingresos y gastos, el registro de movimientos y la tabla con los datos reales de la persona desde PostgreSQL. En modo demo el botón de registro aparece deshabilitado.

---

## 3. Verificación de Cumplimiento de la Rúbrica

| Requisito obligatorio                       | Estado   | Cómo se cumple                                                                          |
| :------------------------------------------ | :------: | :-------------------------------------------------------------------------------------- |
| **Registro de cuenta nueva**                | Cumplido | Pantalla "Crear Cuenta" (`RegisterView.vue`) y ruta `POST /auth/registro`               |
| **Inicio de sesión**                        | Cumplido | Pantalla de login (`LoginView.vue`) y ruta `POST /auth/login`                           |
| **Cierre de sesión**                        | Cumplido | Botón "Cerrar Sesión" de la barra superior: borra la sesión y lleva a `/login`          |
| **Recuperación y cambio de contraseña**     | Cumplido | Código de 4 dígitos enviado al correo (`RecuperarView.vue` y rutas `/auth/recuperar/*`) |
| **Sesión conservada al recargar**           | Cumplido | El token queda guardado y se valida con `GET /auth/me` al recargar (F5)                 |
| **Ruta pública**                            | Cumplido | Página de inicio (`/`), se abre sin iniciar sesión                                      |
| **Ruta privada que redirige al login**      | Cumplido | `/movimientos` exige sesión válida; sin ella lleva a `/login`                           |
| **Nombre de la persona en la ruta privada** | Cumplido | Saludo "¡Hola, nombre!" con su inicial en la barra superior                             |
