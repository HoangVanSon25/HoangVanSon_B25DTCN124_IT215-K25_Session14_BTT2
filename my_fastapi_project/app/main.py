from fastapi import FastAPI
from routers.student import router
from database import Base, enginne
Base.metadata.create_all(bind=enginne)
app = FastAPI()
app.include_router(router)
