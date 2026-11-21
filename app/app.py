from flask import Flask, request
import re
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
# Solo letras y espacios, entre 1 y 50 caracteres
NAME_RE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{1,50}$")


@app.after_request
def security_headers(resp):
    # Cabeceras que ZAP marcó como ausentes
    resp.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Server"] = "secdev"  # no revelar versiones
    return resp


@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    # Validación de entrada
    if not NAME_RE.fullmatch(name):
        return "Nombre invalido", 400
    # Escape de salida (anti-XSS)
    return f"Hello, {escape(name)}!"


if __name__ == '__main__':
    # Sin debug; en el contenedor corre con gunicorn
    app.run()