## Proyecto2

# Presupuesto Estudiantil

Aplicación web para que estudiantes registren sus ingresos y gastos y controlen su dinero.
Proyecto 2 de Interacción Humano-Computador (IHC) · Tarea 1: manejo de acceso.

**Estudiante:** Carmen Jenifer Aranibar Fernandez

- El frontend está hecho con **Vue 3** 
- El backend con **FastAPI** (Python)
- La base de datos es **PostgreSQL**.

---

## 1. Requisitos previos
**Para ejecutar el proyecto se necesitan dos terminales abiertas al mismo tiempo**: una para el backend y otra para el frontend.
Todos los comandos se escriben estando en la carpeta principal del proyecto (`PROYECTO2-IHC`).

---

## 2. Base de datos (PostgreSQL)

Primero hay que crear la base de datos llamada `presupuesto_estudiantil` y cargarle las tablas y los datos.

---

## 3. Backend (FastAPI) · en la primera terminal
### 3.1 Instalar lo que necesita el backend

El entorno virtual es una carpeta llamada `venv` donde se instalan las librerías del proyecto sin mezclarlas con otras:

```bash
cd "PRESUPUESTO ESTUDIANTIL/BACKEND"
python -m venv venv
```

Después hay que activar ese entorno virtual. Con el entorno activado, se instalan todas las librerías del backend con este comando:

```bash
pip install -r requirements.txt
```

### 3.2 Crear el archivo `.env` (obligatorio)

El backend necesita un archivo llamado `.env`, donde se guardan las contraseñas.
Este archivo hay que crearlo copiando la plantilla `.env.example`, que viene en el proyecto.
Después hay que abrir el archivo `.env` y completar tres cosas:

**Primero, la contraseña de PostgreSQL (obligatorio).**

**Segundo, la clave secreta (recomendado).**
En la línea `SECRET_KEY` se puede escribir cualquier texto largo e inventado; sirve para proteger las sesiones de los usuarios.
Si se deja como está, el proyecto funciona igual.

**Tercero, el correo que envía los códigos (opcional).**
Las líneas `SMTP_USER` y `SMTP_PASSWORD` sirven para que el código de recuperación de contraseña llegue por correo. Si se dejan **vacías**, la aplicación funciona igual: el código de 4 dígitos aparece escrito en la terminal del backend,
  con un mensaje como este: `[MODO DESARROLLO] Código de recuperación para correo@ejemplo.com: 1548`

### 3.3 Ejecutar el backend

```bash
python -m uvicorn main:app --reload
```

Debe aparecer `✓ Conexión exitosa a PostgreSQL`.

---

## 4. Frontend (Vue 3) · Terminal 2

```bash
cd "PRESUPUESTO ESTUDIANTIL/FRONTEND"
npm install
npm run dev
```

Abrir **http://localhost:5173** en el navegador.

> El frontend se comunica con el backend en `http://localhost:8000`.
> Ambos deben estar encendidos y en esos puertos.

---

## 5. Probar la aplicación

**Cuenta demo** (botón **"Ver Demo"** en la página de inicio):

Correo = `estudiante@demo.com` 
Contraseña = `estudiante123` 

La cuenta demo es de solo lectura, muestra datos de ejemplo, no permite registrar movimientos ni cambiar la contraseña. Para probar todo, crear una cuenta nueva con **"Crear Cuenta"**.


## 6. Pruebas Unitarias Automatizadas (Tarea 2)

Para ejecutar las 4 pruebas unitarias que verifican la regla de cambio de estado (`Pendiente` -> `Pagado` y acción `"Marcar como pagado"`) en la terminal pon:

```bash
cd "PRESUPUESTO ESTUDIANTIL/BACKEND"
python -m pytest -v tests/test_estado_movimiento.py -p no:warnings
```

Las pruebas validan automáticamente:
1. `test_01_estado_inicial_es_correcto`: El estado inicial de un gasto nuevo es `pendiente`.
2. `test_02_accion_realiza_transicion_esperada`: La acción `"Marcar como pagado"` cambia el estado a `pagado`.
3. `test_03_transicion_invalida_se_rechaza`: Si un gasto ya está en `pagado`, la acción es rechazada con HTTP 400.
4. `test_04_demas_datos_del_elemento_se_conservan`: El monto, descripción, fecha y usuario no se modifican al cambiar el estado.

Para más detalles, consulta [task-02-state-tests.md](task-02-state-tests.md).

---

## 7. Estructura del proyecto

```
PROYECTO2-IHC/
├── docs/
│   ├── README.md                 ← este archivo (instalación, ejecución y pruebas)
│   ├── task-01-access.md         ← Documentación Tarea 1 (Manejo de acceso)
│   └── task-02-state-tests.md    ← Documentación Tarea 2 (Máquina de estados y pruebas)
└── PRESUPUESTO ESTUDIANTIL/
    ├── BASE DE DATOS/            ← schema.sql (tablas) y seed.sql (datos de ejemplo)
    ├── BACKEND/                  ← API FastAPI, modelos, routers y tests/
    │   └── tests/                ← test_estado_movimiento.py (4 pruebas unitarias)
    └── FRONTEND/                 ← App Vue 3 (vistas, componentes y estilos)
```
