"""
Ponto de entrada da aplicação backend.

Este módulo inicializa a aplicação FastAPI, configura as tabelas no banco de dados
e registra o roteador de endpoints.

Responsabilidades:
    1. Criar as tabelas no PostgreSQL via SQLAlchemy (DDL automático) caso não existam.
    2. Instanciar a aplicação FastAPI com metadados do projeto.
    3. Registrar o router com todos os endpoints de Produto.

Execução:
    O servidor é iniciado via Uvicorn, conforme configurado no Dockerfile:
        uvicorn main:app --host 0.0.0.0 --port 8000

Documentação interativa da API (gerada automaticamente pelo FastAPI):
    Swagger UI: http://localhost:8000/docs
    ReDoc:      http://localhost:8000/redoc
"""

from fastapi import FastAPI
from database.database import engine, Base
from routers.router import router
import models.models  # Importação necessária para registrar os modelos no metadata do SQLAlchemy

# Cria automaticamente todas as tabelas mapeadas pelos modelos ORM, caso ainda não existam.
# Não sobrescreve tabelas existentes (equivalente a CREATE TABLE IF NOT EXISTS).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Produtos",
    description=(
        "API RESTful para gerenciamento de produtos. "
        "Permite operações de criação, leitura, atualização e remoção (CRUD) "
        "de produtos armazenados em um banco de dados PostgreSQL."
    ),
    version="1.0.0",
)

# Registra todas as rotas definidas em routers/router.py
app.include_router(router)
