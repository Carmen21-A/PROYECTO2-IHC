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
