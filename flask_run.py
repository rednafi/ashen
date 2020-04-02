from app import create_app
from dynaconf import settings

application = create_app()

# runs this only when the environment is 'development'
if settings.ENVIRONMENT == "development" and settings.GUNICORN is False:
    application.run(host="0.0.0.0", port=settings.FLASK_CONFIG.PORT, debug=True)
