# Projeto CRUD com PostgreSQL e Streamlit

Este projeto é uma aplicação web desenvolvida com **Streamlit** que permite realizar operações de **CRUD** (Create, Read, Update, Delete) em um banco de dados **PostgreSQL**.

## 🚀 Funcionalidades

- **CRUD Completo**: Gerenciamento de registros no banco de dados.
- **Interface Moderna**: Dashboard interativo desenvolvido com Streamlit.
- **Conexão Segura**: Conexão com PostgreSQL utilizando variáveis de ambiente.

## 🛠️ Instalação

1. **Clone o repositório** (ou baixe os arquivos):
   ```bash
   git clone <url-do-repositorio>
   cd projeto_crud_postgres_streamlit
   ```

2. **Instale as dependências**:
   Este projeto utiliza o **Poetry** para gerenciamento de dependências.
   ```bash
   poetry install
   ```

3. **Ative o ambiente virtual**:
   ```bash
   poetry env activate
   ```

4. **Configure as variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do projeto com as seguintes credenciais do seu banco de dados:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=seu_banco
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   ```

## 🏃 Execução

Para iniciar a aplicação:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.
