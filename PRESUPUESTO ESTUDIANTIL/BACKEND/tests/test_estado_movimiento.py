"""
=============================================================================
PRUEBAS UNITARIAS: MÁQUINA DE ESTADOS - PRESUPUESTO ESTUDIANTIL (TAREA 2)
=============================================================================
Proyecto: Presupuesto Estudiantil
Entidad: Movimiento (Gasto)
Regla de estado: Pendiente -> Pagado
Acción: "Marcar como pagado"

Pruebas requeridas según especificación:
1. El estado inicial es el correcto ('pendiente').
2. La acción realiza la transición esperada ('pendiente' -> 'pagado').
3. Una transición inválida se rechaza (intentar pagar uno ya pagado rechaza con 400).
4. Los demás datos del elemento se conservan (monto, descripción, fecha, etc.).
=============================================================================
"""

import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, get_db
import models
from main import app
from security import get_current_user

from sqlalchemy.pool import StaticPool

# Base de datos SQLite aislada en memoria para pruebas rápidas e independientes
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Fixture de base de datos para cada test
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        # Crear usuario de prueba
        usuario_test = models.Usuario(
            id=1,
            nombre="Estudiante Prueba",
            email="test@universidad.edu",
            password_hash="hash_seguro_123"
        )
        db.add(usuario_test)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)

# Fixture de cliente FastAPI con autenticación y BD simuladas
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():
        return db_session.query(models.Usuario).filter(models.Usuario.id == 1).first()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()


# =============================================================================
# PRUEBA 1: EL ESTADO INICIAL ES EL CORRECTO
# =============================================================================
def test_01_estado_inicial_es_correcto(client, db_session):
    """
    Verifica que al registrar un nuevo gasto/movimiento, 
    su estado inicial sea obligatoriamente 'pendiente'.
    """
    payload = {
        "descripcion": "Transporte U",
        "monto": 25.00,
        "tipo": "gasto",
        "categoria": "General"
    }
    response = client.post("/movimientos", json=payload)
    
    assert response.status_code == 200, f"Error al crear movimiento: {response.text}"
    datos = response.json()
    
    # Comprobación de estado inicial
    assert datos["estado"] == "pendiente", f"Se esperaba 'pendiente' pero se obtuvo '{datos.get('estado')}'"
    
    # Comprobar directamente en la base de datos
    mov_db = db_session.query(models.Movimiento).filter(models.Movimiento.id == datos["id"]).first()
    assert mov_db is not None
    assert mov_db.estado == "pendiente"


# =============================================================================
# PRUEBA 2: LA ACCIÓN REALIZA LA TRANSICIÓN ESPERADA
# =============================================================================
def test_02_accion_realiza_transicion_esperada(client, db_session):
    """
    Verifica que al invocar la acción 'Marcar como pagado',
    el movimiento transicione correctamente de 'pendiente' a 'pagado'.
    """
    # 1. Crear movimiento inicial en estado pendiente
    mov = models.Movimiento(
        usuario_id=1,
        monto=25.00,
        tipo="gasto",
        descripcion="Transporte U",
        fecha=date(2026, 10, 5),
        estado="pendiente"
    )
    db_session.add(mov)
    db_session.commit()
    db_session.refresh(mov)
    assert mov.estado == "pendiente"

    # 2. Ejecutar la acción 'Marcar como pagado' (PATCH /movimientos/{id}/pagar)
    response = client.patch(f"/movimientos/{mov.id}/pagar")
    
    assert response.status_code == 200, f"La transición falló: {response.text}"
    datos = response.json()
    
    # 3. Comprobar que el estado resultante es 'pagado'
    assert datos["estado"] == "pagado", f"Se esperaba 'pagado' pero se obtuvo '{datos.get('estado')}'"
    
    # 4. Comprobar que en la base de datos persiste el cambio a 'pagado'
    db_session.refresh(mov)
    assert mov.estado == "pagado"


# =============================================================================
# PRUEBA 3: UNA TRANSICIÓN INVÁLIDA SE RECHAZA
# =============================================================================
def test_03_transicion_invalida_se_rechaza(client, db_session):
    """
    Verifica que si un elemento ya está en estado 'pagado', 
    intentar volver a marcarlo como pagado es una transición inválida y se rechaza.
    """
    # 1. Crear movimiento que YA se encuentra en estado 'pagado'
    mov = models.Movimiento(
        usuario_id=1,
        monto=15.50,
        tipo="gasto",
        descripcion="Fotocopias",
        fecha=date(2026, 10, 5),
        estado="pagado"
    )
    db_session.add(mov)
    db_session.commit()
    db_session.refresh(mov)

    # 2. Intentar ejecutar nuevamente la acción sobre un elemento ya pagado
    response = client.patch(f"/movimientos/{mov.id}/pagar")
    
    # 3. Debe ser rechazado con código HTTP 400 Bad Request
    assert response.status_code == 400, f"Se esperaba HTTP 400 pero se obtuvo {response.status_code}"
    
    detalle = response.json().get("detail", "")
    assert "inválida" in detalle or "invalida" in detalle or "ya se encuentra en estado pagado" in detalle
    
    # 4. El estado en BD no debió alterarse
    db_session.refresh(mov)
    assert mov.estado == "pagado"


# =============================================================================
# PRUEBA 4: LOS DEMÁS DATOS DEL ELEMENTO SE CONSERVAN
# =============================================================================
def test_04_demas_datos_del_elemento_se_conservan(client, db_session):
    """
    Verifica que la transición de estado a 'pagado' no mute, corrompa
    ni borre los demás atributos del movimiento (monto, descripcion, fecha, usuario_id).
    """
    # 1. Crear movimiento con datos específicos
    monto_original = 48.50
    descripcion_original = "Libros de Texto (Uni)"
    fecha_original = date(2026, 10, 3)
    
    mov = models.Movimiento(
        usuario_id=1,
        monto=monto_original,
        tipo="gasto",
        descripcion=descripcion_original,
        fecha=fecha_original,
        estado="pendiente"
    )
    db_session.add(mov)
    db_session.commit()
    db_session.refresh(mov)

    # 2. Ejecutar la acción
    response = client.patch(f"/movimientos/{mov.id}/pagar")
    assert response.status_code == 200

    # 3. Verificar en la respuesta y en la base de datos que todos los demás campos siguen iguales
    db_session.refresh(mov)
    assert mov.estado == "pagado", "El estado debió cambiar a pagado"
    assert float(mov.monto) == monto_original, "El monto cambió indebidamente"
    assert mov.descripcion == descripcion_original, "La descripción cambió indebidamente"
    assert mov.fecha == fecha_original, "La fecha cambió indebidamente"
    assert mov.usuario_id == 1, "El usuario_id cambió indebidamente"
    assert mov.tipo == "gasto", "El tipo cambió indebidamente"
