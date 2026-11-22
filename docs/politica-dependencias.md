# Política de gestión de dependencias

## Alcance
Dependencias Python de la aplicación (`app/requirements.txt`) e imagen base
del contenedor (`app/Dockerfile`).

## Herramientas
- **pip-audit y Trivy** (en el pipeline de Jenkins): detectan vulnerabilidades
  conocidas en cada ejecución.
- **Dependabot** (GitHub): revisa semanalmente las versiones y propone
  actualizaciones mediante Pull Requests.
- **Versiones fijas** en `requirements.txt` (`Flask==3.1.3`, etc.) para
  garantizar builds reproducibles.

## Plazos de parcheo
| Severidad | Plazo máximo |
|---|---|
| Crítica | 24 a 48 horas |
| Alta | 7 días |
| Media | 30 días |
| Baja | Siguiente ciclo de mantenimiento |

## Procedimiento de actualización segura
1. Dependabot (o una alerta del pipeline) detecta una versión vulnerable.
2. Se revisa el aviso y la versión corregida indicada.
3. Se actualiza en una rama o Pull Request, sin forzar cambios mayores sin revisión.
4. El pipeline ejecuta pruebas, pip-audit, Trivy y ZAP sobre la nueva versión.
5. Si todo pasa, se fusiona; si falla, se corrige o se descarta la actualización.

## Cuando no existe parche
- Mitigar (por ejemplo, restringir el uso de la función afectada).
- Aceptar el riesgo con justificación escrita y fecha de revisión.
- Reemplazar la librería por una alternativa mantenida.

## Evidencia en este proyecto
- Antes: Flask 2.2.2 y Werkzeug 2.2.2 con 3 CVE de severidad alta (Trivy) y
  múltiples avisos (pip-audit).
- Después: actualización a Flask 3.1.3 y Werkzeug 3.1.9, sin vulnerabilidades
  reportadas por pip-audit ni Trivy.