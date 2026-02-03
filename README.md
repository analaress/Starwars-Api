
---

# Star Wars API

Este projeto é uma API desenvolvida com **FastAPI** que funciona como um intermediário inteligente para a [SWAPI (Star Wars API)](https://swapi.dev/). O objetivo é facilitar o acesso aos dados da saga, adicionando camadas de segurança, organização e performance.

## Arquitetura e Decisões

A estrutura do projeto foi separada em camadas para garantir que o código seja limpo e fácil de manter:

* **Routers (API)**: Gerencia as rotas e a entrada de dados.
* **Services**: Contém a lógica de negócio (cálculos de datas, agrupamentos e filtros).
* **Clients**: Módulo dedicado à comunicação assíncrona com a API externa.
* **Core & Security**: Centraliza as configurações, segurança com JWT e criptografia de senhas.

### Proposta de Desenho para Nuvem (GCP)

A arquitetura foi pensada para ser *cloud-ready*. Em um ambiente Google Cloud, o fluxo seria:
`Usuário` → `Cloud API Gateway` → `Cloud Run / Functions` (Onde roda este código) → `External SWAPI`.

---

## Tecnologias Principais

* **FastAPI**: Alta performance e documentação automática com Swagger.
* **JWT & Argon2**: Autenticação segura e hash de senhas de última geração.
* **TTLCache**: Estratégia de cache em memória para evitar gargalos na API externa.
* **PostgreSQL + SQLAlchemy**: Para persistência de usuários e senhas.
* **Httpx**: Cliente HTTP assíncrono para requisições não bloqueantes.

---

## O que a API faz? (Principais Rotas)

### Autenticação

* `POST /register`: Criação de nova conta.
* `POST /login`: Autentica o usuário e gera o token de acesso.

### Filmes

* `GET /films`: Lista os filmes com dados extras (ex: anos desde o lançamento).
* `GET /films/eras`: Agrupa a saga por eras (Clássicos, Modernos e Recentes).

### Personagens

* `GET /people`: Listagem com filtros por planeta, espécie ou filme.
* `GET /people/{id}`: Detalhes específicos. Use `?expand=films` para trazer os filmes do personagem no mesmo JSON.

### Estatísticas

* `GET /stats`: Estatísticas da altura média, filme mais antigo e média de personagens.

---

## Como rodar na sua máquina

### 1. Preparar o Ambiente (venv)

No terminal, dentro da pasta do projeto:

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt

```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SWAPI_BASE_URL=https://swapi.dev/api
DATABASE_URL=sqlite:///./sql_app.db
SECRET_KEY=sua_chave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

### 4. Iniciar o Servidor

```bash
uvicorn app.main:app --reload

```

Acesse a documentação interativa em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
