"""
Módulo contendo os modelos de dados para o banco de dados PostgreSQL.
Este módulo define a estrutura das tabelas utilizando o SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class ProductModel(Base):
    """
    Modelo representativo da tabela 'produtos' no banco de dados.

    Atributos:
        id (int): Chave primária do produto.
        nome (str): Nome do produto.
        descricao (str): Descrição detalhada do produto.
        preco (float): Preço unitário do produto.
        categoria (str): Categoria à qual o produto pertence.
        email_fornecedor (str): E-mail de contato do fornecedor (padrão: "Email não informado").
        data_criacao (datetime): Timestamp de quando o registro foi criado (gerado automaticamente).
    """
    __tablename__ = "produtos"  

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String, index=True)
    preco = Column(Float, index=True)
    categoria = Column(String, index=True)
    email_fornecedor = Column(String, index=True, default="Email não informado")
    data_criacao = Column(DateTime(timezone=True), default=func.now(), index=True)