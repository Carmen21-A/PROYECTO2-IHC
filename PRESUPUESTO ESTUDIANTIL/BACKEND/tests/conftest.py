"""Fixtures compartidos por las pruebas: BD SQLite en memoria y cliente autenticado."""

import pytest
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


#prepara todo para las pruebas. Su trabajo es crear una base de 
# datos falsa, solo para las pruebas
engine_test = create_engine(                #Crea el motor de conexión a la base de datos de pruebas y guárdalo en engine_test.
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},   #permitiendo que la conexión se use desde distintos hilos..
    poolclass=StaticPool                          #y usa siempre la misma conexión
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
        #De todas las tablas que conoce Base, bórralas todas en la
        #  base de datos de pruebas.

# Fixture de cliente FastAPI con autenticación y BD simuladas
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():   #No conecta a la BD real, Define una función de reemplazo
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():                                #Define una función de reemplazo para get_current_user
        return db_session.query(models.Usuario).filter(models.Usuario.id == 1).first()    #devuelve directamente el usuario de prueba (el de id 1).

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()
