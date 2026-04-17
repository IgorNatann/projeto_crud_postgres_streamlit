"""
Módulo de configuração do banco de dados.

Responsabilidades:
    - Criar e configurar o engine de conexão com o PostgreSQL via SQLAlchemy.
    - Definir a classe Base do ORM, da qual todos os modelos herdam.
    - Prover a sessão de banco de dados (SessionLocal) para uso nas rotas via injeção de dependência.

Variáveis de ambiente utilizadas:
    DATABASE_URL: URL completa de conexão com o banco de dados no formato
                  postgresql://usuario:senha@host:porta/banco
                  Valor padrão (desenvolvimento local): postgresql://user_crud:password_crud@localhost:5432/database_crud
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexão lida da variável de ambiente ou valor padrão para desenvolvimento local
POSTGRES_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user_crud:password_crud@localhost:5432/database_crud"
)

# Engine principal: gerencia o pool de conexões com o PostgreSQL
engine = create_engine(POSTGRES_DATABASE_URL)

# Fábrica de sessões: cada request recebe sua própria sessão isolada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para todos os modelos ORM do projeto
Base = declarative_base()


def get_db():
    """
    Gerador de sessão de banco de dados para injeção de dependência no FastAPI.

    Abre uma sessão ao início de cada request e garante seu fechamento ao final,
    mesmo em caso de erro, evitando vazamentos de conexão.

    Yields:
        Session: Sessão ativa do SQLAlchemy para interação com o banco de dados.

    Exemplo de uso em uma rota FastAPI:
        @router.get("/items/")
        def list_items(db: Session = Depends(get_db)):
            return db.query(ItemModel).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()