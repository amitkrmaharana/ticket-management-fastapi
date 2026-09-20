from fastapi import FastAPI
from src.utils.db import Base, engine
from src.user.router import user_routes
# from contextlib import asynccontextmanager

# Alternative method commented out for on_event is lifespan
# As on_event is deprecated can be replaced by lifespan in a diffrent way

# app = FastAPI(lifespan=lifespan) 
app = FastAPI()
app.include_router(user_routes)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
    # Base.metadata.create_all(engine)
    # print("Application Started")
    
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(engine)
    print("Application Started")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application stopped")