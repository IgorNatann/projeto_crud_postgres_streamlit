# 🛒 Sistema de Gerenciamento de Produtos

Projeto de portfólio full-stack que demonstra a construção de uma **API RESTful** completa integrada a uma **interface web interativa**, utilizando as melhores práticas de desenvolvimento com Python moderno e containerização com Docker.

---

## 📸 Visão Geral

O sistema permite gerenciar um catálogo de produtos via interface web, com operações completas de **CRUD** (Create, Read, Update, Delete) persistidas em um banco de dados **PostgreSQL**.

```
┌─────────────────┐     HTTP/REST     ┌──────────────────┐     SQLAlchemy    ┌────────────────┐
│   Frontend      │ ◄───────────────► │    Backend       │ ◄───────────────► │   PostgreSQL   │
│   Streamlit     │   porta 8501      │    FastAPI       │    porta 5432      │   (port 5432)  │
│   port 8501     │                   │    port 8000     │                    │                │
└─────────────────┘                   └──────────────────┘                   └────────────────┘
         │                                     │                                      │
         └─────────────────────────────────────┴──────────────────────────────────────┘
                                   Docker Compose Network
```

---

## 🧱 Estrutura do Projeto

```
projeto_crud_postgres_streamlit/
│
├── backend/                        # API REST (FastAPI)
│   ├── main.py                     # Ponto de entrada: inicializa app e tabelas
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py             # Engine, sessão e Base ORM
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py               # Modelos ORM (tabelas do banco)
│   ├── schema/
│   │   ├── __init__.py
│   │   └── schema.py               # Schemas Pydantic (validação e serialização)
│   ├── crud/
│   │   ├── __init__.py
│   │   └── crud.py                 # Camada de acesso ao banco (lógica CRUD)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── router.py               # Endpoints da API REST
│   ├── Dockerfile                  # Imagem Docker do backend
│   └── requirements.txt            # Dependências Python do backend
│
├── frontend/                       # Interface web (Streamlit)
│   ├── app.py                      # Aplicação Streamlit (interface CRUD)
│   ├── logo.png                    # Logotipo exibido na interface
│   ├── .streamlit/
│   │   └── config.toml             # Tema visual da interface Streamlit
│   ├── Dockerfile                  # Imagem Docker do frontend
│   └── requirements.txt            # Dependências Python do frontend
│
├── docker-compose.yaml             # Orquestração dos 3 serviços (postgres, backend, frontend)
├── pyproject.toml                  # Configuração do projeto com Poetry
└── README.md
```

---

## 🚀 Tecnologias Utilizadas

| Camada        | Tecnologia         | Versão  | Função                                      |
|---------------|--------------------|---------|---------------------------------------------|
| **Frontend**  | Streamlit          | Latest  | Interface web interativa                    |
| **Frontend**  | Requests           | Latest  | Cliente HTTP para consumir a API            |
| **Frontend**  | Pandas             | Latest  | Manipulação e exibição de dados tabulares   |
| **Backend**   | FastAPI            | ^0.136  | Framework para construção da API REST       |
| **Backend**   | SQLAlchemy         | Latest  | ORM para acesso ao banco de dados           |
| **Backend**   | Pydantic v2        | ^2.13   | Validação e serialização de dados           |
| **Backend**   | Uvicorn            | Latest  | Servidor ASGI de alto desempenho            |
| **Banco**     | PostgreSQL         | 16      | Banco de dados relacional                   |
| **Infra**     | Docker             | Latest  | Containerização dos serviços                |
| **Infra**     | Docker Compose     | Latest  | Orquestração multi-container                |
| **Dev**       | Poetry             | Latest  | Gerenciamento de dependências Python        |

---

## 📋 Endpoints da API

| Método     | Rota                    | Descrição                               | Status de Sucesso |
|------------|-------------------------|-----------------------------------------|-------------------|
| `POST`     | `/products/`            | Criar um novo produto                   | `201 Created`     |
| `GET`      | `/products/`            | Listar todos os produtos                | `200 OK`          |
| `GET`      | `/products/{id}`        | Buscar produto por ID                   | `200 OK`          |
| `PUT`      | `/products/{id}`        | Atualizar produto por ID (parcial)      | `200 OK`          |
| `DELETE`   | `/products/{id}`        | Remover produto por ID                  | `200 OK`          |

### Categorias válidas de produto

| Categoria         |
|-------------------|
| Eletrônico        |
| Eletrodoméstico   |
| Móveis            |
| Roupas            |
| Calçados          |

---

## 🐳 Como Executar com Docker (recomendado)

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução

### Passos

**1. Clone o repositório:**
```bash
git clone https://github.com/IgorNatann/projeto_crud_postgres_streamlit.git
cd projeto_crud_postgres_streamlit
```

**2. Suba todos os serviços:**
```bash
docker compose up --build
```

**3. Acesse a aplicação:**

| Serviço                       | URL                                      |
|-------------------------------|------------------------------------------|
| Interface Web (Streamlit)     | http://localhost:8501                    |
| Documentação da API (Swagger) | http://localhost:8000/docs               |
| Documentação da API (ReDoc)   | http://localhost:8000/redoc              |

> **Nota:** Na primeira execução, o Docker fará o download das imagens base (~1GB). As execuções seguintes serão mais rápidas pois as camadas ficam em cache.

### Parar os serviços
```bash
docker compose down
```

### Parar e remover volumes (limpar banco de dados)
```bash
docker compose down -v
```

---

## 🗂️ Decisões Técnicas e Boas Práticas

### Arquitetura em Camadas (Backend)
O backend segue uma arquitetura em camadas com responsabilidades bem definidas:

```
Requisição HTTP
      ↓
  router.py        ← Recebe e roteia requisições HTTP, define status codes
      ↓
   crud.py         ← Executa operações no banco via SQLAlchemy
      ↓
  models.py        ← Define a estrutura das tabelas (ORM)
      ↓
 database.py       ← Gerencia conexão, sessão e Base ORM
      ↓
  PostgreSQL
```

### Principais decisões e práticas adotadas

| Prática                          | Implementação                                                                 |
|----------------------------------|-------------------------------------------------------------------------------|
| Separação de responsabilidades   | Camadas independentes: models, schemas, crud, routers                         |
| Injeção de dependência           | Sessão do banco via `Depends(get_db)` em cada endpoint                        |
| Validação automática             | Pydantic valida todos os dados de entrada antes de qualquer operação no banco |
| Atualização parcial              | Endpoint `PUT` só atualiza os campos enviados, preservando os demais          |
| Healthcheck no Docker            | Backend aguarda o Postgres estar `healthy` antes de iniciar                   |
| Documentação automática          | FastAPI gera Swagger e ReDoc automaticamente a partir dos schemas              |
| Criação automática de tabelas    | `Base.metadata.create_all()` garante que as tabelas existam ao iniciar        |
| Segurança de conexão             | Credenciais do banco via variável de ambiente (`DATABASE_URL`)                |

---

## 👤 Autor

**Igor Natann**
- GitHub: [@IgorNatann](https://github.com/IgorNatann)
- E-mail: Igornatan4@gmail.com
