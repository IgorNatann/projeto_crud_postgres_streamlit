"""
Módulo de schemas Pydantic para validação e serialização de dados.

Os schemas (esquemas) são contratos de dados que definem:
    - Quais campos são aceitos nas requisições (entrada).
    - Quais campos são retornados nas respostas (saída).
    - As regras de validação aplicadas a cada campo.

Utiliza a biblioteca Pydantic v2 para validação automática dos dados
recebidos via API, retornando erros descritivos caso a entrada seja inválida.

Schemas definidos:
    - CategoriaBase: Enum com as categorias de produto permitidas.
    - ProductBase:   Campos comuns a criação e atualização de produtos.
    - ProductCreate: Schema para criação de um novo produto (POST).
    - ProductUpdate: Schema para atualização parcial de produto (PUT). Todos os campos são opcionais.
    - ProductResponse: Schema de resposta da API, inclui campos gerados pelo banco (GET).
"""

from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional


class CategoriaBase(Enum):
    """
    Enumeração das categorias de produto aceitas pelo sistema.

    Garante que apenas valores pré-definidos sejam aceitos no campo 'categoria',
    evitando inconsistências nos dados armazenados.

    Valores aceitos:
        - "Eletrônico"
        - "Eletrodoméstico"
        - "Móveis"
        - "Roupas"
        - "Calçados"
    """
    categoria1 = "Eletrônico"
    categoria2 = "Eletrodoméstico"
    categoria3 = "Móveis"
    categoria4 = "Roupas"
    categoria5 = "Calçados"


class ProductBase(BaseModel):
    """
    Schema base compartilhado entre criação e atualização de produtos.

    Contém os campos obrigatórios e as regras de validação aplicadas
    em todas as operações que envolvem dados de produto.

    Atributos:
        name (str): Nome do produto. Campo obrigatório.
        description (str | None): Descrição do produto. Opcional.
        price (PositiveFloat): Preço do produto. Deve ser um número positivo maior que zero.
        categoria (str): Categoria do produto. Validada contra o Enum CategoriaBase.
        email_fornecedor (EmailStr): E-mail do fornecedor. Validado automaticamente pelo Pydantic.
    """
    name: str
    description: Optional[str] = None
    price: PositiveFloat
    categoria: str
    email_fornecedor: EmailStr

    @validator("categoria")
    def check_categoria(cls, v):
        """
        Valida se a categoria informada existe na lista de categorias permitidas.

        Args:
            v (str): Valor da categoria informado na requisição.

        Returns:
            str: O valor da categoria, caso seja válido.

        Raises:
            ValueError: Se a categoria não corresponder a nenhum valor do Enum CategoriaBase.
        """
        if v in [item.value for item in CategoriaBase]:
            return v
        raise ValueError(
            f"Categoria inválida. Valores aceitos: {[item.value for item in CategoriaBase]}"
        )


class ProductCreate(ProductBase):
    """
    Schema para criação de um novo produto via requisição POST.

    Herda todos os campos e validações de ProductBase sem alterações adicionais.
    Implementado como classe separada para facilitar futuras extensões
    específicas ao processo de criação.

    Exemplo de payload JSON:
        {
            "name": "Notebook Gamer",
            "description": "Processador i9, 32GB RAM, SSD 1TB",
            "price": 8999.90,
            "categoria": "Eletrônico",
            "email_fornecedor": "fornecedor@techshop.com"
        }
    """
    pass


class ProductResponse(ProductBase):
    """
    Schema de resposta retornado pela API após operações de leitura ou criação.

    Estende ProductBase com campos adicionais gerados automaticamente pelo banco de dados:

    Atributos adicionais:
        id (int): Identificador único do produto no banco de dados.
        created_at (datetime): Data e hora de criação do registro (com timezone).

    Configuração ORM:
        from_attributes = True — permite que o Pydantic leia dados diretamente
        de objetos SQLAlchemy, sem necessidade de conversão manual.
    """
    id: int
    created_at: datetime

    class Config:
        """Habilita compatibilidade com objetos ORM do SQLAlchemy."""
        from_attributes = True


class ProductUpdate(BaseModel):
    """
    Schema para atualização parcial de um produto existente via requisição PUT.

    Todos os campos são opcionais (Optional), permitindo atualizações parciais —
    o cliente pode enviar apenas os campos que deseja modificar.
    Campos não enviados preservam o valor atual no banco de dados.

    Atributos:
        name (str | None): Novo nome do produto. Opcional.
        description (str | None): Nova descrição. Opcional.
        price (PositiveFloat | None): Novo preço. Deve ser positivo se informado.
        categoria (str | None): Nova categoria. Validada se informada.
        email_fornecedor (EmailStr | None): Novo e-mail do fornecedor. Validado se informado.

    Exemplo de payload JSON para atualizar apenas o preço:
        {
            "price": 7500.00
        }
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    categoria: Optional[str] = None
    email_fornecedor: Optional[EmailStr] = None

    @validator("categoria", pre=True, always=True)
    def check_categoria(cls, v):
        """
        Valida a categoria durante uma atualização, permitindo valor nulo.

        Se o campo não for enviado (None), nenhuma validação é aplicada e
        o valor atual do banco é preservado. Se enviado, deve ser uma
        categoria válida conforme CategoriaBase.

        Args:
            v (str | None): Valor da categoria informado na requisição.

        Returns:
            str | None: O valor da categoria se válido, ou None se não informado.

        Raises:
            ValueError: Se a categoria for informada mas não for válida.
        """
        if v is None:
            return v
        if v in [item.value for item in CategoriaBase]:
            return v
        raise ValueError(
            f"Categoria inválida. Valores aceitos: {[item.value for item in CategoriaBase]}"
        )
