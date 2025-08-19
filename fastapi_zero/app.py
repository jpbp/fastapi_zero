from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi_zero.routers import auth, users, todos
from fastapi_zero.schemas import (
    Message,
)

app = FastAPI(title='Minha Api Bala!')

# Configuração CORS para permitir o frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/html/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root_html():
    return """
    <html>
        <head>
            <title> Nosso olá mundo! </title>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
    </html>"""


# implementar um health check...
