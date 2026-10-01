from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    es_demo: bool = False

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    token: str
    usuario: UsuarioOut

class SolicitarCodigo(BaseModel):
    email: str

class VerificarCodigo(BaseModel):
    email: str
    codigo: str

class RestablecerPassword(BaseModel):
    email: str
    codigo: str
    nueva_password: str

class MovimientoCreate(BaseModel):
    descripcion: str
    categoria: str
    monto: float
    tipo: str
    fecha: Optional[str] = None

class MovimientoOut(BaseModel):
    id: int
    descripcion: str
    categoria: str
    monto: float
    tipo: str
    fecha: str

    class Config:
        from_attributes = True

class ResumenFinanciero(BaseModel):
    saldo_disponible: float
    ingresos_del_mes: float
    gastos_del_mes: float
    movimientos: List[MovimientoOut]

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    tipo: str
    icono: str

    class Config:
        from_attributes = True
