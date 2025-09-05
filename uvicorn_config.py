import multiprocessing
import uvicorn
from config.env_config import settings

ENV = settings.ENVIRONMENT.lower()
if ENV == "development":
    reload = True
    log_level = "info"
    workers = 1
elif ENV == "staging":
    reload = True
    log_level = "warning"
    workers = 1
elif ENV == "production":
    reload = False
    log_level = "warning"
    workers = 1 # we can increase the workers in future
else:
    raise ValueError(f"Unknown ENVIRONMENT: {ENV}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # FastAPI app import
        host=settings.HOST,
        port=settings.PORT,
        reload=reload,
        workers=workers,
        log_level=log_level,
    )
