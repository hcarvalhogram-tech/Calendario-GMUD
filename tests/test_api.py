"""
Testes básicos da API
"""
import pytest
from fastapi.testclient import TestClient
from app.database import SessionLocal, Base, engine
from main import app


@pytest.fixture(scope="function")
def test_db():
    """Cria banco de testes"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Cliente de testes"""
    return TestClient(app)


def test_health_check(client):
    """Testa health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root(client):
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "aplicacao" in response.json()


def test_listar_gmuds_vazio(client):
    """Testa listagem vazia de GMUDs"""
    response = client.get("/api/gmuds/")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_gmud(client):
    """Testa criação de GMUD"""
    payload = {
        "data": "2026-04-15",
        "equipamento": "Compressor A",
        "descricao": "Manutenção preventiva",
        "justificativa": "Manutenção regular",
        "risco": "BAIXO"
    }
    response = client.post("/api/gmuds/", json=payload)
    assert response.status_code == 201
    assert response.json()["equipamento"] == "Compressor A"


def test_criar_gmud_duplicada(client):
    """Testa prevenção de duplicação"""
    payload = {
        "data": "2026-04-15",
        "equipamento": "Compressor A",
        "descricao": "Manutenção preventiva",
        "justificativa": "Manutenção regular",
        "risco": "BAIXO"
    }
    
    # Criar primeira
    response1 = client.post("/api/gmuds/", json=payload)
    assert response1.status_code == 201
    
    # Tentar criar duplicada
    response2 = client.post("/api/gmuds/", json=payload)
    assert response2.status_code == 400


def test_dashboard(client):
    """Testa dashboard"""
    response = client.get("/api/gmuds/dashboard/resumo")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "taxa_conclusao" in response.json()
