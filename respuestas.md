# Respuestas: dónde está cada cosa en el proyecto

Guía de **dónde se encuentra** cada pantalla, botón, cálculo y endpoint del proyecto *Presupuesto Estudiantil*, y **qué hace** cada uno.

> Todas las rutas son relativas a la carpeta `PRESUPUESTO ESTUDIANTIL/`.
> Los números de línea corresponden al estado actual del código.

---

## 1. Estructura general

| Parte | Carpeta / archivo | Qué contiene |
|---|---|---|
| Frontend (Vue 3 + Vite) | `FRONTEND/src/` | Pantallas, rutas, estilos |
| Rutas del frontend | `FRONTEND/src/router/index.js` | Qué URL abre qué pantalla y protección de la ruta privada |
| Barra superior (navbar) | `FRONTEND/src/App.vue` | Logo, menú, saludo, botón "Cerrar Sesión" |
| Pantalla de inicio | `FRONTEND/src/views/HomeView.vue` | Portada con "Empezar Gratis" y "Ver Demo" |
| Login | `FRONTEND/src/views/LoginView.vue` | Iniciar sesión / entrar a la demo |
| Registro | `FRONTEND/src/views/RegisterView.vue` | Crear cuenta |
| Recuperar contraseña | `FRONTEND/src/views/RecuperarView.vue` | 3 pasos: correo → código → nueva clave |
| **Mis Movimientos** | `FRONTEND/src/views/MovimientosView.vue` | Tarjetas de saldo, tabla, botón Registrar, modal de Gasto, **resta de cantidades** |
| Backend (FastAPI) | `BACKEND/main.py` | Arranca la API y registra los routers |
| Endpoints de usuarios | `BACKEND/routers/usuarios.py` | Registro, login, recuperación, `/auth/me` |
| Endpoints de movimientos | `BACKEND/routers/movimientos.py` | Listar, crear y eliminar movimientos |
| Endpoints de categorías | `BACKEND/routers/categorias.py` | Lista de categorías |
| Validación de datos | `BACKEND/schemas.py` | Forma de los datos que entran y salen |
| Tablas (ORM) | `BACKEND/models.py` | Usuario, Categoria, Movimiento |
| Token / contraseñas | `BACKEND/security.py` | Hash de claves y JWT |
| Base de datos | `BASE DE DATOS/schema.sql`, `seed.sql` | Creación de tablas y datos de ejemplo |

---

## 2. Rutas (URLs) de la aplicación

Archivo: `FRONTEND/src/router/index.js`

| URL | Pantalla | ¿Pública? |
|---|---|---|
| `/` | HomeView | Sí |
| `/login` | LoginView (con `?demo=1` entra en modo demo) | Sí |
| `/registro` | RegisterView | Sí |
| `/recuperar` | RecuperarView | Sí |
| `/movimientos` | MovimientosView | **No, requiere sesión** |
| cualquier otra | redirige a `/` | — |

**Protección de la ruta privada** (líneas 50–80):
- `validarSesion(token)` (línea 50) llama a `GET http://localhost:8000/auth/me` con el token.
- Si el token es válido → deja entrar y guarda el usuario en `localStorage`.
- Si no hay token o es inválido → borra `token` y `usuario` y manda a `/login?redirect=/movimientos`.
- Si ya tienes sesión y vas a `/login` o `/registro` → te manda directo a `/movimientos`.

---

## 3. Barra superior (navbar) — `FRONTEND/src/App.vue`

Hay **dos navbars**; se elige con `esRutaPrivada` (línea 73), que es `true` solo en `/movimientos`.

### 3.1 Navbar azul (dentro de la app, línea 3)
| Elemento | Línea | Qué hace |
|---|---|---|
| Logo "Presupuesto Estudiantil" | 6 | Lleva a `/movimientos` |
| Enlace **Inicio** | 11 | Lleva a `/` |
| Enlace **Mis Movimientos** | 12 | Lleva a `/movimientos` |
| Círculo con inicial (avatar) | 18 | Muestra la primera letra del nombre (`inicialUsuario`, línea 71) |
| Texto "¡Hola, *Nombre*!" | 19 | Muestra el primer nombre (`primerNombre`, línea 70) |
| Botón **Cerrar Sesión** | 21 | `cerrarSesion()` (línea 89): borra `token` y `usuario` de `localStorage` y va a `/login` |

### 3.2 Navbar clara (pantallas públicas, línea 26)
| Elemento | Línea | Qué hace |
|---|---|---|
| Logo | 28 | Lleva a `/` |
| Inicio / Funcionalidades / Precios / Ayuda | 34–37 | Saltan a secciones de la portada (`#inicio`, `#funcionalidades`…). Solo se ven en `/` |
| **Volver al Inicio** | 41 | Aparece fuera de `/`; lleva a `/` |
| **Iniciar Sesión** | 45 | Lleva a `/login` |
| **Crear Cuenta** | 46 | Lleva a `/registro` |

---

## 4. Pantalla de inicio — `FRONTEND/src/views/HomeView.vue`

| Elemento | Línea | Qué hace |
|---|---|---|
| Título "Toma el control de tu dinero universitario" | 7 | Texto principal |
| Botón **Empezar Gratis** | 17 | Lleva a `/registro` |
| Botón **Ver Demo ▶** | 18 | Lleva a `/login?demo=1` (rellena solo los datos de la cuenta demo) |
| Tarjetas "Control de Gastos", "Historial Detallado", "Alertas de Ahorro" | 28–50 | Solo informativas |

---

## 5. Login — `FRONTEND/src/views/LoginView.vue`

| Elemento | Línea | Qué hace |
|---|---|---|
| Pestaña **Iniciar Sesión** | 6 | Pestaña activa (no navega) |
| Pestaña **Registrarse** | 9 | Lleva a `/registro` |
| Aviso "Modo demo" | 14 | Solo aparece si la URL tiene `?demo=1` |
| Campo Correo | 24 | `v-model="email"` |
| Botón **Show/Hide Password** | 37 | Alterna `mostrarPassword` (muestra u oculta la clave) |
| Campo Contraseña | 43 | Cambia entre `password` y `text` según `mostrarPassword` |
| Ícono ojo 👁️/🙈 | 50 | Hace lo mismo que Show/Hide Password |
| Mensaje de error | 56 | Muestra `errorMsg` |
| Botón **Iniciar Sesión / Entrar a la Demo** | 60 | Envía el formulario → `handleLogin()` |
| Enlace **Recuperar aquí** | 67 | Lleva a `/recuperar` (oculto en demo) |
| Enlace **Regístrate gratis** | 71 | Lleva a `/registro` |

**Modo demo** (líneas 88–102): si `?demo=1`, rellena automáticamente
`estudiante@demo.com` / `estudiante123`.

**`handleLogin()`** (línea 104):
1. `POST http://localhost:8000/auth/login` con `{ email, password }`.
2. Si responde OK → guarda `token` y `usuario` en `localStorage`, avisa a la navbar (evento `usuario-autenticado`) y va a `/movimientos`.
3. Si falla → muestra "Correo o contraseña incorrectos." (viene del backend).
4. Si el backend está apagado → "No se pudo conectar con el servidor…".

---

## 6. Registro — `FRONTEND/src/views/RegisterView.vue`

| Elemento | Línea | Qué hace |
|---|---|---|
| Pestaña **Iniciar Sesión** | 6 | Lleva a `/login` |
| Campo Nombre Completo | 20 | `v-model="nombre"` |
| Campo Correo | 34 | `v-model="email"` |
| Campo Contraseña | 48 | `v-model="password"` (mínimo 6 caracteres) |
| Botón **Crear Cuenta** | 65 | `handleRegister()` |
| Enlace **Inicia sesión aquí** | 72 | Lleva a `/login` |

**`handleRegister()`** (línea 95): `POST /auth/registro` → si sale bien muestra
"¡Cuenta creada con éxito! Redirigiendo...", guarda token y usuario y, a los 1,2 s, va a `/movimientos`.
Si el correo ya existe, el backend responde "Ya existe una cuenta con este correo…".

---

## 7. Recuperar contraseña — `FRONTEND/src/views/RecuperarView.vue`

Tiene **3 pasos** (variable `paso`, línea 138). Los 3 puntitos de arriba (línea 13) muestran el progreso.

### Paso 1 — Correo (línea 16)
| Elemento | Línea | Qué hace |
|---|---|---|
| Campo Correo Registrado | 22 | `v-model="email"` |
| Botón **Enviar código** | 33 | `enviarCodigo()` (línea 167) → `POST /auth/recuperar/solicitar` y pasa al paso 2 |
| **← Volver a Iniciar Sesión** | 38 | Lleva a `/login` |

### Paso 2 — Código de 4 dígitos (línea 44)
| Elemento | Línea | Qué hace |
|---|---|---|
| 4 casillas del código | 52 | `alEscribir()` (línea 184) solo acepta números y salta a la siguiente casilla; `alBorrar()` (línea 189) retrocede con Backspace; `pegarCodigo()` (línea 197) permite pegar el código completo |
| Botón **Verificar código** | 69 | `verificarCodigo()` (línea 208) → `POST /auth/recuperar/verificar`. Está desactivado hasta tener 4 dígitos |
| Botón **Reenviar código** | 74 | Vuelve a llamar `enviarCodigo()` |
| Botón **Cambiar correo** | 78 | `volverAlPaso1()` (línea 203) |

### Paso 3 — Nueva contraseña (línea 84)
| Elemento | Línea | Qué hace |
|---|---|---|
| Nueva Contraseña / Confirmar | 90, 104 | Dos campos |
| Botón **Cambiar Contraseña** | 116 | `guardarNuevaPassword()` (línea 221): valida mínimo 6 caracteres y que coincidan → `POST /auth/recuperar/restablecer` → a los 1,5 s va a `/login` |

### Reglas del backend (`BACKEND/routers/usuarios.py`)
- El código es de **4 dígitos aleatorios** (línea 86) y se guarda **hasheado**.
- **Vence en 10 minutos** (`CODIGO_MINUTOS = 10`, línea 11).
- **Máximo 5 intentos** (`CODIGO_MAX_INTENTOS = 5`, línea 12). Cada fallo dice "Te quedan N intentos".
- La cuenta demo **no puede** recuperar contraseña (línea 79, error 403).
- El correo se envía con `BACKEND/correo.py`.

---

## 8. Mis Movimientos — `FRONTEND/src/views/MovimientosView.vue` ⭐

Esta es la pantalla principal. Funciona distinto para **cuenta normal** y **cuenta demo**
(`esDemo`, línea 319, viene de `usuario.es_demo`).

### 8.1 Título y aviso demo
| Elemento | Línea | Qué hace |
|---|---|---|
| Título **Mis Movimientos** | 6 | Texto |
| Banner "Estás viendo una demo…" | 9 | Solo en demo |
| Botón **crea tu cuenta gratis** (dentro del banner) | 11 | `salirDemo()` (línea 347): borra la sesión demo y va a `/registro` |

### 8.2 Las 3 tarjetas de resumen (líneas 14–43)
| Tarjeta | Línea | Valor que muestra | Color |
|---|---|---|---|
| **Saldo Disponible** | 16–23 | `saldoTotal` | azul marino |
| **Ingresos del Mes** | 25–32 | `ingresosTotal` | celeste |
| **Gastos del Mes** | 34–41 | `gastosTotal` | rojo |

- En cuenta normal se muestra en **Bs** (ej. `675.00 Bs`).
- En demo se muestra en **$** (ej. `$120.00`).
- Siempre con 2 decimales (`.toFixed(2)`).
- Los textos "Actualizado hoy" y "Octubre 2026" están **escritos fijos** en el HTML (líneas 21, 30, 39).

### 8.3 🧮 LA RESTA DE LAS CANTIDADES (cómo se calcula el saldo)

Todo está en el `<script setup>`, líneas 306–389.

**a) Saldo base** — línea 313:
```js
const SALDO_BASE = 700
```
El usuario **empieza con 700 Bs**. Si cambias ese número, cambia el saldo inicial.

**b) Total de gastos** — líneas 370–376 (`gastosTotal`):
```js
listaMovimientos.value
  .filter(m => m.tipo === 'gasto')                       // solo los gastos
  .reduce((sum, item) => sum + Number(item.monto || 0), 0) // los suma
```

**c) Total de ingresos** — líneas 378–384 (`ingresosTotal`): igual, pero con `tipo === 'ingreso'`.

**d) Saldo disponible (la resta)** — líneas 386–389 (`saldoTotal`):
```js
return SALDO_BASE + ingresosTotal.value - gastosTotal.value
```

👉 **Fórmula:** `Saldo = 700 + Ingresos − Gastos`

**Ejemplo:**
| Acción | Gastos | Saldo |
|---|---|---|
| Al empezar | 0 Bs | 700 − 0 = **700 Bs** |
| Registro gasto de 25 Bs (Transporte) | 25 Bs | 700 − 25 = **675 Bs** |
| Registro gasto de 10,50 Bs (Almuerzo) | 35,50 Bs | 700 − 35,50 = **664,50 Bs** |

Son `computed` de Vue: **se recalculan solos** cada vez que cambia `listaMovimientos`,
así que al guardar un gasto las 3 tarjetas se actualizan al instante.

**En modo demo** no se usa esta fórmula: los tres valores vienen ya calculados del backend
(`saldoDemo`, `ingresosDemo`, `gastosDemo`, líneas 365–367, rellenados en `cargarMovimientos()`, línea 404).

**En el backend** (`BACKEND/routers/movimientos.py`, líneas 29–62) también se calcula:
```python
saldo = round(ingresos - gastos, 2)   # línea 55
```
⚠️ Ojo: el backend **no** suma los 700 de base; la base de 700 solo existe en el frontend.

### 8.4 Botón **+ Registrar Movimiento** (líneas 45–54)
- Al hacer clic: `abrirModal = true` → abre el modal.
- En demo está **desactivado** (`:disabled="esDemo"`) con el mensaje "No disponible en modo demo".
- Estilos: `.btn-new-mov` (línea 688 del `<style>`).

### 8.5 Tabla de movimientos — cuenta normal (líneas 57–105)
Columnas: **MOVIMIENTO | DESCRIPCION | FECHA | ACCIONES**

| Columna | Línea | Qué muestra |
|---|---|---|
| MOVIMIENTO | 79–83 | Etiqueta tipo "Gasto 25Bs" o "Ingreso 100Bs" — función `formatearMovimientoTexto()` (línea 504). Rojo si es gasto (`.badge-gasto-bs`), verde si es ingreso (`.badge-ingreso-bs`). Si el monto es entero no muestra decimales |
| DESCRIPCION | 85–87 | El texto escrito en el modal |
| FECHA | 88–90 | Convierte `2026-10-01` → **"1 de Octubre"** con `formatearFechaEspanol()` (línea 511) |
| ACCIONES | 91–102 | Botón de **papelera 🗑️** |

- **Botón papelera** (línea 92): está **desactivado** (`disabled`, tooltip "Acción deshabilitada"). Por ahora **no borra nada**. Existe la función `eliminarMovimientoItem(id)` (línea 587) que sí borraría (quita de la lista, de `localStorage` y llama `DELETE /movimientos/{id}`), pero **no está conectada** al botón.
- **Estado vacío** (líneas 68–76): si no hay movimientos muestra 💳 "No hay movimientos registrados — Presiona el botón '+ Registrar Movimiento'…".

### 8.6 Tabla de movimientos — cuenta demo (líneas 108–131)
Columnas: **FECHA | DESCRIPCIÓN | CATEGORÍA | MONTO**
- Categoría con color según `badgeClass()` (línea 448): Comida, Transporte, Libros, Ingreso.
- Monto con `+$` verde si es ingreso y `-$` rojo si es gasto.

### 8.7 Modal **Gasto** — cuenta normal (líneas 210–302)

Se abre con "+ Registrar Movimiento". Título **Gasto** con ícono de $ y subtítulo "Registra los detalles del gasto universitario".

| Elemento | Línea | Qué hace |
|---|---|---|
| Botón **✕** (cerrar) | 222 | `cerrarModalGasto()` (línea 499): cierra y limpia el error |
| Clic fuera del modal | 210 | También cierra (`@click.self`) |
| Campo **Cantidad** (con prefijo "Bs") | 229–242 | `cantidadGasto`, número mayor a 0 |
| Campo **Descripción** | 245–254 | `descripcionGasto` (ej. "Transporte") |
| Campo **Día** | 258–269 | `diaGasto`, del 1 al 31 |
| Selector **Mes** | 271–277 | `mesGasto`, Enero…Diciembre (por defecto Octubre) |
| Mensaje de error | 281 | "Por favor completa la cantidad y la descripción." |
| Botón **Cancelar** | 284 | `cerrarModalGasto()` |
| Botón **Guardar** | 287 | Envía el formulario → `guardarGastoEstudiantil()`. Mientras guarda dice "Guardando..." y se desactiva |

**Qué hace `guardarGastoEstudiantil()`** (línea 527), paso a paso:
1. Valida que haya cantidad y descripción.
2. Arma la fecha: año **2026** fijo + mes elegido + día → `"2026-10-01"` (líneas 536–541).
3. Crea el gasto con `tipo: 'gasto'` y categoría fija **'Transporte'** (línea 546).
4. Lo pone **al inicio** de la lista y lo guarda en `localStorage` (líneas 553–554) → **aquí se dispara la resta** del saldo.
5. Lo envía al backend: `POST /movimientos` (línea 556). Si responde OK, actualiza el `id` con el de la base de datos.
6. Si el servidor está apagado, **igual queda guardado localmente**.
7. Al final limpia el formulario (cantidad vacía, día 1, mes Octubre) y cierra el modal.

### 8.8 Modal en modo demo (líneas 136–207)
Tiene botones **Gasto / Ingreso** (eligen el tipo), Descripción, Categoría (según el tipo), Monto ($), **Cancelar** y **Guardar Movimiento** (`guardarMovimiento()`, línea 456). En la práctica no se abre porque el botón está desactivado en demo, y el backend además bloquea con 403.

### 8.9 Guardado local (localStorage)
- Clave por usuario: `movimientos_<email>` (`storageKey`, línea 322).
- `guardarEnStorage()` (línea 327) y `cargarDeStorage()` (línea 337).
- La lista arranca con lo guardado localmente (línea 361), así **no se pierde al recargar** la página.
- Al montar la pantalla (`onMounted`, línea 600) se llama a `cargarMovimientos()` y `cargarCategorias()`.
- Si el backend responde **401** (token vencido) → `sesionExpirada()` (línea 398) cierra la sesión y manda a `/login`.

---

## 9. Backend — endpoints (API en `http://localhost:8000`)

Documentación automática: `http://localhost:8000/docs`

### 9.1 Usuarios — `BACKEND/routers/usuarios.py` (prefijo `/auth`)
| Método | Ruta | Qué hace |
|---|---|---|
| POST | `/auth/registro` | Crea la cuenta y devuelve token + usuario |
| POST | `/auth/login` | Verifica correo/clave y devuelve token + usuario |
| POST | `/auth/recuperar/solicitar` | Genera y envía el código de 4 dígitos |
| POST | `/auth/recuperar/verificar` | Comprueba el código |
| POST | `/auth/recuperar/restablecer` | Cambia la contraseña |
| GET | `/auth/me` | Devuelve el usuario del token (se usa para proteger `/movimientos`) |

### 9.2 Movimientos — `BACKEND/routers/movimientos.py` (prefijo `/movimientos`, requieren token)
| Método | Ruta | Línea | Qué hace |
|---|---|---|---|
| GET | `/movimientos` | 19 | Lista los movimientos del usuario (más recientes primero) y calcula ingresos, gastos y `saldo = ingresos − gastos` |
| POST | `/movimientos` | 64 | Crea un movimiento. Si no mandas categoría usa "General"; si no mandas tipo usa "gasto"; si no mandas fecha usa la de hoy. La fecha llega en formato `AAAA-MM-DD` |
| DELETE | `/movimientos/{id}` | 105 | Borra un movimiento del usuario (404 si no existe) |

- `bloquear_demo()` (línea 12): si el usuario es la cuenta demo, **prohíbe crear o borrar** (error 403).

### 9.3 Categorías — `BACKEND/routers/categorias.py`
| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/categorias` | Devuelve las categorías de la BD; si está vacía devuelve 7 por defecto (Comida y Almuerzo, Transporte, Libros y Copias, Ocio y Salidas, Beca Mensual, Apoyo Familiar, Ingresos) |

### 9.4 Seguridad — `BACKEND/security.py`
- Contraseñas guardadas con **hash** (`hash_password`, línea 20).
- Token **JWT** con algoritmo HS256, dura **1440 minutos (24 h)** (línea 16).
- `get_current_user()` (línea 35) lee el token `Bearer` y devuelve el usuario.

### 9.5 Datos (schemas) — `BACKEND/schemas.py`
- `MovimientoCreate`: `descripcion`, `categoria` (opcional, "General"), `monto`, `tipo` (opcional, "gasto"), `fecha` (opcional).
- `ResumenFinanciero`: `saldo_disponible`, `ingresos_del_mes`, `gastos_del_mes`, `movimientos`.

---

## 10. Base de datos

### Tablas (`BACKEND/models.py` y `BASE DE DATOS/schema.sql`)
| Tabla | Campos principales |
|---|---|
| `usuarios` | id, nombre, email (único), password_hash, token_recuperacion, codigo_expira, codigo_intentos, creado_en |
| `categorias` | id, nombre, tipo (gasto/ingreso), icono |
| `movimientos` | id, usuario_id, categoria_id, monto (2 decimales), tipo, descripcion, fecha, creado_en |

- Si se borra un usuario, se borran sus movimientos (`CASCADE`).
- La cuenta demo es la que tiene el correo **`estudiante@demo.com`** (`models.py`, línea 6).
- `BASE DE DATOS/seed.sql` carga categorías, la cuenta demo y movimientos de ejemplo.

---

## 11. Cosas a tener en cuenta (limitaciones actuales)

1. **Botón papelera desactivado**: todavía no elimina movimientos.
2. **Categoría fija**: todo gasto registrado desde el modal se guarda como "Transporte".
3. **Año fijo 2026** en la fecha del gasto.
4. **Solo gastos**: en cuenta normal el modal solo registra gastos (no ingresos).
5. **Saldo base de 700 Bs solo en el frontend**; el backend calcula el saldo sin esa base.
6. "Ingresos/Gastos **del Mes**" en realidad suman **todos** los movimientos, no solo los del mes actual.
7. Los textos "Octubre 2026" y "Actualizado hoy" de las tarjetas son fijos.
