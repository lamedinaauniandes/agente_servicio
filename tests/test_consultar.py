from fastapi.testclient import TestClient
from main import app

def test_consulta_responde_200():
    with TestClient(app) as client:
        response = client.post(
            "/consultar",
            json={"pregunta": "Cuanto es el tiempo de respuesta para incidencias criticas?"}
        )

    assert response.status_code == 200


def test_consulta_retorna_campos_esperados():
    with TestClient(app) as client:
        response = client.post(
            "/consultar",
            json={"pregunta": "¿cual es la penalización por cada hora de downtime no planificado?"}
        )

    body = response.json()

    assert "respuesta" in body
    assert "fuentes" in body
    assert "tiempo_ms" in body