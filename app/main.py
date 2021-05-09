from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.postgre_connector import PostgreSqlConnector
from .events import startup
from .routers import index

app = FastAPI(title='EzInventory API')

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
# @app.exception_handler()
# async def auth_unauthorized_exception_handler(request, exc):
#     Your exception handeling logic here

# Event handlers


@app.on_event("startup")
async def startup_event():
    startup.init_database_session(PostgreSqlConnector)

# Routers
app.include_router(
    index.router,
    tags=["index"],
    # responses={},
)
