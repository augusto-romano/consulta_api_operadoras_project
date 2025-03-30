Operadoras de Saúde - API de Consulta

Um projeto simples para consulta de operadoras de saúde no Brasil, com backend em Python e frontend em Vue.js.

Funcionalidades:

Busca por Razão Social ou Nome Fantasia

Visualização em tabela com ordenação

Design responsivo

Detalhes completos das operadoras

API RESTful com Flask

Tecnologias:

Backend:

Python 3.x

Flask

Pandas

Unidecode

Frontend:

Vue.js 3

Axios

CSS moderno

Para testar o projeto

Backend:

cd backend

pip install -r requirements.txt

.\venv\Scripts\activate

py app.py

Frontend:

cd frontend

npm install

npm run dev

Acesse:

API: http://localhost:5000

Frontend: http://localhost:5173/

Endpoint da API:

http://localhost:5000/search?query="termo"
