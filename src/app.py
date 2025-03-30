from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from api.trons import router as tron_router
from core.settings import get_settings
from db.connector import DatabaseConnector
from clients.tron_account import TronAccount
import controller.tron_control as tron_modul

logger = logging.getLogger(__name__)
config =get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Launching the application.")
    db = DatabaseConnector(config.DB.asyncpg_url)
    tron = TronAccount()
    tron_modul.tron_controller = tron_modul.TronController(db=db, tron=tron)
    yield
    logger.info("application shutdown")
    await db.disconnect()


app = FastAPI(lifespan=lifespan, title='FastAPI')
app.include_router(tron_router, tags=['tron'], prefix='/tron')



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="core/logging.yaml")
