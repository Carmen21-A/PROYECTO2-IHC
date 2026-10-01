from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

DEMO_EMAIL = "estudiante@demo.com"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    token_recuperacion = Column(String(255), nullable=True)
    codigo_expira = Column(DateTime, nullable=True)
    codigo_intentos = Column(Integer, default=0)
    creado_en = Column(DateTime, default=datetime.utcnow)

    movimientos = relationship("Movimiento", back_populates="usuario", cascade="all, delete-orphan")

    @property
    def es_demo(self) -> bool:
        return self.email == DEMO_EMAIL

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    tipo = Column(String(10), nullable=False)
    icono = Column(String(50), default="tag")

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True)
    monto = Column(Numeric(10, 2), nullable=False)
    tipo = Column(String(10), nullable=False)
    descripcion = Column(String(255), nullable=False)
    fecha = Column(Date, default=datetime.utcnow().date)
    creado_en = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="movimientos")
