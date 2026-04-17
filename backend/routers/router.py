"""
Módulo de rotas da API REST para o recurso Produto.

Define os endpoints HTTP que expõem as operações CRUD do sistema.
Utiliza o APIRouter do FastAPI para organizar as rotas em um módulo
separado, que é registrado na aplicação principal (main.py).

Todas as rotas seguem o padrão RESTful:
    POST   /products/           → Criar produto
    GET    /products/           → Listar todos os produtos
    GET    /products/{id}       → Buscar produto por ID
    DELETE /products/{id}       → Remover produto por ID
    PUT    /products/{id}       → Atualizar produto por ID

Validação e serialização de dados são feitas automaticamente pelos schemas
Pydantic (ProductCreate, ProductUpdate, ProductResponse).
O acesso ao banco de dados é gerenciado pela função get_db via Depends.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schema.schema import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud.crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product,
)

router = APIRouter()


@router.post("/products/", response_model=ProductResponse, status_code=201)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto no banco de dados.

    Recebe os dados do produto no corpo da requisição, valida via schema
    ProductCreate e persiste no banco via camada CRUD.

    Args:
        product (ProductCreate): Dados do produto a ser criado, validados pelo Pydantic.
        db (Session): Sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        ProductResponse: O produto criado com campos gerados pelo banco (id, created_at).

    HTTP Status:
        201 Created — Produto criado com sucesso.
        422 Unprocessable Entity — Dados inválidos (ex: categoria inexistente, e-mail inválido).
    """
    return create_product(db=db, product=product)


@router.get("/products/", response_model=List[ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    """
    Retorna a lista completa de produtos cadastrados.

    Args:
        db (Session): Sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        List[ProductResponse]: Lista com todos os produtos. Retorna lista vazia
                               caso não haja produtos cadastrados.

    HTTP Status:
        200 OK — Lista retornada com sucesso (mesmo que vazia).
    """
    products = get_products(db)
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados de um produto específico pelo seu ID.

    Args:
        product_id (int): ID do produto a ser buscado, extraído da URL.
        db (Session): Sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        ProductResponse: Dados completos do produto encontrado.

    Raises:
        HTTPException 404: Se nenhum produto com o ID informado for encontrado.

    HTTP Status:
        200 OK  — Produto encontrado e retornado.
        404 Not Found — Produto não encontrado para o ID informado.
    """
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product


@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    """
    Remove um produto do banco de dados pelo seu ID.

    Busca o produto pelo ID e, se encontrado, realiza a exclusão permanente.
    Retorna os dados do produto removido para confirmação ao cliente.

    Args:
        product_id (int): ID do produto a ser removido, extraído da URL.
        db (Session): Sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        ProductResponse: Dados do produto que foi removido.

    Raises:
        HTTPException 404: Se nenhum produto com o ID informado for encontrado.

    HTTP Status:
        200 OK  — Produto removido com sucesso.
        404 Not Found — Produto não encontrado para o ID informado.

    Atenção:
        A operação é permanente e irreversível.
    """
    db_product = delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza parcialmente os dados de um produto existente pelo seu ID.

    Apenas os campos enviados com valor não nulo serão atualizados.
    Campos omitidos preservam seus valores atuais no banco de dados.

    Args:
        product_id (int): ID do produto a ser atualizado, extraído da URL.
        product (ProductUpdate): Campos a serem atualizados. Todos são opcionais.
        db (Session): Sessão do banco de dados injetada automaticamente pelo FastAPI.

    Returns:
        ProductResponse: Dados completos do produto após a atualização.

    Raises:
        HTTPException 404: Se nenhum produto com o ID informado for encontrado.

    HTTP Status:
        200 OK  — Produto atualizado com sucesso.
        404 Not Found — Produto não encontrado para o ID informado.
        422 Unprocessable Entity — Dados inválidos no corpo da requisição.
    """
    db_product = update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product