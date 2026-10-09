# BACKEND - EXPLICACIÓN LÍNEA POR LÍNEA

Documento explicativo línea por línea de todo el código del **Backend** del proyecto *Presupuesto Estudiantil* (FastAPI + SQLAlchemy + SQLite / PostgreSQL).

---

## Índice de Contenidos

1. [Carpeta: routers](#1-carpeta-routers)
   - [categorias.py](#categoriaspy)
   - [movimientos.py](#movimientospy)
   - [usuarios.py](#usuariospy)
2. [Carpeta: Raíz del Backend (BACKEND/)](#2-carpeta-raíz-del-backend-backend)
   - [main.py](#mainpy)
   - [database.py](#databasepy)
   - [models.py](#modelspy)
   - [schemas.py](#schemaspy)
   - [security.py](#securitypy)
   - [correo.py](#correopy)
3. [Carpeta: tests](#3-carpeta-tests)
   - [test_estado_movimiento.py](#test_estado_movimientopy)

---

# 1. Carpeta: routers

## categorias.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/routers/categorias.py`  
Total de líneas: 24

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `from fastapi import APIRouter, Depends` | Importa `APIRouter` para agrupar endpoints bajo un prefijo común y `Depends` para inyección de dependencias. |
| 2 | `from sqlalchemy.orm import Session` | Importa el tipo `Session` de SQLAlchemy para manejar operaciones en la base de datos. |
| 3 | `from typing import List` | Importa `List` para definir listas tipadas en la respuesta de la API. |
| 4 | `from database import get_db` | Importa la función que provee la sesión activa de la base de datos. |
| 5 | `import models` | Importa los modelos ORM para poder consultar la tabla `categorias`. |
| 6 | `import schemas` | Importa los esquemas de Pydantic para validar y estructurar la salida de datos hacia el frontend. |
| 7 | *(Línea en blanco)* | Línea vacía para separar las importaciones de la definición del enrutador. |
| 8 | `router = APIRouter(prefix="/categorias", tags=["Categorías"])` | Crea el enrutador HTTP bajo la ruta base `/categorias` y le asigna la etiqueta "Categorías" para la documentación Swagger. |
| 9 | *(Línea en blanco)* | Línea vacía para separar la declaración del enrutador de las funciones. |
| 10 | `@router.get("", response_model=List[schemas.CategoriaOut])` | Decorador que define un endpoint HTTP GET en `/categorias`, indicando que devolverá una lista estructurada según `CategoriaOut`. |
| 11 | `def listar_categorias(db: Session = Depends(get_db)):` | Define la función controladora recibiendo automáticamente la sesión de la base de datos inyectada. |
| 12 | `    categorias = db.query(models.Categoria).all()` | Consulta y obtiene todas las filas guardadas en la tabla `categorias` de la base de datos. |
| 13 | `    if not categorias:` | Comprueba si la consulta devolvió una lista vacía (si aún no se han cargado categorías en la base de datos). |
| 14 | `        return [` | Inicia el retorno de una lista de categorías fijas de respaldo en caso de que la tabla esté vacía. |
| 15 | `            {"id": 1, "nombre": "Comida y Almuerzo", "tipo": "gasto", "icono": "utensils"},` | Categoría 1: Gasto de alimentación universitaria con icono de tenedor y cuchillo. |
| 16 | `            {"id": 2, "nombre": "Transporte", "tipo": "gasto", "icono": "bus"},` | Categoría 2: Gasto de pasajes y transporte público con icono de autobús. |
| 17 | `            {"id": 3, "nombre": "Libros y Copias", "tipo": "gasto", "icono": "book-open"},` | Categoría 3: Gasto académico en material de estudio con icono de libro abierto. |
| 18 | `            {"id": 4, "nombre": "Ocio y Salidas", "tipo": "gasto", "icono": "coffee"},` | Categoría 4: Gasto recreativo y café con icono de taza. |
| 19 | `            {"id": 5, "nombre": "Beca Mensual", "tipo": "ingreso", "icono": "award"},` | Categoría 5: Ingreso por beca universitaria con icono de medalla de honor. |
| 20 | `            {"id": 6, "nombre": "Apoyo Familiar", "tipo": "ingreso", "icono": "heart"},` | Categoría 6: Ingreso de dinero enviado por la familia con icono de corazón. |
| 21 | `            {"id": 7, "nombre": "Ingresos", "tipo": "ingreso", "icono": "dollar-sign"}` | Categoría 7: Ingreso general de dinero con icono de signo de dólar. |
| 22 | `        ]` | Cierra la lista de categorías predeterminadas de respaldo. |
| 23 | `    return categorias` | Si la base de datos sí tenía categorías registradas, las retorna directamente. |
| 24 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## movimientos.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/routers/movimientos.py`  
Total de líneas: 150

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `from fastapi import APIRouter, Depends, HTTPException, status` | Importa utilidades de FastAPI: enrutador, dependencias, manejo de errores HTTP y códigos de estado. |
| 2 | `from sqlalchemy.orm import Session` | Importa el tipo `Session` de SQLAlchemy para manejar operaciones en base de datos. |
| 3 | `from datetime import datetime` | Importa la clase `datetime` para manipular fechas y horas del sistema. |
| 4 | `from database import get_db` | Importa la función proveedora de la conexión activa a la base de datos. |
| 5 | `import models` | Importa los modelos ORM (`Usuario`, `Movimiento`, `Categoria`). |
| 6 | `import schemas` | Importa los esquemas de Pydantic que validan las entradas y salidas de datos. |
| 7 | `from security import get_current_user` | Importa la función de autenticación que valida el token JWT y obtiene el usuario conectado. |
| 8 | *(Línea en blanco)* | Línea vacía para separar importaciones. |
| 9 | `router = APIRouter(prefix="/movimientos", tags=["Movimientos Estudiantiles"])` | Crea el enrutador para agrupar las rutas bajo el prefijo `/movimientos` con la etiqueta "Movimientos Estudiantiles". |
| 10 | *(Línea en blanco)* | Línea vacía de separación. |
| 11 | `def bloquear_demo(usuario: models.Usuario):` | Declara la función auxiliar que impide cambios a la cuenta de prueba de demostración. |
| 12 | `    if usuario.es_demo:` | Evalúa si la propiedad `es_demo` del usuario autenticado es verdadera (`estudiante@demo.com`). |
| 13 | `        raise HTTPException(` | Lanza una excepción HTTP que interrumpe la petición. |
| 14 | `            status_code=status.HTTP_403_FORBIDDEN,` | Asigna el código de error HTTP 403 (Prohibido). |
| 15 | `            detail="Modo demo: no se pueden registrar ni modificar movimientos."` | Mensaje informativo explicando que la cuenta demo es exclusivamente de lectura. |
| 16 | `        )` | Cierra la llamada de `HTTPException`. |
| 17 | *(Línea en blanco)* | Línea vacía de separación. |
| 18 | `@router.get("", response_model=schemas.ResumenFinanciero)` | Endpoint HTTP GET en `/movimientos` que responde con el resumen financiero (`ResumenFinanciero`). |
| 19 | `def listar_movimientos(` | Declara la función controladora para consultar los movimientos del usuario actual. |
| 20 | `    db: Session = Depends(get_db),` | Inyecta la sesión de la base de datos como dependencia. |
| 21 | `    usuario: models.Usuario = Depends(get_current_user)` | Inyecta el usuario autenticado que realiza la petición. |
| 22 | `):` | Cierra los argumentos de la función `listar_movimientos`. |
| 23 | `    movimientos_db = db.query(models.Movimiento)\` | Inicia una consulta en la base de datos sobre la tabla `movimientos`. |
| 24 | `        .filter(models.Movimiento.usuario_id == usuario.id)\` | Filtra únicamente los movimientos que pertenecen al usuario que inició sesión. |
| 25 | `        .order_by(models.Movimiento.fecha.desc(), models.Movimiento.id.desc())\` | Ordena los registros del más reciente al más antiguo por fecha y por ID. |
| 26 | `        .all()` | Ejecuta la consulta y trae todos los registros encontrados como una lista. |
| 27 | *(Línea en blanco)* | Línea vacía de separación. |
| 28 | `    movimientos_out = []` | Inicializa una lista vacía para almacenar los movimientos formateados que se enviarán al cliente. |
| 29 | `    ingresos = 0.0` | Inicializa en cero el total acumulado de ingresos. |
| 30 | `    gastos = 0.0` | Inicializa en cero el total acumulado de gastos efectivamente pagados. |
| 31 | *(Línea en blanco)* | Línea vacía de separación. |
| 32 | `    for m in movimientos_db:` | Itera sobre cada registro de movimiento retornado por la base de datos. |
| 33 | `        monto_float = float(m.monto)` | Convierte el monto de la base de datos (decimal) a número de punto flotante de Python. |
| 34 | `        estado_val = getattr(m, "estado", "pendiente") or "pendiente"` | Lee de forma segura el atributo `estado`, asignando `'pendiente'` si no tiene valor. |
| 35 | `        if m.tipo == "ingreso":` | Comprueba si el tipo de transacción es un ingreso. |
| 36 | `            ingresos += monto_float` | Suma el monto directamente a la bolsa de ingresos totales. |
| 37 | `        else:` | Bloque alternativo para cuando la transacción es de tipo gasto. |
| 38 | `            if estado_val == "pagado":` | Aplica la regla contable de la Tarea 2: solo los gastos con estado `'pagado'` se descuentan del balance. |
| 39 | `                gastos += monto_float` | Suma el monto al acumulador de gastos pagados. |
| 40 | *(Línea en blanco)* | Línea vacía de separación. |
| 41 | `        categoria_nombre = "General"` | Asigna "General" como nombre predeterminado de categoría. |
| 42 | `        if m.categoria_id:` | Comprueba si el movimiento tiene una clave foránea de categoría asignada. |
| 43 | `            cat = db.query(models.Categoria).filter(models.Categoria.id == m.categoria_id).first()` | Busca en la base de datos los datos de la categoría mediante su ID. |
| 44 | `            if cat:` | Si se encontró el registro de la categoría. |
| 45 | `                categoria_nombre = cat.nombre` | Asigna el nombre real de la categoría encontrada. |
| 46 | *(Línea en blanco)* | Línea vacía de separación. |
| 47 | `        movimientos_out.append({` | Agrega un diccionario con la información limpia del movimiento a la lista de salida. |
| 48 | `            "id": m.id,` | Identificador único del movimiento. |
| 49 | `            "descripcion": m.descripcion,` | Concepto o título del gasto o ingreso. |
| 50 | `            "categoria": categoria_nombre,` | Nombre textual de la categoría asociada. |
| 51 | `            "monto": monto_float,` | Valor numérico del monto. |
| 52 | `            "tipo": m.tipo,` | Tipo de movimiento: `'ingreso'` o `'gasto'`. |
| 53 | `            "fecha": m.fecha.strftime("%Y-%m-%d") if hasattr(m.fecha, 'strftime') else str(m.fecha),` | Convierte la fecha al formato estándar ISO AAAA-MM-DD. |
| 54 | `            "estado": estado_val` | Estado actual del ciclo de vida: `'pendiente'` o `'pagado'`. |
| 55 | `        })` | Cierra el diccionario del movimiento procesado. |
| 56 | *(Línea en blanco)* | Línea vacía de separación. |
| 57 | `    saldo = round(ingresos - gastos, 2)` | Calcula el saldo disponible restando los gastos pagados a los ingresos, redondeando a 2 decimales. |
| 58 | *(Línea en blanco)* | Línea vacía de separación. |
| 59 | `    return {` | Retorna el objeto JSON estructurado con el resumen financiero completo. |
| 60 | `        "saldo_disponible": saldo,` | Saldo neto real disponible para el estudiante. |
| 61 | `        "ingresos_del_mes": round(ingresos, 2),` | Sumatoria total de ingresos redondeada. |
| 62 | `        "gastos_del_mes": round(gastos, 2),` | Sumatoria total de gastos pagados redondeada. |
| 63 | `        "movimientos": movimientos_out` | Lista detallada de cada movimiento del estudiante. |
| 64 | `    }` | Cierra el diccionario retornado. |
| 65 | *(Línea en blanco)* | Línea vacía de separación. |
| 66 | `@router.post("", response_model=schemas.MovimientoOut)` | Endpoint HTTP POST en `/movimientos` para registrar un nuevo movimiento en el sistema. |
| 67 | `def crear_movimiento(` | Declara la función controladora para crear transacciones. |
| 68 | `    datos: schemas.MovimientoCreate,` | Recibe y valida los datos enviados en el cuerpo JSON según el esquema `MovimientoCreate`. |
| 69 | `    db: Session = Depends(get_db),` | Inyecta la sesión de base de datos. |
| 70 | `    usuario: models.Usuario = Depends(get_current_user)` | Inyecta el usuario autenticado que realiza la creación. |
| 71 | `):` | Cierra los argumentos de la función `crear_movimiento`. |
| 72 | `    bloquear_demo(usuario)` | Invoca la función que bloquea la creación si el usuario está en modo demo. |
| 73 | *(Línea en blanco)* | Línea vacía de separación. |
| 74 | `    cat = None` | Inicializa la variable de categoría en `None`. |
| 75 | `    if datos.categoria:` | Comprueba si el cliente envió un nombre de categoría en los datos. |
| 76 | `        cat = db.query(models.Categoria).filter(models.Categoria.nombre == datos.categoria).first()` | Busca en la base de datos la categoría que tenga ese nombre exacto. |
| 77 | `    cat_id = cat.id if cat else None` | Extrae el ID de la categoría si se encontró, o deja `None` si no existe. |
| 78 | *(Línea en blanco)* | Línea vacía de separación. |
| 79 | `    fecha_val = datetime.utcnow().date()` | Define por defecto la fecha actual del sistema en UTC. |
| 80 | `    if datos.fecha:` | Comprueba si el usuario envió una fecha personalizada. |
| 81 | `        try:` | Abre un bloque de captura para procesar la fecha recibida en formato texto. |
| 82 | `            fecha_val = datetime.strptime(datos.fecha, "%Y-%m-%d").date()` | Convierte el texto AAAA-MM-DD a un objeto `date` de Python. |
| 83 | `        except Exception:` | Captura cualquier error si el formato del texto de la fecha no era válido. |
| 84 | `            pass` | Si falla el parseo, ignora el error y conserva la fecha actual por defecto. |
| 85 | *(Línea en blanco)* | Línea vacía de separación. |
| 86 | `    nuevo = models.Movimiento(` | Instancia un nuevo registro del modelo ORM `Movimiento`. |
| 87 | `        usuario_id=usuario.id,` | Asigna el ID del usuario propietario de la cuenta. |
| 88 | `        categoria_id=cat_id,` | Asigna el ID de la categoría vinculada. |
| 89 | `        monto=datos.monto,` | Asigna el valor del monto enviado. |
| 90 | `        tipo=datos.tipo or "gasto",` | Asigna el tipo (`'gasto'` o `'ingreso'`, por defecto `'gasto'`). |
| 91 | `        descripcion=datos.descripcion.strip(),` | Limpia espacios en blanco alrededor de la descripción y la asigna. |
| 92 | `        fecha=fecha_val,` | Asigna la fecha determinada. |
| 93 | `        estado=datos.estado or "pendiente"` | Asigna el estado inicial del movimiento (por defecto `'pendiente'`). |
| 94 | `    )` | Cierra la instanciación del objeto `Movimiento`. |
| 95 | `    db.add(nuevo)` | Añade el objeto a la sesión de SQLAlchemy para ser insertado. |
| 96 | `    db.commit()` | Confirma y guarda permanentemente el registro en la base de datos. |
| 97 | `    db.refresh(nuevo)` | Recarga el objeto desde la base de datos para obtener su ID generado. |
| 98 | *(Línea en blanco)* | Línea vacía de separación. |
| 99 | `    return {` | Retorna el diccionario estructurado con los datos del nuevo movimiento. |
| 100 | `        "id": nuevo.id,` | ID autoincremental generado en la BD. |
| 101 | `        "descripcion": nuevo.descripcion,` | Concepto del movimiento creado. |
| 102 | `        "categoria": cat.nombre if cat else (datos.categoria or "General"),` | Nombre resuelto de la categoría. |
| 103 | `        "monto": float(nuevo.monto),` | Monto monetario convertido a coma flotante. |
| 104 | `        "tipo": nuevo.tipo,` | Tipo de movimiento asignado. |
| 105 | `        "fecha": nuevo.fecha.strftime("%Y-%m-%d") if hasattr(nuevo.fecha, 'strftime') else str(nuevo.fecha),` | Fecha en formato texto estándar AAAA-MM-DD. |
| 106 | `        "estado": nuevo.estado` | Estado inicial guardado (`'pendiente'`). |
| 107 | `    }` | Cierra el diccionario retornado. |
| 108 | *(Línea en blanco)* | Línea vacía de separación. |
| 109 | `@router.patch("/{movimiento_id}/pagar", response_model=schemas.MovimientoOut)` | Endpoint HTTP PATCH en `/movimientos/{id}/pagar` para ejecutar la transición de estado (Tarea 2). |
| 110 | `def marcar_como_pagado(` | Declara la función controladora de la acción "Marcar como pagado". |
| 111 | `    movimiento_id: int,` | Recibe el identificador del movimiento a través de la URL. |
| 112 | `    db: Session = Depends(get_db),` | Inyecta la sesión de la base de datos. |
| 113 | `    usuario: models.Usuario = Depends(get_current_user)` | Inyecta el usuario autenticado que realiza la solicitud. |
| 114 | `):` | Cierra los argumentos de la función `marcar_como_pagado`. |
| 115 | `    bloquear_demo(usuario)` | Bloquea la operación si el usuario autenticado pertenece a la cuenta demo. |
| 116 | *(Línea en blanco)* | Línea vacía de separación. |
| 117 | `    mov = db.query(models.Movimiento).filter(` | Inicia la consulta buscando el registro en la base de datos. |
| 118 | `        models.Movimiento.id == movimiento_id,` | Filtra por el ID numérico del movimiento pasado en la ruta. |
| 119 | `        models.Movimiento.usuario_id == usuario.id` | Asegura que el movimiento pertenezca obligatoriamente al usuario autenticado (control de acceso). |
| 120 | `    ).first()` | Obtiene el primer resultado coincidente o `None` si no existe. |
| 121 | *(Línea en blanco)* | Línea vacía de separación. |
| 122 | `    if not mov:` | Comprueba si el movimiento no fue encontrado para este usuario. |
| 123 | `        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")` | Lanza error HTTP 404 informando que no existe el movimiento solicitado. |
| 124 | *(Línea en blanco)* | Línea vacía de separación. |
| 125 | `    if getattr(mov, "estado", "pendiente") == "pagado":` | Valida la máquina de estados: verifica si el movimiento ya se encuentra en estado `'pagado'`. |
| 126 | `        raise HTTPException(` | Lanza una excepción HTTP rechazando la transición prohibida. |
| 127 | `            status_code=status.HTTP_400_BAD_REQUEST,` | Retorna código de estado HTTP 400 (Bad Request). |
| 128 | `            detail="Transición inválida: el movimiento ya se encuentra en estado pagado."` | Mensaje formal indicando que no se permite volver a pagar un elemento ya pagado. |
| 129 | `        )` | Cierra la definición de la excepción `HTTPException`. |
| 130 | *(Línea en blanco)* | Línea vacía de separación. |
| 131 | `    mov.estado = "pagado"` | Ejecuta la transición de estado válida actualizando el campo `estado` a `'pagado'`. |
| 132 | `    db.commit()` | Confirma y guarda el cambio permanentemente en la base de datos. |
| 133 | `    db.refresh(mov)` | Recarga los datos actualizados del registro desde la base de datos. |
| 134 | *(Línea en blanco)* | Línea vacía de separación. |
| 135 | `    categoria_nombre = "General"` | Inicializa el nombre de categoría por defecto en "General". |
| 136 | `    if mov.categoria_id:` | Comprueba si el movimiento tiene categoría vinculada. |
| 137 | `        cat = db.query(models.Categoria).filter(models.Categoria.id == mov.categoria_id).first()` | Busca en la base de datos la información de la categoría por su ID. |
| 138 | `        if cat:` | Si se encontró la categoría en la base de datos. |
| 139 | `            categoria_nombre = cat.nombre` | Asigna el nombre real de la categoría. |
| 140 | *(Línea en blanco)* | Línea vacía de separación. |
| 141 | `    return {` | Retorna el objeto completo confirmando que los demás atributos se conservaron intactos. |
| 142 | `        "id": mov.id,` | Conserva el identificador único del movimiento. |
| 143 | `        "descripcion": mov.descripcion,` | Conserva el concepto original intacto. |
| 144 | `        "categoria": categoria_nombre,` | Conserva la categoría original intacta. |
| 145 | `        "monto": float(mov.monto),` | Conserva el monto original intacto. |
| 146 | `        "tipo": mov.tipo,` | Conserva el tipo de movimiento intacto. |
| 147 | `        "fecha": mov.fecha.strftime("%Y-%m-%d") if hasattr(mov.fecha, 'strftime') else str(mov.fecha),` | Conserva la fecha original intacta. |
| 148 | `        "estado": mov.estado` | Devuelve el nuevo estado actualizado a `'pagado'`. |
| 149 | `    }` | Cierra el diccionario retornado. |
| 150 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## usuarios.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/routers/usuarios.py`  
Total de líneas: 125

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `import secrets` | Importa el módulo criptográfico seguro `secrets` para generar números aleatorios no predecibles. |
| 2 | `from datetime import datetime, timedelta` | Importa utilidades de tiempo para calcular marcas de expiración de códigos. |
| 3 | `from fastapi import APIRouter, Depends, HTTPException, status` | Importa el enrutador de FastAPI, dependencias, excepciones HTTP y códigos de estado. |
| 4 | `from sqlalchemy.orm import Session` | Importa la sesión de SQLAlchemy para interactuar con la base de datos. |
| 5 | `from database import get_db` | Importa la función proveedora de la sesión activa de base de datos. |
| 6 | `import models` | Importa los modelos ORM de la base de datos (`Usuario`). |
| 7 | `import schemas` | Importa los esquemas de validación de Pydantic de usuarios y autenticación. |
| 8 | `from security import hash_password, verify_password, create_access_token, get_current_user` | Importa las funciones de seguridad para encriptar claves, verificar hashes, crear JWT y extraer usuario. |
| 9 | `from correo import enviar_codigo_recuperacion` | Importa la función encargada de enviar el código de verificación por correo electrónico. |
| 10 | *(Línea en blanco)* | Línea vacía de separación. |
| 11 | `CODIGO_MINUTOS = 10` | Constante: define el tiempo de vigencia del código de verificación (10 minutos). |
| 12 | `CODIGO_MAX_INTENTOS = 5` | Constante: define la cantidad máxima permitida de intentos errados antes de bloquear el código (5 intentos). |
| 13 | *(Línea en blanco)* | Línea vacía de separación. |
| 14 | `router = APIRouter(prefix="/auth", tags=["Autenticación y Usuarios"])` | Crea el enrutador de FastAPI bajo el prefijo `/auth` con la etiqueta "Autenticación y Usuarios". |
| 15 | *(Línea en blanco)* | Línea vacía de separación. |
| 16 | `@router.post("/registro", response_model=schemas.TokenResponse)` | Endpoint HTTP POST en `/auth/registro` para registrar usuarios nuevos, respondiendo con un token de acceso. |
| 17 | `def registrar_usuario(datos: schemas.UsuarioRegistro, db: Session = Depends(get_db)):` | Declara la función controladora recibiendo los datos de registro y la sesión inyectada de la BD. |
| 18 | `    existe = db.query(models.Usuario).filter(models.Usuario.email == datos.email.lower()).first()` | Consulta si ya existe en la base de datos algún usuario registrado con el mismo correo (en minúsculas). |
| 19 | `    if existe:` | Comprueba si se encontró un usuario preexistente con ese correo. |
| 20 | `        raise HTTPException(` | Lanza una excepción HTTP para detener el registro duplicado. |
| 21 | `            status_code=status.HTTP_400_BAD_REQUEST,` | Retorna código de estado HTTP 400 (Bad Request). |
| 22 | `            detail="Ya existe una cuenta con este correo institucional o personal."` | Mensaje informativo explicando que el correo ya está registrado en la plataforma. |
| 23 | `        )` | Cierra la llamada de `HTTPException`. |
| 24 | *(Línea en blanco)* | Línea vacía de separación. |
| 25 | `    nuevo_usuario = models.Usuario(` | Instancia un nuevo registro del modelo `Usuario`. |
| 26 | `        nombre=datos.nombre.strip(),` | Limpia espacios en blanco alrededor del nombre y lo asigna. |
| 27 | `        email=datos.email.lower().strip(),` | Normaliza el correo electrónico a minúsculas, elimina espacios y lo asigna. |
| 28 | `        password_hash=hash_password(datos.password)` | Genera el hash criptográfico seguro de la contraseña (nunca se guarda en texto plano). |
| 29 | `    )` | Cierra la instanciación del objeto `Usuario`. |
| 30 | `    db.add(nuevo_usuario)` | Agrega el nuevo usuario a la sesión de la base de datos. |
| 31 | `    db.commit()` | Confirma y guarda el usuario permanentemente en la base de datos. |
| 32 | `    db.refresh(nuevo_usuario)` | Recarga los datos del usuario recién guardado para obtener su ID asignado. |
| 33 | *(Línea en blanco)* | Línea vacía de separación. |
| 34 | `    token = create_access_token({"sub": str(nuevo_usuario.id), "email": nuevo_usuario.email})` | Genera un token JWT firmado conteniendo el ID del usuario en el reclamo `"sub"` y su correo. |
| 35 | *(Línea en blanco)* | Línea vacía de separación. |
| 36 | `    return {` | Retorna el diccionario de respuesta para iniciar sesión inmediatamente. |
| 37 | `        "token": token,` | Token de acceso JWT para ser guardado por el navegador. |
| 38 | `        "usuario": nuevo_usuario` | Objeto con los datos públicos del usuario según el esquema `UsuarioOut`. |
| 39 | `    }` | Cierra el diccionario retornado. |
| 40 | *(Línea en blanco)* | Línea vacía de separación. |
| 41 | `@router.post("/login", response_model=schemas.TokenResponse)` | Endpoint HTTP POST en `/auth/login` para iniciar sesión y obtener credenciales. |
| 42 | `def login(datos: schemas.UsuarioLogin, db: Session = Depends(get_db)):` | Declara la función controladora de login recibiendo correo, clave y la sesión de BD. |
| 43 | `    usuario = db.query(models.Usuario).filter(models.Usuario.email == datos.email.lower()).first()` | Busca en la base de datos al usuario que coincida con el correo ingresado en minúsculas. |
| 44 | `    if not usuario or not verify_password(datos.password, usuario.password_hash):` | Verifica si el usuario no existe O si la contraseña provista no coincide con el hash almacenado. |
| 45 | `        raise HTTPException(` | Lanza una excepción HTTP de rechazo si las credenciales son inválidas. |
| 46 | `            status_code=status.HTTP_401_UNAUTHORIZED,` | Retorna código de estado HTTP 401 (No autorizado). |
| 47 | `            detail="Correo o contraseña incorrectos."` | Mensaje seguro genérico que no revela si el error fue el correo o la contraseña. |
| 48 | `        )` | Cierra la excepción `HTTPException`. |
| 49 | *(Línea en blanco)* | Línea vacía de separación. |
| 50 | `    token = create_access_token({"sub": str(usuario.id), "email": usuario.email})` | Genera el token JWT firmado para la sesión activa del usuario. |
| 51 | *(Línea en blanco)* | Línea vacía de separación. |
| 52 | `    return {` | Retorna las credenciales de sesión autorizada. |
| 53 | `        "token": token,` | Token JWT para ser almacenado en el frontend (localStorage). |
| 54 | `        "usuario": usuario` | Objeto con los datos del perfil del usuario autenticado. |
| 55 | `    }` | Cierra el diccionario de respuesta. |
| 56 | *(Línea en blanco)* | Línea vacía de separación. |
| 57 | `def _buscar_usuario(db: Session, email: str):` | Declara la función auxiliar privada para buscar un usuario por su correo electrónico. |
| 58 | `    return db.query(models.Usuario).filter(models.Usuario.email == email.lower().strip()).first()` | Ejecuta la consulta filtrando por correo limpio y en minúsculas, retornando el primer resultado o `None`. |
| 59 | *(Línea en blanco)* | Línea vacía de separación. |
| 60 | `def _validar_codigo(db: Session, usuario, codigo: str):` | Declara la función auxiliar que valida las reglas de seguridad del código de verificación de 4 dígitos. |
| 61 | `    if not usuario or not usuario.token_recuperacion or not usuario.codigo_expira:` | Comprueba si el usuario no existe, o si no tiene un código activo o fecha de vencimiento registrada. |
| 62 | `        raise HTTPException(status_code=400, detail="Primero solicita un código de verificación.")` | Lanza error HTTP 400 exigiendo solicitar un código previamente. |
| 63 | `    if datetime.utcnow() > usuario.codigo_expira:` | Comprueba si la fecha y hora actual en UTC supera la hora de vencimiento del código. |
| 64 | `        raise HTTPException(status_code=400, detail="El código venció. Solicita uno nuevo.")` | Lanza error HTTP 400 indicando que el código expiró por tiempo. |
| 65 | `    if (usuario.codigo_intentos or 0) >= CODIGO_MAX_INTENTOS:` | Comprueba si el usuario ya alcanzó o superó el límite de 5 intentos erróneos permitidos. |
| 66 | `        raise HTTPException(status_code=400, detail="Demasiados intentos fallidos. Solicita un código nuevo.")` | Lanza error HTTP 400 bloqueando el código por agotamiento de intentos. |
| 67 | `    if not verify_password(codigo.strip(), usuario.token_recuperacion):` | Compara el código ingresado por el usuario contra el hash almacenado en la BD. |
| 68 | `        usuario.codigo_intentos = (usuario.codigo_intentos or 0) + 1` | Si el código no coincide, incrementa en 1 el contador de intentos fallidos. |
| 69 | `        db.commit()` | Guarda inmediatamente el incremento del contador en la base de datos. |
| 70 | `        restantes = CODIGO_MAX_INTENTOS - usuario.codigo_intentos` | Calcula cuántos intentos restantes le quedan al usuario. |
| 71 | `        if restantes <= 0:` | Comprueba si ya no le quedan intentos disponibles. |
| 72 | `            raise HTTPException(status_code=400, detail="Código incorrecto. Ya no te quedan intentos: solicita un código nuevo.")` | Lanza error avisando que agotó todos sus intentos. |
| 73 | `        palabra = "intento" if restantes == 1 else "intentos"` | Formatea gramaticalmente la palabra "intento" o "intentos" según la cantidad restante. |
| 74 | `        raise HTTPException(status_code=400, detail=f"Código incorrecto. Te quedan {restantes} {palabra}.")` | Lanza error HTTP 400 indicando la cantidad exacta de intentos que le restan. |
| 75 | *(Línea en blanco)* | Línea vacía de separación. |
| 76 | `@router.post("/recuperar/solicitar")` | Endpoint HTTP POST en `/auth/recuperar/solicitar` para el Paso 1 de recuperación de contraseña. |
| 77 | `def solicitar_codigo(datos: schemas.SolicitarCodigo, db: Session = Depends(get_db)):` | Declara la función para generar y despachar el código de recuperación. |
| 78 | `    usuario = _buscar_usuario(db, datos.email)` | Busca si el correo suministrado pertenece a un usuario registrado en el sistema. |
| 79 | `    if usuario and usuario.es_demo:` | Comprueba si el usuario encontrado corresponde a la cuenta de prueba (`estudiante@demo.com`). |
| 80 | `        raise HTTPException(` | Lanza una excepción impidiendo alterar la cuenta demostrativa. |
| 81 | `            status_code=status.HTTP_403_FORBIDDEN,` | Asigna el código de error HTTP 403 (Prohibido). |
| 82 | `            detail="La cuenta demo es solo de muestra: no se puede cambiar su contraseña."` | Mensaje aclarando que la cuenta demo no permite cambio de clave. |
| 83 | `        )` | Cierra la definición de la excepción. |
| 84 | *(Línea en blanco)* | Línea vacía de separación. |
| 85 | `    if usuario:` | Si el usuario existe y no es la cuenta demo, procede con la generación del código. |
| 86 | `        codigo = f"{secrets.randbelow(10000):04d}"` | Genera un número aleatorio criptográfico entre 0000 y 9999 con 4 dígitos fijos (ejemplo: '0482'). |
| 87 | `        usuario.token_recuperacion = hash_password(codigo)` | Guarda en la BD el hash seguro del código (nunca el código en texto plano). |
| 88 | `        usuario.codigo_expira = datetime.utcnow() + timedelta(minutes=CODIGO_MINUTOS)` | Establece la fecha y hora de vencimiento sumando 10 minutos al momento actual. |
| 89 | `        usuario.codigo_intentos = 0` | Reinicia el contador de intentos fallidos a cero. |
| 90 | `        db.commit()` | Confirma y guarda permanentemente estos datos en la base de datos. |
| 91 | `        try:` | Abre un bloque de captura de errores para intentar despachar el correo electrónico. |
| 92 | `            enviar_codigo_recuperacion(usuario.email, usuario.nombre, codigo, CODIGO_MINUTOS)` | Llama a la función que conecta por SMTP y envía el correo con el código al estudiante. |
| 93 | `        except Exception as err:` | Captura cualquier fallo si el servidor de correo SMTP no responde. |
| 94 | `            print(f"Error al enviar el correo: {err}")` | Imprime en la consola del servidor el detalle del error de correo. |
| 95 | `            raise HTTPException(` | Lanza una excepción HTTP notificando el problema externo. |
| 96 | `                status_code=status.HTTP_502_BAD_GATEWAY,` | Asigna código HTTP 502 (Bad Gateway) por falla en el servicio de correo. |
| 97 | `                detail="No se pudo enviar el correo. Intenta de nuevo en unos minutos."` | Mensaje para el usuario sugiriendo reintentar en unos minutos. |
| 98 | `            )` | Cierra la definición de la excepción. |
| 99 | *(Línea en blanco)* | Línea vacía de separación. |
| 100 | `    return {"mensaje": "Si el correo está registrado, te enviamos un código de 4 dígitos."}` | Retorna una respuesta neutra para no divulgar si el correo existe o no (buena práctica de seguridad). |
| 101 | *(Línea en blanco)* | Línea vacía de separación. |
| 102 | `@router.post("/recuperar/verificar")` | Endpoint HTTP POST en `/auth/recuperar/verificar` para el Paso 2 de recuperación de contraseña. |
| 103 | `def verificar_codigo(datos: schemas.VerificarCodigo, db: Session = Depends(get_db)):` | Declara la función para comprobar si el código de 4 dígitos ingresado es válido. |
| 104 | `    _validar_codigo(db, _buscar_usuario(db, datos.email), datos.codigo)` | Ejecuta todas las validaciones de existencia, expiración, intentos y hash del código. |
| 105 | `    return {"mensaje": "Código verificado."}` | Si no hubo excepciones, confirma que el código es correcto y permite avanzar. |
| 106 | *(Línea en blanco)* | Línea vacía de separación. |
| 107 | `@router.post("/recuperar/restablecer")` | Endpoint HTTP POST en `/auth/recuperar/restablecer` para el Paso 3 final de cambio de contraseña. |
| 108 | `def restablecer_password(datos: schemas.RestablecerPassword, db: Session = Depends(get_db)):` | Declara la función para registrar la nueva contraseña elegida por el estudiante. |
| 109 | `    usuario = _buscar_usuario(db, datos.email)` | Busca el registro del usuario por su correo en la base de datos. |
| 110 | `    _validar_codigo(db, usuario, datos.codigo)` | Valida nuevamente el código para garantizar la autenticidad de la petición final. |
| 111 | `    if len(datos.nueva_password) < 6:` | Comprueba la regla de complejidad mínima de contraseña (al menos 6 caracteres). |
| 112 | `        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres.")` | Lanza error HTTP 400 si la clave no cumple con la longitud mínima requerida. |
| 113 | *(Línea en blanco)* | Línea vacía de separación. |
| 114 | `    usuario.password_hash = hash_password(datos.nueva_password)` | Genera el hash seguro de la nueva clave y lo asigna al campo `password_hash`. |
| 115 | `    usuario.token_recuperacion = None` | Anula el código de recuperación para impedir que pueda reutilizarse. |
| 116 | `    usuario.codigo_expira = None` | Limpia la fecha de expiración del código. |
| 117 | `    usuario.codigo_intentos = 0` | Restablece el contador de intentos a cero. |
| 118 | `    db.commit()` | Guarda permanentemente la nueva contraseña y la limpieza de datos en la base de datos. |
| 119 | *(Línea en blanco)* | Línea vacía de separación. |
| 120 | `    return {"mensaje": "Contraseña actualizada exitosamente."}` | Retorna mensaje de confirmación de cambio exitoso de contraseña. |
| 121 | *(Línea en blanco)* | Línea vacía de separación. |
| 122 | `@router.get("/me", response_model=schemas.UsuarioOut)` | Endpoint HTTP GET en `/auth/me` para obtener el perfil del usuario autenticado. |
| 123 | `def obtener_perfil(usuario: models.Usuario = Depends(get_current_user)):` | Declara la función inyectando el usuario validado a partir de la cabecera Bearer del token. |
| 124 | `    return usuario` | Retorna los datos públicos del usuario conectado (id, nombre, email, es_demo). |
| 125 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

# 2. Carpeta: Raíz del Backend (BACKEND/)

## main.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/main.py`  
Total de líneas: 52

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `from fastapi import FastAPI` | Importa la clase principal `FastAPI` para crear el servidor web de la aplicación. |
| 2 | `from fastapi.middleware.cors import CORSMiddleware` | Importa el middleware de CORS para permitir solicitudes web desde el frontend (Vue 3). |
| 3 | `from database import engine, Base` | Importa el motor de conexión (`engine`) y la clase base declarativa (`Base`) desde `database.py`. |
| 4 | `import models` | Importa los modelos ORM de la base de datos para que SQLAlchemy los reconozca al iniciar. |
| 5 | `from routers import usuarios, movimientos, categorias` | Importa los tres módulos de rutas desde la carpeta `routers/`. |
| 6 | *(Línea en blanco)* | Línea vacía de separación. |
| 7 | `from sqlalchemy import text, inspect` | Importa `text` para ejecutar sentencias SQL directas e `inspect` para inspeccionar la estructura de tablas. |
| 8 | *(Línea en blanco)* | Línea vacía de separación. |
| 9 | `try:` | Inicia bloque `try` para inicializar y migrar la base de datos de manera segura al arrancar. |
| 10 | `    Base.metadata.create_all(bind=engine)` | Crea automáticamente todas las tablas faltantes en la base de datos conectada. |
| 11 | `    inspector = inspect(engine)` | Crea un objeto inspector para consultar las tablas y columnas existentes en la base de datos. |
| 12 | `    if "movimientos" in inspector.get_table_names():` | Comprueba si la tabla `movimientos` ya existe en la base de datos. |
| 13 | `        columnas = [c["name"] for c in inspector.get_columns("movimientos")]` | Obtiene una lista con los nombres de todas las columnas que tiene actualmente la tabla `movimientos`. |
| 14 | `        if "estado" not in columnas:` | Verifica si la columna `estado` (necesaria para la Tarea 2) todavía no existe en la tabla. |
| 15 | `            with engine.connect() as conn:` | Abre una conexión directa a la base de datos. |
| 16 | `                conn.execute(text("ALTER TABLE movimientos ADD COLUMN estado VARCHAR(20) DEFAULT 'pendiente' NOT NULL;"))` | Ejecuta la instrucción SQL de migración para añadir la columna `estado` con valor por defecto `'pendiente'`. |
| 17 | `                conn.commit()` | Confirma y aplica permanentemente la alteración de la tabla. |
| 18 | `                print("[OK] Columna 'estado' agregada a tabla movimientos exitosamente.")` | Imprime mensaje en consola confirmando que la columna fue agregada con éxito. |
| 19 | `except Exception as e:` | Captura cualquier excepción que ocurra durante la inicialización de la base de datos. |
| 20 | `    print(f"Nota de conexion a la base de datos: {e}")` | Imprime en consola la advertencia del error de base de datos sin detener la aplicación. |
| 21 | *(Línea en blanco)* | Línea vacía de separación. |
| 22 | `app = FastAPI(` | Instancia la aplicación principal de FastAPI en la variable `app`. |
| 23 | `    title="Presupuesto Estudiantil API",` | Asigna el título formal que aparecerá en la documentación `/docs`. |
| 24 | `    description="API Backend para control de presupuesto estudiantil (IHC - Proyecto 2)",` | Asigna la descripción del proyecto para la documentación de Swagger. |
| 25 | `    version="1.0.0"` | Define la versión actual de la API en "1.0.0". |
| 26 | `)` | Cierra los argumentos de creación de la instancia de `FastAPI`. |
| 27 | *(Línea en blanco)* | Línea vacía de separación. |
| 28 | `app.add_middleware(` | Registra un middleware en la aplicación de FastAPI para procesar peticiones HTTP entrantes. |
| 29 | `    CORSMiddleware,` | Especifica que el middleware a registrar es el de control de acceso de origen cruzado (CORS). |
| 30 | `    allow_origins=[` | Inicia la lista de dominios y puertos autorizados a consumir esta API. |
| 31 | `        "http://localhost:5173",` | Permite peticiones desde el frontend en desarrollo local (puerto por defecto de Vite). |
| 32 | `        "http://127.0.0.1:5173",` | Permite peticiones usando la IP local 127.0.0.1 en el puerto 5173. |
| 33 | `        "*"` | Permite peticiones desde cualquier otro origen para evitar bloqueos durante pruebas o red local. |
| 34 | `    ],` | Cierra la lista de orígenes permitidos. |
| 35 | `    allow_credentials=True,` | Habilita el intercambio de cabeceras de autorización y credenciales. |
| 36 | `    allow_methods=["*"],` | Permite todos los métodos HTTP (GET, POST, PUT, DELETE, PATCH, etc.). |
| 37 | `    allow_headers=["*"],` | Permite todas las cabeceras HTTP en las solicitudes entrantes. |
| 38 | `)` | Cierra la configuración del middleware CORS. |
| 39 | *(Línea en blanco)* | Línea vacía de separación. |
| 40 | `app.include_router(usuarios.router)` | Incluye todas las rutas de usuarios y autenticación (`/auth`). |
| 41 | `app.include_router(movimientos.router)` | Incluye todas las rutas de movimientos financieros (`/movimientos`). |
| 42 | `app.include_router(categorias.router)` | Incluye todas las rutas de categorías (`/categorias`). |
| 43 | *(Línea en blanco)* | Línea vacía de separación. |
| 44 | `@app.get("/")` | Define un endpoint HTTP GET en la ruta raíz (`/`). |
| 45 | `def ruta_raiz():` | Declara la función que atiende las visitas a la ruta raíz. |
| 46 | `    return {` | Retorna un diccionario JSON confirmando el estado del backend. |
| 47 | `        "aplicacion": "Presupuesto Estudiantil API",` | Nombre del sistema. |
| 48 | `        "estado": "En línea 🚀",` | Estado operativo del servidor. |
| 49 | `        "documentacion": "/docs",` | Ruta hacia la interfaz interactiva de Swagger UI. |
| 50 | `        "tarea": "Manejo de acceso (Tarea 1 - IHC)"` | Identificador de la tarea académica correspondiente. |
| 51 | `    }` | Cierra el diccionario de respuesta. |
| 52 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## database.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/database.py`  
Total de líneas: 38

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `import os` | Importa el módulo del sistema operativo para leer variables de entorno. |
| 2 | `from dotenv import load_dotenv` | Importa la función `load_dotenv` para cargar variables del archivo `.env`. |
| 3 | `from sqlalchemy import create_engine` | Importa `create_engine` de SQLAlchemy para crear la conexión con la base de datos. |
| 4 | `from sqlalchemy.orm import declarative_base, sessionmaker` | Importa `declarative_base` para la clase base de los modelos y `sessionmaker` para crear sesiones. |
| 5 | *(Línea en blanco)* | Línea vacía de separación. |
| 6 | `load_dotenv()` | Carga las variables definidas en el archivo `.env` en las variables de entorno del sistema. |
| 7 | *(Línea en blanco)* | Línea vacía de separación. |
| 8 | `DATABASE_URL = os.getenv(` | Lee el valor de la variable de entorno `DATABASE_URL`. |
| 9 | `    "DATABASE_URL",` | Nombre de la variable de entorno solicitada. |
| 10 | `    "postgresql+psycopg://postgres:postgres@localhost:5432/presupuesto_estudiantil"` | Cadena de conexión por defecto apuntando a PostgreSQL local con el driver psycopg3. |
| 11 | `)` | Cierra la llamada a `os.getenv`. |
| 12 | *(Línea en blanco)* | Línea vacía de separación. |
| 13 | `if DATABASE_URL.startswith("postgresql://"):` | Verifica si la URL recibida usa el prefijo clásico antiguo de PostgreSQL. |
| 14 | `    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)` | Reemplaza el prefijo para forzar el uso del driver moderno `psycopg` (versión 3). |
| 15 | `elif DATABASE_URL.startswith("postgresql+psycopg2://"):` | Verifica si la URL especificó el driver antiguo `psycopg2`. |
| 16 | `    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+psycopg://", 1)` | Lo reemplaza por `postgresql+psycopg://` para asegurar compatibilidad. |
| 17 | *(Línea en blanco)* | Línea vacía de separación. |
| 18 | `engine = None` | Inicializa la variable `engine` en `None`. |
| 19 | `try:` | Inicia bloque para intentar conectar a PostgreSQL. |
| 20 | `    test_engine = create_engine(DATABASE_URL, echo=False)` | Crea el motor de SQLAlchemy con la URL de PostgreSQL (`echo=False` silencia trazas excesivas de SQL). |
| 21 | `    with test_engine.connect() as conn:` | Abre una conexión de prueba con la base de datos PostgreSQL. |
| 22 | `        print("[OK] Conexion exitosa a PostgreSQL")` | Imprime mensaje en consola si la conexión a PostgreSQL fue exitosa. |
| 23 | `    engine = test_engine` | Asigna el motor probado como el motor activo de la aplicación. |
| 24 | `except Exception as err:` | Captura el error si el servidor de PostgreSQL está apagado o las credenciales no son válidas. |
| 25 | `    print(f"[Nota] PostgreSQL: {err}")` | Muestra en consola el error que impidió conectar a PostgreSQL. |
| 26 | `    print("[Info] Usando almacenamiento local seguro (SQLite) mientras configuras tus credenciales de PostgreSQL en .env")` | Informa que la app usará SQLite local automáticamente para que el proyecto funcione sin configuraciones complejas. |
| 27 | `    engine = create_engine("sqlite:///./presupuesto.db", connect_args={"check_same_thread": False})` | Crea el motor de base de datos SQLite en el archivo local `presupuesto.db` habilitando soporte multihilo. |
| 28 | *(Línea en blanco)* | Línea vacía de separación. |
| 29 | `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)` | Configura la fábrica de sesiones de base de datos vinculada al motor activo. |
| 30 | `Base = declarative_base()` | Crea la clase base de la cual heredarán todos los modelos de tablas (ORM). |
| 31 | *(Línea en blanco)* | Línea vacía de separación. |
| 32 | `def get_db():` | Declara la función generadora que entrega y cierra una sesión de base de datos por cada petición. |
| 33 | `    db = SessionLocal()` | Abre una nueva sesión de la base de datos. |
| 34 | `    try:` | Inicia bloque para entregar la sesión de forma controlada. |
| 35 | `        yield db` | Entrega (`yield`) la sesión al endpoint que la solicitó como dependencia. |
| 36 | `    finally:` | Bloque que se ejecuta obligatoriamente al finalizar la atención de la petición HTTP. |
| 37 | `        db.close()` | Cierra la sesión de la base de datos liberando la conexión de vuelta al pool. |
| 38 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## models.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/models.py`  
Total de líneas: 48

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey` | Importa los tipos de datos y restricciones de SQLAlchemy para definir los campos de las tablas. |
| 2 | `from sqlalchemy.orm import relationship` | Importa `relationship` para definir relaciones ORM entre modelos (ej: usuario y sus movimientos). |
| 3 | `from datetime import datetime` | Importa `datetime` para asignar fechas y horas automáticas a los registros creados. |
| 4 | `from database import Base` | Importa la clase base declarativa desde `database.py`. |
| 5 | *(Línea en blanco)* | Línea vacía de separación. |
| 6 | `DEMO_EMAIL = "estudiante@demo.com"` | Constante: define el correo asignado a la cuenta especial de demostración. |
| 7 | *(Línea en blanco)* | Línea vacía de separación. |
| 8 | `class Usuario(Base):` | Define la clase del modelo ORM correspondiente a la tabla de usuarios. |
| 9 | `    __tablename__ = "usuarios"` | Establece el nombre físico de la tabla en la base de datos como `"usuarios"`. |
| 10 | *(Línea en blanco)* | Línea vacía de separación. |
| 11 | `    id = Column(Integer, primary_key=True, index=True)` | Campo `id`: clave primaria entera, autoincremental e indexada. |
| 12 | `    nombre = Column(String(100), nullable=False)` | Campo `nombre`: cadena de texto de hasta 100 caracteres, no puede ser nula. |
| 13 | `    email = Column(String(150), unique=True, index=True, nullable=False)` | Campo `email`: correo único, indexado para búsquedas rápidas, de hasta 150 caracteres y no nulo. |
| 14 | `    password_hash = Column(String(255), nullable=False)` | Campo `password_hash`: almacena la contraseña cifrada en hash seguro (hasta 255 caracteres). |
| 15 | `    token_recuperacion = Column(String(255), nullable=True)` | Campo `token_recuperacion`: almacena el hash del código de 4 dígitos para recuperar clave (puede ser nulo). |
| 16 | `    codigo_expira = Column(DateTime, nullable=True)` | Campo `codigo_expira`: fecha y hora de vencimiento del código de recuperación (puede ser nulo). |
| 17 | `    codigo_intentos = Column(Integer, default=0)` | Campo `codigo_intentos`: número de intentos fallidos al introducir el código (inicia en 0). |
| 18 | `    creado_en = Column(DateTime, default=datetime.utcnow)` | Campo `creado_en`: marca de tiempo UTC en que se registró la cuenta. |
| 19 | *(Línea en blanco)* | Línea vacía de separación. |
| 20 | `    movimientos = relationship("Movimiento", back_populates="usuario", cascade="all, delete-orphan")` | Define relación de uno a muchos con `Movimiento`; si se borra el usuario se borran sus movimientos en cascada. |
| 21 | *(Línea en blanco)* | Línea vacía de separación. |
| 22 | `    @property` | Decorador para definir un método accesible como un atributo simple del objeto. |
| 23 | `    def es_demo(self) -> bool:` | Declara la propiedad que evalúa si el usuario es la cuenta de demostración. |
| 24 | `        return self.email == DEMO_EMAIL` | Retorna `True` si el correo coincide con `estudiante@demo.com`, o `False` en caso contrario. |
| 25 | *(Línea en blanco)* | Línea vacía de separación. |
| 26 | `class Categoria(Base):` | Define la clase del modelo ORM correspondiente a la tabla de categorías. |
| 27 | `    __tablename__ = "categorias"` | Establece el nombre físico de la tabla en la base de datos como `"categorias"`. |
| 28 | *(Línea en blanco)* | Línea vacía de separación. |
| 29 | `    id = Column(Integer, primary_key=True, index=True)` | Campo `id`: clave primaria entera e indexada de la categoría. |
| 30 | `    nombre = Column(String(50), nullable=False)` | Campo `nombre`: nombre de la categoría (hasta 50 caracteres, no nulo). |
| 31 | `    tipo = Column(String(10), nullable=False)` | Campo `tipo`: indica si la categoría es de `'ingreso'` o `'gasto'`. |
| 32 | `    icono = Column(String(50), default="tag")` | Campo `icono`: nombre del icono en el frontend (por defecto "tag"). |
| 33 | *(Línea en blanco)* | Línea vacía de separación. |
| 34 | `class Movimiento(Base):` | Define la clase del modelo ORM correspondiente a la tabla de movimientos financieros. |
| 35 | `    __tablename__ = "movimientos"` | Establece el nombre físico de la tabla en la base de datos como `"movimientos"`. |
| 36 | *(Línea en blanco)* | Línea vacía de separación. |
| 37 | `    id = Column(Integer, primary_key=True, index=True)` | Campo `id`: clave primaria entera e indexada del movimiento. |
| 38 | `    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)` | Clave foránea referenciando a `usuarios.id`; eliminación en cascada si el usuario es borrado. |
| 39 | `    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True)` | Clave foránea opcional referenciando a `categorias.id`; si se borra la categoría queda en NULL. |
| 40 | `    monto = Column(Numeric(10, 2), nullable=False)` | Campo `monto`: número decimal con hasta 10 dígitos y 2 decimales, no nulo. |
| 41 | `    tipo = Column(String(10), nullable=False)` | Campo `tipo`: almacena `'ingreso'` o `'gasto'`. |
| 42 | `    descripcion = Column(String(255), nullable=False)` | Campo `descripcion`: concepto de la transacción (hasta 255 caracteres, no nulo). |
| 43 | `    fecha = Column(Date, default=datetime.utcnow().date)` | Campo `fecha`: fecha en que se realizó el movimiento (por defecto la fecha actual). |
| 44 | `    estado = Column(String(20), default="pendiente", nullable=False)` | Campo `estado`: ciclo de vida del movimiento (por defecto `'pendiente'`, no nulo). Requerido por la Tarea 2. |
| 45 | `    creado_en = Column(DateTime, default=datetime.utcnow)` | Campo `creado_en`: marca de tiempo UTC de creación del registro. |
| 46 | *(Línea en blanco)* | Línea vacía de separación. |
| 47 | `    usuario = relationship("Usuario", back_populates="movimientos")` | Define la relación inversa de muchos a uno con el modelo `Usuario`. |
| 48 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## schemas.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/schemas.py`  
Total de líneas: 72

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `from pydantic import BaseModel` | Importa la clase `BaseModel` de Pydantic para definir esquemas de validación de datos. |
| 2 | `from typing import Optional, List` | Importa `Optional` para campos no obligatorios y `List` para definir listas de modelos. |
| 3 | *(Línea en blanco)* | Línea vacía de separación. |
| 4 | `class UsuarioRegistro(BaseModel):` | Define el esquema para validar los datos recibidos al registrar una cuenta nueva. |
| 5 | `    nombre: str` | Exige un campo de texto obligatorio con el nombre completo del usuario. |
| 6 | `    email: str` | Exige un campo de texto obligatorio con el correo electrónico del usuario. |
| 7 | `    password: str` | Exige un campo de texto obligatorio con la contraseña elegida. |
| 8 | *(Línea en blanco)* | Línea vacía de separación. |
| 9 | `class UsuarioLogin(BaseModel):` | Define el esquema para validar los datos que el usuario envía al iniciar sesión. |
| 10 | `    email: str` | Exige el campo de correo electrónico del usuario. |
| 11 | `    password: str` | Exige el campo de la contraseña. |
| 12 | *(Línea en blanco)* | Línea vacía de separación. |
| 13 | `class UsuarioOut(BaseModel):` | Define el esquema de salida segura de información del usuario (sin devolver contraseñas). |
| 14 | `    id: int` | Devuelve el ID numérico del usuario. |
| 15 | `    nombre: str` | Devuelve el nombre del usuario. |
| 16 | `    email: str` | Devuelve el correo del usuario. |
| 17 | `    es_demo: bool = False` | Devuelve si el usuario está en modo demo (por defecto `False`). |
| 18 | *(Línea en blanco)* | Línea vacía de separación. |
| 19 | `    class Config:` | Clase de configuración interna de Pydantic. |
| 20 | `        from_attributes = True` | Permite que Pydantic serialice datos leyendo directamente los atributos de modelos ORM de SQLAlchemy. |
| 21 | *(Línea en blanco)* | Línea vacía de separación. |
| 22 | `class TokenResponse(BaseModel):` | Define el esquema retornado tras un login o registro exitoso. |
| 23 | `    token: str` | Retorna la cadena del token de acceso JWT generado. |
| 24 | `    usuario: UsuarioOut` | Retorna el objeto con los datos del usuario autenticado. |
| 25 | *(Línea en blanco)* | Línea vacía de separación. |
| 26 | `class SolicitarCodigo(BaseModel):` | Esquema para el Paso 1 de recuperación de contraseña: solicitud de código. |
| 27 | `    email: str` | Correo electrónico de la cuenta que desea recuperar el acceso. |
| 28 | *(Línea en blanco)* | Línea vacía de separación. |
| 29 | `class VerificarCodigo(BaseModel):` | Esquema para el Paso 2 de recuperación de contraseña: verificación de código. |
| 30 | `    email: str` | Correo del usuario que recibió el código. |
| 31 | `    codigo: str` | Cadena con el código de 4 dígitos ingresado por el usuario. |
| 32 | *(Línea en blanco)* | Línea vacía de separación. |
| 33 | `class RestablecerPassword(BaseModel):` | Esquema para el Paso 3 de recuperación de contraseña: cambio de contraseña. |
| 34 | `    email: str` | Correo electrónico de la cuenta a actualizar. |
| 35 | `    codigo: str` | Código de 4 dígitos para comprobación final. |
| 36 | `    nueva_password: str` | Nueva contraseña que el usuario desea asignar. |
| 37 | *(Línea en blanco)* | Línea vacía de separación. |
| 38 | `class MovimientoCreate(BaseModel):` | Define el esquema para validar los datos al registrar un nuevo movimiento financiero. |
| 39 | `    descripcion: str` | Campo obligatorio con el concepto o descripción del movimiento. |
| 40 | `    categoria: Optional[str] = "General"` | Nombre de la categoría (opcional, asigna "General" por defecto). |
| 41 | `    monto: float` | Monto monetario numérico obligatorio. |
| 42 | `    tipo: Optional[str] = "gasto"` | Tipo de movimiento (opcional, asigna "gasto" por defecto). |
| 43 | `    fecha: Optional[str] = None` | Fecha en formato texto AAAA-MM-DD (opcional, por defecto `None`). |
| 44 | `    estado: Optional[str] = "pendiente"` | Estado del movimiento (opcional, asigna "pendiente" por defecto). |
| 45 | *(Línea en blanco)* | Línea vacía de separación. |
| 46 | `class MovimientoOut(BaseModel):` | Define el formato de salida estructurado para enviar un movimiento al cliente. |
| 47 | `    id: int` | Identificador único del movimiento. |
| 48 | `    descripcion: str` | Concepto del movimiento. |
| 49 | `    categoria: str` | Nombre textual de la categoría. |
| 50 | `    monto: float` | Cantidad monetaria del movimiento. |
| 51 | `    tipo: str` | Tipo: `'ingreso'` o `'gasto'`. |
| 52 | `    fecha: str` | Fecha formateada en texto (AAAA-MM-DD). |
| 53 | `    estado: str = "pendiente"` | Estado del movimiento (`'pendiente'` o `'pagado'`). |
| 54 | *(Línea en blanco)* | Línea vacía de separación. |
| 55 | `    class Config:` | Clase de configuración de Pydantic. |
| 56 | `        from_attributes = True` | Habilita compatibilidad con modelos ORM de SQLAlchemy. |
| 57 | *(Línea en blanco)* | Línea vacía de separación. |
| 58 | `class ResumenFinanciero(BaseModel):` | Define el formato devuelto por el dashboard principal de finanzas. |
| 59 | `    saldo_disponible: float` | Saldo neto disponible calculado (ingresos - gastos pagados). |
| 60 | `    ingresos_del_mes: float` | Total acumulado de ingresos. |
| 61 | `    gastos_del_mes: float` | Total acumulado de gastos pagados. |
| 62 | `    movimientos: List[MovimientoOut]` | Lista completa de todos los movimientos registrados. |
| 63 | *(Línea en blanco)* | Línea vacía de separación. |
| 64 | `class CategoriaOut(BaseModel):` | Define el formato de salida para los datos de cada categoría. |
| 65 | `    id: int` | Identificador numérico de la categoría. |
| 66 | `    nombre: str` | Nombre descriptivo de la categoría. |
| 67 | `    tipo: str` | Tipo de movimiento asociado: `'ingreso'` o `'gasto'`. |
| 68 | `    icono: str` | Identificador del icono para representarla visualmente. |
| 69 | *(Línea en blanco)* | Línea vacía de separación. |
| 70 | `    class Config:` | Clase de configuración interna de Pydantic. |
| 71 | `        from_attributes = True` | Permite lectura directa de modelos ORM. |
| 72 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## security.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/security.py`  
Total de líneas: 57

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `import os` | Importa el módulo del sistema operativo para leer variables de entorno. |
| 2 | `from datetime import datetime, timedelta` | Importa utilidades para calcular fechas de expiración de los tokens JWT. |
| 3 | `import jwt` | Importa la librería PyJWT para codificar, firmar y decodificar tokens JWT. |
| 4 | `from dotenv import load_dotenv` | Importa `load_dotenv` para leer variables desde el archivo `.env`. |
| 5 | `from werkzeug.security import generate_password_hash, check_password_hash` | Importa funciones de hash seguro de contraseñas de Werkzeug (pbkdf2 / scrypt). |
| 6 | `from fastapi import Depends, HTTPException, status` | Importa dependencias, excepciones HTTP y códigos de estado de FastAPI. |
| 7 | `from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials` | Importa el esquema de seguridad HTTP Bearer para autenticación por cabeceras. |
| 8 | `from sqlalchemy.orm import Session` | Importa el tipo `Session` de SQLAlchemy. |
| 9 | `from database import get_db` | Importa la función de inyección de sesión de base de datos. |
| 10 | `import models` | Importa los modelos ORM para consultar la tabla de usuarios. |
| 11 | *(Línea en blanco)* | Línea vacía de separación. |
| 12 | `load_dotenv()` | Carga las variables de entorno desde el archivo `.env`. |
| 13 | *(Línea en blanco)* | Línea vacía de separación. |
| 14 | `SECRET_KEY = os.getenv("SECRET_KEY", "clave_super_secreta_ihc_presupuesto_estudiantil_2026")` | Lee la clave secreta usada para firmar los JWT o aplica una clave fija por defecto. |
| 15 | `ALGORITHM = os.getenv("ALGORITHM", "HS256")` | Lee el algoritmo de firma criptográfica (por defecto HMAC-SHA256: "HS256"). |
| 16 | `ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))` | Lee la duración de validez del token en minutos (1440 minutos = 24 horas). |
| 17 | *(Línea en blanco)* | Línea vacía de separación. |
| 18 | `security_bearer = HTTPBearer(auto_error=False)` | Instancia el extractor del encabezado `Authorization: Bearer <token>` sin fallar automáticamente. |
| 19 | *(Línea en blanco)* | Línea vacía de separación. |
| 20 | `def hash_password(password: str) -> str:` | Declara la función para encriptar una contraseña en texto plano. |
| 21 | `    return generate_password_hash(password)` | Retorna el hash criptográfico seguro generado por Werkzeug. |
| 22 | *(Línea en blanco)* | Línea vacía de separación. |
| 23 | `def verify_password(plain_password: str, hashed_password: str) -> bool:` | Declara la función para comparar una contraseña contra su hash guardado. |
| 24 | `    return check_password_hash(hashed_password, plain_password)` | Retorna `True` si la contraseña ingresada coincide con el hash, o `False` si no coincide. |
| 25 | *(Línea en blanco)* | Línea vacía de separación. |
| 26 | `def create_access_token(data: dict, expires_delta: timedelta = None) -> str:` | Declara la función para firmar y generar un token de acceso JWT. |
| 27 | `    to_encode = data.copy()` | Crea una copia del diccionario de datos (payload) para no modificar el parámetro original. |
| 28 | `    if expires_delta:` | Comprueba si se especificó un tiempo de expiración personalizado. |
| 29 | `        expire = datetime.utcnow() + expires_delta` | Suma el tiempo personalizado a la fecha y hora UTC actual. |
| 30 | `    else:` | Si no se especificó un tiempo personalizado. |
| 31 | `        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)` | Suma el tiempo estándar (24 horas) a la fecha y hora actual UTC. |
| 32 | `    to_encode.update({"exp": expire})` | Añade el reclamo de expiración `"exp"` al diccionario del payload. |
| 33 | `    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)` | Codifica y firma el token usando la clave secreta y el algoritmo seleccionado. |
| 34 | *(Línea en blanco)* | Línea vacía de separación. |
| 35 | `def get_current_user(` | Declara la función de dependencia para autenticar al usuario que hace una petición. |
| 36 | `    auth: HTTPAuthorizationCredentials = Depends(security_bearer),` | Extrae las credenciales Bearer de la cabecera HTTP `Authorization`. |
| 37 | `    db: Session = Depends(get_db)` | Inyecta la sesión activa de la base de datos. |
| 38 | `):` | Cierra los argumentos de la función `get_current_user`. |
| 39 | `    if not auth:` | Comprueba si la solicitud no contenía la cabecera de autenticación. |
| 40 | `        raise HTTPException(` | Lanza una excepción HTTP de falta de credenciales. |
| 41 | `            status_code=status.HTTP_401_UNAUTHORIZED,` | Retorna código HTTP 401 (No autorizado). |
| 42 | `            detail="No se proporcionó token de autenticación. Inicia sesión.",` | Mensaje instructivo solicitando iniciar sesión. |
| 43 | `            headers={"WWW-Authenticate": "Bearer"},` | Agrega la cabecera estándar HTTP indicando que el esquema requerido es Bearer. |
| 44 | `        )` | Cierra la definición de la excepción. |
| 45 | `    try:` | Inicia bloque de captura para decodificar y validar el token JWT. |
| 46 | `        payload = jwt.decode(auth.credentials, SECRET_KEY, algorithms=[ALGORITHM])` | Decodifica y verifica la firma criptográfica del token recibido. |
| 47 | `        user_id = payload.get("sub")` | Extrae el identificador del usuario desde el reclamo `"sub"` del payload. |
| 48 | `        if user_id is None:` | Verifica si el reclamo `"sub"` no vino presente en el payload. |
| 49 | `            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")` | Lanza error HTTP 401 indicando que el token es inválido. |
| 50 | `    except jwt.PyJWTError:` | Captura cualquier fallo de JWT (firma manipulada, formato corrupto o token vencido). |
| 51 | `        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado o inválido")` | Lanza error HTTP 401 indicando que el token ya no es válido. |
| 52 | *(Línea en blanco)* | Línea vacía de separación. |
| 53 | `    usuario = db.query(models.Usuario).filter(models.Usuario.id == int(user_id)).first()` | Busca en la base de datos al usuario cuyo ID coincide con el del token. |
| 54 | `    if usuario is None:` | Comprueba si el usuario no fue encontrado (por ejemplo, si fue borrado). |
| 55 | `        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")` | Lanza error HTTP 404 indicando que el usuario ya no existe. |
| 56 | `    return usuario` | Retorna el objeto `Usuario` autenticado para ser usado en el endpoint correspondiente. |
| 57 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

## correo.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/correo.py`  
Total de líneas: 49

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `import os` | Importa el módulo del sistema operativo para leer variables de configuración de correo. |
| 2 | `import smtplib` | Importa el cliente SMTP estándar de Python para comunicarse con servidores de correo. |
| 3 | `from email.message import EmailMessage` | Importa la clase `EmailMessage` para construir correos con texto y contenido HTML. |
| 4 | `from dotenv import load_dotenv` | Importa `load_dotenv` para cargar credenciales desde el archivo `.env`. |
| 5 | *(Línea en blanco)* | Línea vacía de separación. |
| 6 | `load_dotenv()` | Carga las variables de entorno desde el archivo `.env`. |
| 7 | *(Línea en blanco)* | Línea vacía de separación. |
| 8 | `SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")` | Lee el servidor host SMTP (por defecto el de Gmail: `"smtp.gmail.com"`). |
| 9 | `SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))` | Lee el puerto SMTP (por defecto 587 para conexión con cifrado STARTTLS). |
| 10 | `SMTP_USER = os.getenv("SMTP_USER", "")` | Lee el correo del remitente configurado en `.env`. |
| 11 | `SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")` | Lee la contraseña de aplicación o clave SMTP del remitente. |
| 12 | `SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Presupuesto Estudiantil")` | Lee el nombre visible que aparecerá en el remitente ("Presupuesto Estudiantil"). |
| 13 | *(Línea en blanco)* | Línea vacía de separación. |
| 14 | `def correo_configurado() -> bool:` | Declara la función que verifica si las credenciales de correo están configuradas. |
| 15 | `    return bool(SMTP_USER and SMTP_PASSWORD)` | Retorna `True` si existen usuario y contraseña en las variables; `False` en caso contrario. |
| 16 | *(Línea en blanco)* | Línea vacía de separación. |
| 17 | `def enviar_codigo_recuperacion(destino: str, nombre: str, codigo: str, minutos: int):` | Declara la función principal para despachar el correo con el código de 4 dígitos. |
| 18 | `    if not correo_configurado():` | Comprueba si el correo no tiene credenciales configuradas en el entorno. |
| 19 | `        print(f"[MODO DESARROLLO] Código de recuperación para {destino}: {codigo}")` | Imprime el código en la consola del backend para poder probar la recuperación en desarrollo local. |
| 20 | `        return` | Finaliza la función de inmediato sin intentar la conexión SMTP. |
| 21 | *(Línea en blanco)* | Línea vacía de separación. |
| 22 | `    msg = EmailMessage()` | Crea una nueva instancia de mensaje de correo electrónico. |
| 23 | `    msg["Subject"] = f"Tu código de verificación: {codigo}"` | Define el asunto del correo incluyendo el código de 4 dígitos. |
| 24 | `    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"` | Establece la cabecera del remitente con su nombre formal y dirección de correo. |
| 25 | `    msg["To"] = destino` | Establece el destinatario del correo con la dirección del estudiante. |
| 26 | `    msg.set_content(` | Define la versión de texto plano del mensaje para clientes de correo básicos. |
| 27 | `        f"Hola {nombre},\n\n"` | Saludo personalizado con el nombre del usuario. |
| 28 | `        f"Tu código para restablecer la contraseña es: {codigo}\n\n"` | Muestra el código de verificación en texto simple. |
| 29 | `        f"Vence en {minutos} minutos. Si no pediste este cambio, ignora este correo.\n\n"` | Instrucción de seguridad e indicación del tiempo de vencimiento. |
| 30 | `        f"— {SMTP_FROM_NAME}"` | Firma institucional del mensaje. |
| 31 | `    )` | Cierra el llamado a `set_content`. |
| 32 | `    msg.add_alternative(f"""\` | Añade una versión enriquecida en formato HTML visualmente atractiva. |
| 33 | `<div style="font-family: Arial, sans-serif; max-width: 440px; margin: auto; color: #0F172A;">` | Contenedor principal estilizado con ancho máximo de 440px para lectura óptima en móviles. |
| 34 | `  <h2 style="color: #154C86;">🎓 {SMTP_FROM_NAME}</h2>` | Título del correo con icono de birrete universitario en color azul corporativo. |
| 35 | `  <p>Hola <strong>{nombre}</strong>,</p>` | Párrafo saludando al estudiante con su nombre en negrita. |
| 36 | `  <p>Usa este código para restablecer tu contraseña:</p>` | Texto explicativo del motivo del correo. |
| 37 | `  <p style="font-size: 34px; font-weight: bold; letter-spacing: 12px; color: #2E7D9A;` | Estilo de la caja destacada: tamaño grande de 34px y espaciado de 12px entre dígitos. |
| 38 | `            background: #E0F2F7; padding: 14px; text-align: center; border-radius: 8px;">{codigo}</p>` | Fondo azul claro suave, relleno amplio, centrado y bordes redondeados con el código insertado. |
| 39 | `  <p style="color: #475569; font-size: 14px;">` | Estilo secundario en color gris para el aviso de seguridad. |
| 40 | `    Vence en {minutos} minutos. Si no pediste este cambio, ignora este correo.` | Mensaje de advertencia de vencimiento en HTML. |
| 41 | `  </p>` | Cierra el párrafo secundario. |
| 42 | `</div>` | Cierra el contenedor HTML principal. |
| 43 | `""", subtype="html")` | Cierra la adición del contenido HTML especificando el subtipo `"html"`. |
| 44 | *(Línea en blanco)* | Línea vacía de separación. |
| 45 | `    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as servidor:` | Abre la conexión con el servidor SMTP con tiempo límite de 15 segundos. |
| 46 | `        servidor.starttls()` | Inicia el canal seguro encriptado mediante STARTTLS. |
| 47 | `        servidor.login(SMTP_USER, SMTP_PASSWORD)` | Autentica la sesión en el servidor SMTP con usuario y contraseña. |
| 48 | `        servidor.send_message(msg)` | Transmite y envía el mensaje de correo al destinatario. |
| 49 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---

# 3. Carpeta: tests

## test_estado_movimiento.py
Ruta: `PRESUPUESTO ESTUDIANTIL/BACKEND/tests/test_estado_movimiento.py`  
Total de líneas: 222

| Línea | Código | Qué hace |
|---|---|---|
| 1 | `"""` | Inicia bloque de documentación general del módulo de pruebas. |
| 2 | `=============================================================================` | Línea divisoria decorativa en el comentario. |
| 3 | `PRUEBAS UNITARIAS: MÁQUINA DE ESTADOS - PRESUPUESTO ESTUDIANTIL (TAREA 2)` | Título formal del conjunto de pruebas requeridas para la Tarea 2. |
| 4 | `=============================================================================` | Línea divisoria decorativa. |
| 5 | `Proyecto: Presupuesto Estudiantil` | Identifica el proyecto evaluado. |
| 6 | `Entidad: Movimiento (Gasto)` | Identifica la entidad bajo prueba. |
| 7 | `Regla de estado: Pendiente -> Pagado` | Describe la transición de la máquina de estados. |
| 8 | `Acción: "Marcar como pagado"` | Identifica el nombre de la acción evaluada. |
| 9 | `` | Línea vacía dentro del docstring. |
| 10 | `Pruebas requeridas según especificación:` | Lista de los 4 requerimientos obligatorios de la tarea. |
| 11 | `1. El estado inicial es el correcto ('pendiente').` | Requisito 1 de la prueba. |
| 12 | `2. La acción realiza la transición esperada ('pendiente' -> 'pagado').` | Requisito 2 de la prueba. |
| 13 | `3. Una transición inválida se rechaza (intentar pagar uno ya pagado rechaza con 400).` | Requisito 3 de la prueba. |
| 14 | `4. Los demás datos del elemento se conservan (monto, descripción, fecha, etc.).` | Requisito 4 de la prueba. |
| 15 | `=============================================================================` | Línea divisoria decorativa. |
| 16 | `"""` | Cierra el docstring del módulo. |
| 17 | *(Línea en blanco)* | Línea vacía de separación. |
| 18 | `import pytest` | Importa el framework de pruebas automatizadas Pytest. |
| 19 | `from datetime import date` | Importa la clase `date` para fijar fechas concretas en los tests. |
| 20 | `from sqlalchemy import create_engine` | Importa `create_engine` para instanciar una base de datos aislada para los tests. |
| 21 | `from sqlalchemy.orm import sessionmaker` | Importa `sessionmaker` para generar sesiones de prueba. |
| 22 | `from fastapi.testclient import TestClient` | Importa `TestClient` de FastAPI para simular peticiones HTTP a los endpoints sin levantar un servidor real. |
| 23 | *(Línea en blanco)* | Línea vacía de separación. |
| 24 | `import sys` | Importa el módulo de sistema para manipular las rutas de búsqueda de Python. |
| 25 | `import os` | Importa el módulo del sistema operativo. |
| 26 | `sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` | Añade la carpeta raíz de `BACKEND` al `sys.path` para poder importar módulos vecinos (`main`, `database`, etc.). |
| 27 | *(Línea en blanco)* | Línea vacía de separación. |
| 28 | `from database import Base, get_db` | Importa `Base` y la dependencia `get_db` de la aplicación. |
| 29 | `import models` | Importa los modelos ORM de la base de datos. |
| 30 | `from main import app` | Importa la aplicación principal de FastAPI sobre la cual se ejecutarán las pruebas. |
| 31 | `from security import get_current_user` | Importa la dependencia de autenticación para poder sustituirla en las pruebas. |
| 32 | *(Línea en blanco)* | Línea vacía de separación. |
| 33 | `from sqlalchemy.pool import StaticPool` | Importa `StaticPool` para que la base de datos SQLite en memoria mantenga una única conexión compartida entre hilos. |
| 34 | *(Línea en blanco)* | Línea vacía de separación. |
| 35 | `# Base de datos SQLite aislada en memoria para pruebas rápidas e independientes` | Comentario explicativo del entorno aislado de prueba. |
| 36 | `SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"` | Define la URL de conexión especial a SQLite en memoria RAM. |
| 37 | *(Línea en blanco)* | Línea vacía de separación. |
| 38 | `engine_test = create_engine(` | Crea el motor de base de datos específico para las pruebas. |
| 39 | `    SQLALCHEMY_TEST_DATABASE_URL,` | Pasa la URL de base de datos en memoria. |
| 40 | `    connect_args={"check_same_thread": False},` | Permite usar la conexión a través de diferentes hilos. |
| 41 | `    poolclass=StaticPool` | Mantiene la misma base de datos viva mientras duren las consultas del test. |
| 42 | `)` | Cierra la llamada de `create_engine`. |
| 43 | `TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)` | Crea la fábrica de sesiones de base de datos conectada al motor de pruebas. |
| 44 | *(Línea en blanco)* | Línea vacía de separación. |
| 45 | `# Fixture de base de datos para cada test` | Comentario sobre el fixture de base de datos. |
| 46 | `@pytest.fixture(scope="function")` | Define un fixture de Pytest con alcance de función (se ejecuta limpio para cada test). |
| 47 | `def db_session():` | Declara la función del fixture que prepara la base de datos. |
| 48 | `    Base.metadata.create_all(bind=engine_test)` | Crea todas las tablas en la base de datos en memoria antes de comenzar el test. |
| 49 | `    db = TestingSessionLocal()` | Abre una sesión de prueba en la base de datos en memoria. |
| 50 | `    try:` | Inicia bloque `try` para entregar la sesión. |
| 51 | `        # Crear usuario de prueba` | Comentario explicativo de la inserción de usuario base. |
| 52 | `        usuario_test = models.Usuario(` | Instancia un usuario ficticio para las pruebas. |
| 53 | `            id=1,` | ID fijo 1. |
| 54 | `            nombre="Estudiante Prueba",` | Nombre del estudiante de pruebas. |
| 55 | `            email="test@universidad.edu",` | Correo de pruebas. |
| 56 | `            password_hash="hash_seguro_123"` | Hash simulado de contraseña. |
| 57 | `        )` | Cierra la creación del usuario. |
| 58 | `        db.add(usuario_test)` | Agrega el usuario de prueba a la sesión. |
| 59 | `        db.commit()` | Guarda el usuario en la base de datos en memoria. |
| 60 | `        yield db` | Entrega la sesión al caso de prueba en ejecución. |
| 61 | `    finally:` | Bloque de limpieza posterior a cada test. |
| 62 | `        db.close()` | Cierra la sesión de prueba. |
| 63 | `        Base.metadata.drop_all(bind=engine_test)` | Destruye todas las tablas en memoria para dejar el entorno 100% limpio para el siguiente test. |
| 64 | *(Línea en blanco)* | Línea vacía de separación. |
| 65 | `# Fixture de cliente FastAPI con autenticación y BD simuladas` | Comentario explicativo del cliente HTTP de pruebas. |
| 66 | `@pytest.fixture(scope="function")` | Declara un fixture de cliente HTTP por función. |
| 67 | `def client(db_session):` | Recibe la sesión de base de datos de prueba como dependencia. |
| 68 | `    def override_get_db():` | Función de sustitución que entrega la sesión de prueba en lugar de la BD real. |
| 69 | `        try:` | Abre bloque try para la entrega de sesión. |
| 70 | `            yield db_session` | Entrega la sesión en memoria. |
| 71 | `        finally:` | Bloque finalizador. |
| 72 | `            pass` | No realiza acción extra. |
| 73 | *(Línea en blanco)* | Línea vacía de separación. |
| 74 | `    def override_get_current_user():` | Función de sustitución para simular que el usuario con ID=1 ya está autenticado. |
| 75 | `        return db_session.query(models.Usuario).filter(models.Usuario.id == 1).first()` | Retorna directamente el usuario de prueba sin requerir cabecera JWT real. |
| 76 | *(Línea en blanco)* | Línea vacía de separación. |
| 77 | `    app.dependency_overrides[get_db] = override_get_db` | Sobrescribe la dependencia `get_db` de FastAPI con la versión de prueba en memoria. |
| 78 | `    app.dependency_overrides[get_current_user] = override_get_current_user` | Sobrescribe la dependencia `get_current_user` para saltarse la autenticación en los tests. |
| 79 | *(Línea en blanco)* | Línea vacía de separación. |
| 80 | `    with TestClient(app) as test_client:` | Crea el cliente de pruebas conectado a la aplicación configurada. |
| 81 | `        yield test_client` | Entrega el cliente HTTP al caso de prueba. |
| 82 | *(Línea en blanco)* | Línea vacía de separación. |
| 83 | `    app.dependency_overrides.clear()` | Limpia las sustituciones de dependencias al finalizar el test para no afectar otras pruebas. |
| 84 | *(Línea en blanco)* | Línea vacía de separación. |
| 85 | *(Línea en blanco)* | Línea vacía de separación. |
| 86 | `# =============================================================================` | Separador de sección. |
| 87 | `# PRUEBA 1: EL ESTADO INICIAL ES EL CORRECTO` | Identificador del Caso de Prueba 1. |
| 88 | `# =============================================================================` | Separador de sección. |
| 89 | `def test_01_estado_inicial_es_correcto(client, db_session):` | Función de prueba para verificar que el estado por defecto al crear un gasto sea 'pendiente'. |
| 90 | `    """` | Inicia docstring de la prueba 1. |
| 91 | `    Verifica que al registrar un nuevo gasto/movimiento, ` | Explicación del objetivo de la prueba. |
| 92 | `    su estado inicial sea obligatoriamente 'pendiente'.` | Detalle del requisito verificado. |
| 93 | `    """` | Cierra docstring. |
| 94 | `    payload = {` | Define el cuerpo JSON enviado para crear el movimiento. |
| 95 | `        "descripcion": "Transporte U",` | Descripción del gasto. |
| 96 | `        "monto": 25.00,` | Monto del gasto. |
| 97 | `        "tipo": "gasto",` | Tipo de movimiento: gasto. |
| 98 | `        "categoria": "General"` | Categoría: General. |
| 99 | `    }` | Cierra el diccionario del payload. |
| 100 | `    response = client.post("/movimientos", json=payload)` | Envía petición HTTP POST a `/movimientos` usando el cliente de prueba. |
| 101 | *(Línea en blanco)* | Línea vacía de separación. |
| 102 | `    assert response.status_code == 200, f"Error al crear movimiento: {response.text}"` | Aserción: confirma que el endpoint respondió con código HTTP 200 (éxito). |
| 103 | `    datos = response.json()` | Convierte el cuerpo de la respuesta a un diccionario de Python. |
| 104 | *(Línea en blanco)* | Línea vacía de separación. |
| 105 | `    # Comprobación de estado inicial` | Comentario sobre la verificación clave. |
| 106 | `    assert datos["estado"] == "pendiente", f"Se esperaba 'pendiente' pero se obtuvo '{datos.get('estado')}'"` | Aserción: confirma que el campo `estado` en la respuesta JSON es obligatoriamente `'pendiente'`. |
| 107 | *(Línea en blanco)* | Línea vacía de separación. |
| 108 | `    # Comprobar directamente en la base de datos` | Comentario sobre la verificación en BD. |
| 109 | `    mov_db = db_session.query(models.Movimiento).filter(models.Movimiento.id == datos["id"]).first()` | Consulta el registro directamente en la base de datos usando la sesión. |
| 110 | `    assert mov_db is not None` | Aserción: confirma que el registro realmente existe en la base de datos. |
| 111 | `    assert mov_db.estado == "pendiente"` | Aserción: confirma que en la tabla física de la BD el valor de `estado` es `'pendiente'`. |
| 112 | *(Línea en blanco)* | Línea vacía de separación. |
| 113 | *(Línea en blanco)* | Línea vacía de separación. |
| 114 | `# =============================================================================` | Separador de sección. |
| 115 | `# PRUEBA 2: LA ACCIÓN REALIZA LA TRANSICIÓN ESPERADA` | Identificador del Caso de Prueba 2. |
| 116 | `# =============================================================================` | Separador de sección. |
| 117 | `def test_02_accion_realiza_transicion_esperada(client, db_session):` | Función de prueba para verificar la transición de 'pendiente' a 'pagado'. |
| 118 | `    """` | Inicia docstring de la prueba 2. |
| 119 | `    Verifica que al invocar la acción 'Marcar como pagado',` | Explicación del objetivo de la prueba. |
| 120 | `    el movimiento transicione correctamente de 'pendiente' a 'pagado'.` | Detalle de la transición evaluada. |
| 121 | `    """` | Cierra docstring. |
| 122 | `    # 1. Crear movimiento inicial en estado pendiente` | Comentario del paso 1. |
| 123 | `    mov = models.Movimiento(` | Instancia directamente un movimiento en el modelo ORM. |
| 124 | `        usuario_id=1,` | Vinculado al usuario 1. |
| 125 | `        monto=25.00,` | Monto de 25.00. |
| 126 | `        tipo="gasto",` | Tipo gasto. |
| 127 | `        descripcion="Transporte U",` | Descripción del gasto. |
| 128 | `        fecha=date(2026, 10, 5),` | Fecha fija. |
| 129 | `        estado="pendiente"` | Estado inicial en 'pendiente'. |
| 130 | `    )` | Cierra la instanciación. |
| 131 | `    db_session.add(mov)` | Añade el movimiento a la sesión. |
| 132 | `    db_session.commit()` | Confirma y guarda el movimiento en la BD. |
| 133 | `    db_session.refresh(mov)` | Recarga los datos para obtener el ID asignado. |
| 134 | `    assert mov.estado == "pendiente"` | Aserción: confirma que el movimiento nació en estado 'pendiente'. |
| 135 | *(Línea en blanco)* | Línea vacía de separación. |
| 136 | `    # 2. Ejecutar la acción 'Marcar como pagado' (PATCH /movimientos/{id}/pagar)` | Comentario del paso 2. |
| 137 | `    response = client.patch(f"/movimientos/{mov.id}/pagar")` | Envía petición HTTP PATCH al endpoint de pagar con el ID del movimiento recién creado. |
| 138 | *(Línea en blanco)* | Línea vacía de separación. |
| 139 | `    assert response.status_code == 200, f"La transición falló: {response.text}"` | Aserción: confirma que la respuesta HTTP tiene código 200 (éxito). |
| 140 | `    datos = response.json()` | Convierte la respuesta a formato JSON. |
| 141 | *(Línea en blanco)* | Línea vacía de separación. |
| 142 | `    # 3. Comprobar que el estado resultante es 'pagado'` | Comentario del paso 3. |
| 143 | `    assert datos["estado"] == "pagado", f"Se esperaba 'pagado' pero se obtuvo '{datos.get('estado')}'"` | Aserción: confirma que en la respuesta de la API el estado cambió exitosamente a `'pagado'`. |
| 144 | *(Línea en blanco)* | Línea vacía de separación. |
| 145 | `    # 4. Comprobar que en la base de datos persiste el cambio a 'pagado'` | Comentario del paso 4. |
| 146 | `    db_session.refresh(mov)` | Recarga los datos del registro directamente desde la base de datos. |
| 147 | `    assert mov.estado == "pagado"` | Aserción: confirma que en la base de datos el valor de `estado` ahora es `'pagado'`. |
| 148 | *(Línea en blanco)* | Línea vacía de separación. |
| 149 | *(Línea en blanco)* | Línea vacía de separación. |
| 150 | `# =============================================================================` | Separador de sección. |
| 151 | `# PRUEBA 3: UNA TRANSICIÓN INVÁLIDA SE RECHAZA` | Identificador del Caso de Prueba 3. |
| 152 | `# =============================================================================` | Separador de sección. |
| 153 | `def test_03_transicion_invalida_se_rechaza(client, db_session):` | Función de prueba para verificar el rechazo de transiciones prohibidas. |
| 154 | `    """` | Inicia docstring de la prueba 3. |
| 155 | `    Verifica que si un elemento ya está en estado 'pagado', ` | Explicación del caso de prueba. |
| 156 | `    intentar volver a marcarlo como pagado es una transición inválida y se rechaza.` | Detalle del rechazo con HTTP 400. |
| 157 | `    """` | Cierra docstring. |
| 158 | `    # 1. Crear movimiento que YA se encuentra en estado 'pagado'` | Comentario del paso 1. |
| 159 | `    mov = models.Movimiento(` | Instancia un movimiento directamente en el modelo ORM. |
| 160 | `        usuario_id=1,` | Usuario 1. |
| 161 | `        monto=15.50,` | Monto de 15.50. |
| 162 | `        tipo="gasto",` | Tipo gasto. |
| 163 | `        descripcion="Fotocopias",` | Concepto. |
| 164 | `        fecha=date(2026, 10, 5),` | Fecha fija. |
| 165 | `        estado="pagado"` | Estado ya en 'pagado' intencionalmente. |
| 166 | `    )` | Cierra instanciación. |
| 167 | `    db_session.add(mov)` | Añade el movimiento a la sesión. |
| 168 | `    db_session.commit()` | Guarda el movimiento en la BD. |
| 169 | `    db_session.refresh(mov)` | Recarga los datos. |
| 170 | *(Línea en blanco)* | Línea vacía de separación. |
| 171 | `    # 2. Intentar ejecutar nuevamente la acción sobre un elemento ya pagado` | Comentario del paso 2. |
| 172 | `    response = client.patch(f"/movimientos/{mov.id}/pagar")` | Intenta invocar la acción de pago sobre el movimiento que ya estaba pagado. |
| 173 | *(Línea en blanco)* | Línea vacía de separación. |
| 174 | `    # 3. Debe ser rechazado con código HTTP 400 Bad Request` | Comentario del paso 3. |
| 175 | `    assert response.status_code == 400, f"Se esperaba HTTP 400 pero se obtuvo {response.status_code}"` | Aserción: confirma que la API rechaza la petición con código de error HTTP 400. |
| 176 | *(Línea en blanco)* | Línea vacía de separación. |
| 177 | `    detalle = response.json().get("detail", "")` | Extrae el mensaje de error `detail` del cuerpo de la respuesta. |
| 178 | `    assert "inválida" in detalle or "invalida" in detalle or "ya se encuentra en estado pagado" in detalle` | Aserción: confirma que el mensaje explica que la transición es inválida o que ya estaba pagado. |
| 179 | *(Línea en blanco)* | Línea vacía de separación. |
| 180 | `    # 4. El estado en BD no debió alterarse` | Comentario del paso 4. |
| 181 | `    db_session.refresh(mov)` | Recarga el registro desde la BD para verificar su integridad. |
| 182 | `    assert mov.estado == "pagado"` | Aserción: confirma que el estado en la base de datos se mantiene firme en `'pagado'`. |
| 183 | *(Línea en blanco)* | Línea vacía de separación. |
| 184 | *(Línea en blanco)* | Línea vacía de separación. |
| 185 | `# =============================================================================` | Separador de sección. |
| 186 | `# PRUEBA 4: LOS DEMÁS DATOS DEL ELEMENTO SE CONSERVAN` | Identificador del Caso de Prueba 4. |
| 187 | `# =============================================================================` | Separador de sección. |
| 188 | `def test_04_demas_datos_del_elemento_se_conservan(client, db_session):` | Función de prueba para verificar que la transición no corrompe ni altera los demás atributos. |
| 189 | `    """` | Inicia docstring de la prueba 4. |
| 190 | `    Verifica que la transición de estado a 'pagado' no mute, corrompa` | Explicación del objetivo de la prueba. |
| 191 | `    ni borre los demás atributos del movimiento (monto, descripcion, fecha, usuario_id).` | Lista de atributos cuya integridad se comprueba. |
| 192 | `    """` | Cierra docstring. |
| 193 | `    # 1. Crear movimiento con datos específicos` | Comentario del paso 1. |
| 194 | `    monto_original = 48.50` | Define un monto de referencia para contrastar luego. |
| 195 | `    descripcion_original = "Libros de Texto (Uni)"` | Define una descripción de referencia. |
| 196 | `    fecha_original = date(2026, 10, 3)` | Define una fecha de referencia. |
| 197 | *(Línea en blanco)* | Línea vacía de separación. |
| 198 | `    mov = models.Movimiento(` | Instancia el movimiento en estado pendiente con esos datos específicos. |
| 199 | `        usuario_id=1,` | Usuario 1. |
| 200 | `        monto=monto_original,` | Monto de referencia. |
| 201 | `        tipo="gasto",` | Tipo gasto. |
| 202 | `        descripcion=descripcion_original,` | Descripción de referencia. |
| 203 | `        fecha=fecha_original,` | Fecha de referencia. |
| 204 | `        estado="pendiente"` | Estado inicial pendiente. |
| 205 | `    )` | Cierra instanciación. |
| 206 | `    db_session.add(mov)` | Añade a la sesión. |
| 207 | `    db_session.commit()` | Guarda en la BD. |
| 208 | `    db_session.refresh(mov)` | Recarga para obtener ID. |
| 209 | *(Línea en blanco)* | Línea vacía de separación. |
| 210 | `    # 2. Ejecutar la acción` | Comentario del paso 2. |
| 211 | `    response = client.patch(f"/movimientos/{mov.id}/pagar")` | Ejecuta la acción "Marcar como pagado" llamando al endpoint. |
| 212 | `    assert response.status_code == 200` | Aserción: confirma que la respuesta es exitosa (HTTP 200). |
| 213 | *(Línea en blanco)* | Línea vacía de separación. |
| 214 | `    # 3. Verificar en la respuesta y en la base de datos que todos los demás campos siguen iguales` | Comentario del paso 3. |
| 215 | `    db_session.refresh(mov)` | Recarga los datos actualizados desde la base de datos. |
| 216 | `    assert mov.estado == "pagado", "El estado debió cambiar a pagado"` | Aserción: confirma que el único cambio previsto ocurrió (`estado` pasó a `'pagado'`). |
| 217 | `    assert float(mov.monto) == monto_original, "El monto cambió indebidamente"` | Aserción: confirma que el monto sigue siendo exactamente 48.50 sin ninguna alteración. |
| 218 | `    assert mov.descripcion == descripcion_original, "La descripción cambió indebidamente"` | Aserción: confirma que la descripción se preservó intacta. |
| 219 | `    assert mov.fecha == fecha_original, "La fecha cambió indebidamente"` | Aserción: confirma que la fecha se preservó intacta. |
| 220 | `    assert mov.usuario_id == 1, "El usuario_id cambió indebidamente"` | Aserción: confirma que el ID del usuario propietario no fue modificado. |
| 221 | `    assert mov.tipo == "gasto", "El tipo cambió indebidamente"` | Aserción: confirma que el tipo de movimiento continúa siendo `'gasto'`. |
| 222 | *(Línea en blanco)* | Fin del archivo conforme al estándar PEP 8. |

---
