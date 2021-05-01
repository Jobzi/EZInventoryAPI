from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import index

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler()
# async def auth_unauthorized_exception_handler(request, exc):
#     Your exception handeling logic here


app.include_router(
    index.router,
    tags=["index"],
    # responses={},
)
