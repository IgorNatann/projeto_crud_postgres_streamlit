"""
Módulo de modelos ORM (Object-Relational Mapping).

Define as classes que representam as tabelas do banco de dados PostgreSQL
utilizando o SQLAlchemy ORM. Cada classe corresponde a uma tabela e cada
atributo corresponde a uma coluna.

Tabelas mapeadas:
    - produtos: armazena os dados dos produtos cadastrados no sistema.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base


class ProductModel(Base):
    """
    Modelo ORM que representa a tabela 'produtos' no banco de dados PostgreSQL.

    Esta classe é utilizada pelo SQLAlchemy para mapear objetos Python
    diretamente a registros no banco de dados, eliminando a necessidade
    de escrever SQL manualmente nas operações CRUD.

    Atributos:
        id (int): Chave primária com auto incremento. Gerada automaticamente pelo banco.
        nome (str): Nome do produto. Indexado para buscas rápidas.
        descricao (str): Descrição detalhada do produto. Indexado para buscas rápidas.
        preco (float): Preço unitário do produto. Deve ser um valor positivo.
        categoria (str): Categoria à qual o produto pertence (ex: Eletrônico, Móveis).
        email_fornecedor (str): E-mail de contato do fornecedor do produto.
        data_criacao (datetime): Timestamp de criação do registro, gerado automaticamente
                                  pelo banco de dados no momento da inserção.

    Tabela no banco:
        __tablename__ = "produtos"

    Exemplo de uso:
        produto = ProductModel(
            nome="Notebook",
            descricao="Notebook i7 16GB RAM",
            preco=4500.00,
            categoria="Eletrônico",
            email_fornecedor="fornecedor@email.com"
        )
        db.add(produto)
        db.commit()
    """

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    preco = Column(Float, index=True)
    categoria = Column(String, index=True)
    email_fornecedor = Column(String, index=True, default="Email não informado")
    data_criacao = Column(DateTime(timezone=True), default=func.now(), index=True)