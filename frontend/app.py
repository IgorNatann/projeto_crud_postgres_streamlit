"""
Interface frontend do sistema de Gerenciamento de Produtos.

Este módulo implementa a aplicação Streamlit que consome a API REST do backend
(FastAPI) e fornece uma interface web interativa para as operações CRUD de produtos.

Seções da interface:
    1. Adicionar Produto   — Formulário para cadastrar um novo produto via POST.
    2. Visualizar Produtos — Lista todos os produtos registrados via GET.
    3. Buscar Produto      — Exibe detalhes de um produto por ID via GET.
    4. Deletar Produto     — Remove um produto por ID via DELETE.
    5. Atualizar Produto   — Formulário de atualização parcial por ID via PUT.

Dependências:
    - streamlit:  Framework para construção da interface web.
    - requests:   Biblioteca HTTP para consumir a API REST do backend.
    - pandas:     Manipulação e exibição tabular dos dados retornados pela API.

Configuração de tema:
    O tema visual é definido em .streamlit/config.toml, seguindo a identidade
    visual do projeto.

Comunicação com o backend:
    Todas as requisições são feitas para o serviço 'backend' na porta 8000,
    hostname resolvido automaticamente pela rede interna do Docker Compose:
        http://backend:8000/products/
"""

import streamlit as st
import requests
import pandas as pd

# ─────────────────────────────────────────────
# Configuração geral da página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gerenciamento de Produtos",
    layout="wide",
)

st.image("logo.png", width=200)
st.title("Gerenciamento de Produtos")


# ─────────────────────────────────────────────
# Funções auxiliares
# ─────────────────────────────────────────────

def show_response_message(response: requests.Response) -> None:
    """
    Exibe uma mensagem de feedback na interface com base no status HTTP da resposta.

    Interpreta a resposta da API REST e exibe:
        - Mensagem de sucesso verde para status 200.
        - Mensagem de erro vermelha com detalhes para qualquer outro status,
          extraindo a chave 'detail' do corpo JSON da resposta quando disponível.

    Args:
        response (requests.Response): Objeto de resposta retornado pela biblioteca requests
                                       após uma chamada à API do backend.

    Comportamento para erros:
        - Se 'detail' for uma lista (erros de validação Pydantic), exibe cada mensagem.
        - Se 'detail' for uma string, exibe diretamente.
        - Se a resposta não puder ser decodificada como JSON, exibe erro genérico.
    """
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                # Erros de validação Pydantic retornam 'detail' como lista de objetos
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Erro: {errors}")
                else:
                    # Erros simples retornam 'detail' como string
                    st.error(f"Erro: {data['detail']}")
        except ValueError:
            st.error("Erro desconhecido. Não foi possível decodificar a resposta.")


def format_product_dataframe(data: list | dict) -> pd.DataFrame:
    """
    Converte os dados de produto(s) retornados pela API em um DataFrame formatado.

    Garante que as colunas sejam exibidas sempre na mesma ordem,
    independente da ordem retornada pelo JSON da API.

    Args:
        data (list | dict): Um produto (dict) ou lista de produtos (list of dicts)
                             retornados pela API.

    Returns:
        pd.DataFrame: DataFrame com as colunas na ordem definida para exibição.
    """
    # Normaliza entrada para sempre ser uma lista
    if isinstance(data, dict):
        data = [data]

    df = pd.DataFrame(data)
    colunas_ordenadas = [
        "id",
        "name",
        "description",
        "price",
        "categoria",
        "email_fornecedor",
        "created_at",
    ]
    return df[colunas_ordenadas]


# ─────────────────────────────────────────────
# Seção 1: Adicionar Produto
# ─────────────────────────────────────────────

with st.expander("➕ Adicionar um Novo Produto"):
    """
    Formulário para cadastrar um novo produto no sistema.
    Envia uma requisição POST para a API com os dados preenchidos.
    """
    with st.form("new_product"):
        name = st.text_input("Nome do Produto")
        description = st.text_area("Descrição do Produto")
        price = st.number_input("Preço", min_value=0.01, format="%f")
        categoria = st.selectbox(
            "Categoria",
            ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
        )
        email_fornecedor = st.text_input("Email do Fornecedor")
        submit_button = st.form_submit_button("Adicionar Produto")

        if submit_button:
            # Envia os dados para a API via POST e exibe o resultado
            response = requests.post(
                "http://backend:8000/products/",
                json={
                    "name": name,
                    "description": description,
                    "price": price,
                    "categoria": categoria,
                    "email_fornecedor": email_fornecedor,
                },
            )
            show_response_message(response)

# ─────────────────────────────────────────────
# Seção 2: Visualizar Todos os Produtos
# ─────────────────────────────────────────────

with st.expander("📋 Visualizar Produtos"):
    """
    Lista todos os produtos cadastrados no banco de dados em formato de tabela.
    Envia uma requisição GET para a API e exibe o resultado como HTML sem índice.
    """
    if st.button("Exibir Todos os Produtos"):
        response = requests.get("http://backend:8000/products/")
        if response.status_code == 200:
            df = format_product_dataframe(response.json())
            # Renderiza a tabela sem a coluna de índice do pandas
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# ─────────────────────────────────────────────
# Seção 3: Buscar Produto por ID
# ─────────────────────────────────────────────

with st.expander("🔍 Obter Detalhes de um Produto"):
    """
    Busca e exibe os detalhes de um produto específico pelo seu ID.
    Envia uma requisição GET para /products/{id}.
    """
    get_id = st.number_input("ID do Produto", min_value=1, format="%d")
    if st.button("Buscar Produto"):
        response = requests.get(f"http://backend:8000/products/{get_id}")
        if response.status_code == 200:
            df = format_product_dataframe(response.json())
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# ─────────────────────────────────────────────
# Seção 4: Deletar Produto
# ─────────────────────────────────────────────

with st.expander("🗑️ Deletar Produto"):
    """
    Remove permanentemente um produto do banco de dados pelo seu ID.
    Envia uma requisição DELETE para /products/{id}.
    Atenção: operação irreversível.
    """
    delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
    if st.button("Deletar Produto"):
        response = requests.delete(f"http://backend:8000/products/{delete_id}")
        show_response_message(response)

# ─────────────────────────────────────────────
# Seção 5: Atualizar Produto
# ─────────────────────────────────────────────

with st.expander("✏️ Atualizar Produto"):
    """
    Formulário para atualização parcial de um produto existente.
    Apenas os campos preenchidos são enviados à API via PUT.
    Campos deixados em branco preservam seus valores atuais no banco.
    """
    with st.form("update_product"):
        update_id = st.number_input("ID do Produto", min_value=1, format="%d")
        new_name = st.text_input("Novo Nome do Produto")
        new_description = st.text_area("Nova Descrição do Produto")
        new_price = st.number_input("Novo Preço", min_value=0.01, format="%f")
        new_categoria = st.selectbox(
            "Nova Categoria",
            ["Eletrônico", "Eletrodoméstico", "Móveis", "Roupas", "Calçados"],
        )
        new_email = st.text_input("Novo Email do Fornecedor")
        update_button = st.form_submit_button("Atualizar Produto")

        if update_button:
            # Monta o payload apenas com os campos que foram explicitamente preenchidos
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_price > 0:
                update_data["price"] = new_price
            if new_email:
                update_data["email_fornecedor"] = new_email
            if new_categoria:
                update_data["categoria"] = new_categoria

            if update_data:
                # Envia apenas os campos alterados para a API via PUT
                response = requests.put(
                    f"http://backend:8000/products/{update_id}",
                    json=update_data,
                )
                show_response_message(response)
            else:
                st.error("Nenhuma informação fornecida para atualização")