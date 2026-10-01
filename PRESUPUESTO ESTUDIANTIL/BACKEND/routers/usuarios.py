import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from security import hash_password, verify_password, create_access_token, get_current_user
from correo import enviar_codigo_recuperacion

CODIGO_MINUTOS = 10
CODIGO_MAX_INTENTOS = 5

router = APIRouter(prefix="/auth", tags=["Autenticación y Usuarios"])

@router.post("/registro", response_model=schemas.TokenResponse)
def registrar_usuario(datos: schemas.UsuarioRegistro, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(models.Usuario.email == datos.email.lower()).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta con este correo institucional o personal."
        )

    nuevo_usuario = models.Usuario(
        nombre=datos.nombre.strip(),
        email=datos.email.lower().strip(),
        password_hash=hash_password(datos.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    token = create_access_token({"sub": str(nuevo_usuario.id), "email": nuevo_usuario.email})

    return {
        "token": token,
        "usuario": nuevo_usuario
    }

@router.post("/login", response_model=schemas.TokenResponse)
def login(datos: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == datos.email.lower()).first()
    if not usuario or not verify_password(datos.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos."
        )

    token = create_access_token({"sub": str(usuario.id), "email": usuario.email})

    return {
        "token": token,
        "usuario": usuario
    }

def _buscar_usuario(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email.lower().strip()).first()

def _validar_codigo(db: Session, usuario, codigo: str):
    if not usuario or not usuario.token_recuperacion or not usuario.codigo_expira:
        raise HTTPException(status_code=400, detail="Primero solicita un código de verificación.")
    if datetime.utcnow() > usuario.codigo_expira:
        raise HTTPException(status_code=400, detail="El código venció. Solicita uno nuevo.")
    if (usuario.codigo_intentos or 0) >= CODIGO_MAX_INTENTOS:
        raise HTTPException(status_code=400, detail="Demasiados intentos fallidos. Solicita un código nuevo.")
    if not verify_password(codigo.strip(), usuario.token_recuperacion):
        usuario.codigo_intentos = (usuario.codigo_intentos or 0) + 1
        db.commit()
        restantes = CODIGO_MAX_INTENTOS - usuario.codigo_intentos
        if restantes <= 0:
            raise HTTPException(status_code=400, detail="Código incorrecto. Ya no te quedan intentos: solicita un código nuevo.")
        palabra = "intento" if restantes == 1 else "intentos"
        raise HTTPException(status_code=400, detail=f"Código incorrecto. Te quedan {restantes} {palabra}.")

@router.post("/recuperar/solicitar")
def solicitar_codigo(datos: schemas.SolicitarCodigo, db: Session = Depends(get_db)):
    usuario = _buscar_usuario(db, datos.email)
    if usuario and usuario.es_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta demo es solo de muestra: no se puede cambiar su contraseña."
        )

    if usuario:
        codigo = f"{secrets.randbelow(10000):04d}"
        usuario.token_recuperacion = hash_password(codigo)
        usuario.codigo_expira = datetime.utcnow() + timedelta(minutes=CODIGO_MINUTOS)
        usuario.codigo_intentos = 0
        db.commit()
        try:
            enviar_codigo_recuperacion(usuario.email, usuario.nombre, codigo, CODIGO_MINUTOS)
        except Exception as err:
            print(f"Error al enviar el correo: {err}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="No se pudo enviar el correo. Intenta de nuevo en unos minutos."
            )

    return {"mensaje": "Si el correo está registrado, te enviamos un código de 4 dígitos."}

@router.post("/recuperar/verificar")
def verificar_codigo(datos: schemas.VerificarCodigo, db: Session = Depends(get_db)):
    _validar_codigo(db, _buscar_usuario(db, datos.email), datos.codigo)
    return {"mensaje": "Código verificado."}

@router.post("/recuperar/restablecer")
def restablecer_password(datos: schemas.RestablecerPassword, db: Session = Depends(get_db)):
    usuario = _buscar_usuario(db, datos.email)
    _validar_codigo(db, usuario, datos.codigo)
    if len(datos.nueva_password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres.")

    usuario.password_hash = hash_password(datos.nueva_password)
    usuario.token_recuperacion = None
    usuario.codigo_expira = None
    usuario.codigo_intentos = 0
    db.commit()

    return {"mensaje": "Contraseña actualizada exitosamente."}

@router.get("/me", response_model=schemas.UsuarioOut)
def obtener_perfil(usuario: models.Usuario = Depends(get_current_user)):
    return usuario
