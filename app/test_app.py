from app import app

client = app.test_client()


def test_nombre_valido():
    r = client.get("/hello?name=Alvaro")
    assert r.status_code == 200
    assert b"Hello, Alvaro!" in r.data


def test_xss_rechazado():
    r = client.get("/hello?name=<script>alert(1)</script>")
    assert r.status_code == 400


def test_cabeceras_seguridad():
    r = client.get("/hello?name=Ana")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in r.headers