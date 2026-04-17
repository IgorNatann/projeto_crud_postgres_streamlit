"""
Módulo de operações CRUD (Create, Read, Update, Delete).

Centraliza toda a lógica de acesso ao banco de dados para a entidade Produto.
As funções deste módulo recebem uma sessão de banco de dados (db) e realizam
operações diretamente sobre o model ProductModel via SQLAlchemy ORM.

Ao isolar o acesso ao banco neste módulo, as rotas (router.py) ficam limpas
e responsáveis apenas pelo tratamento de requisições HTTP, seguindo o princípio
de separação de responsabilidades.

Funções disponíveis:
    - get_product:    Busca um produto pelo ID.
    - get_products:   Lista todos os produtos.
    - create_product: Cria um novo produto.
    - delete_product: Remove um produto pelo ID.
    - update_product: Atualiza campos de um produto existente pelo ID.
"""

from sqlalchemy.orm import Session
from schema.schema import ProductUpdate, ProductCreate
from models.models import ProductModel


def get_product(db: Session, product_id: int) -> ProductModel | None:
    """
    Busca um único produto no banco de dados pelo seu ID.

    Args:
        db (Session): Sessão ativa do SQLAlchemy injetada via FastAPI Depends.
        product_id (int): ID do produto a ser buscado.

    Returns:
        ProductModel | None: O objeto do produto encontrado, ou None se não existir.

    Exemplo:
        produto = get_product(db, product_id=1)
        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_products(db: Session) -> list[ProductModel]:
    """
    Retorna todos os produtos cadastrados no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy injetada via FastAPI Depends.

    Returns:
        list[ProductModel]: Lista com todos os produtos. Retorna lista vazia
                            caso não haja nenhum produto cadastrado.
    """
    return db.query(ProductModel).all()


def create_product(db: Session, product: ProductCreate) -> ProductModel:
    """
    Insere um novo produto no banco de dados.

    Converte o schema Pydantic (ProductCreate) em um objeto ORM (ProductModel),
    persiste no banco e retorna o objeto atualizado com os campos gerados
    automaticamente (ex: id, data_criacao).

    Args:
        db (Session): Sessão ativa do SQLAlchemy injetada via FastAPI Depends.
        product (ProductCreate): Dados do produto validados pelo schema Pydantic.

    Returns:
        ProductModel: O produto recém-criado com todos os campos preenchidos,
                      incluindo id e data_criacao gerados pelo banco.
    """
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)  # Atualiza o objeto com os dados gerados pelo banco (ex: id, data_criacao)
    return db_product


def delete_product(db: Session, product_id: int) -> ProductModel | None:
    """
    Remove um produto do banco de dados pelo ID.

    Busca o produto, executa a exclusão e confirma a transação.
    Retorna o objeto deletado para que a rota possa confirmar ao cliente
    qual registro foi removido.

    Args:
        db (Session): Sessão ativa do SQLAlchemy injetada via FastAPI Depends.
        product_id (int): ID do produto a ser removido.

    Returns:
        ProductModel | None: O objeto do produto removido, ou None se não for encontrado.

    Atenção:
        A operação é permanente e irreversível. Não há soft delete implementado.
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None

    db.delete(db_product)
    db.commit()
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate) -> ProductModel | None:
    """
    Atualiza parcialmente os campos de um produto existente.

    Implementa atualização parcial (PATCH-like sobre PUT): apenas os campos
    enviados com valor não nulo são atualizados. Campos omitidos ou enviados
    como None preservam seus valores atuais no banco de dados.

    Args:
        db (Session): Sessão ativa do SQLAlchemy injetada via FastAPI Depends.
        product_id (int): ID do produto a ser atualizado.
        product (ProductUpdate): Schema com os campos a serem atualizados.
                                  Todos os campos são opcionais.

    Returns:
        ProductModel | None: O produto atualizado, ou None se o ID não for encontrado.

    Exemplo:
        # Atualiza apenas o preço do produto de ID 5
        update_product(db, product_id=5, product=ProductUpdate(price=299.90))
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None

    # Atualiza apenas os campos que foram explicitamente fornecidos na requisição
    if product.name is not None:
        db_product.nome = product.name
    if product.description is not None:
        db_product.descricao = product.description
    if product.price is not None:
        db_product.preco = product.price
    if product.categoria is not None:
        db_product.categoria = product.categoria
    if product.email_fornecedor is not None:
        db_product.email_fornecedor = product.email_fornecedor

    db.commit()
    db.refresh(db_product)
    return db_product