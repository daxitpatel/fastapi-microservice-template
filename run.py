import newrelic.agent
import os
import uvicorn


if os.environ.get("IS_NEW_RELIC_ENABLED", False) and os.path.exists(os.path.abspath(os.path.join(__file__, '..', 'app', 'newrelic.ini'))):
    newrelic.agent.initialize(os.path.abspath(os.path.join(__file__, '..', 'app', 'newrelic.ini')))

from app import app

if __name__ == "__main__":
    try:

        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=app.config.PORT,
            reload=app.config.DEBUG,
            log_level=app.config.LOG_LEVEL.lower()
        )

    except Exception as e:
        print(f"Server exit with error: {e}")
