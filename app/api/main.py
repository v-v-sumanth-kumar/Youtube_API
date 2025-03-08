from fastapi import FastAPI
from api.routes import router
from models.database import Base,engine


app = FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(router)
