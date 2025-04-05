# Sistema de Gerenciamento de Tarefas

Uma aplicação web para gerenciar suas tarefas diárias, construída com FastAPI e SQLite.

## Funcionalidades

### Para Usuários:
- Cadastrar nova tarefa
- Editar tarefas existentes
- Marcar tarefas como concluídas
- Remover tarefas obsoletas
- Visualizar tarefas pendentes
- Buscar tarefas por palavras-chave

### Para Administradores:
- Visualizar todas as contas de usuário
- Remover contas de usuários inativos ou suspeitos
- Acessar os logs do sistema

## Requisitos

Execute o seguinte comando para instalar as bibliotecas necessárias:

```
pip install -r requirements.txt
```

## Uso

1. Clone o repositório

2. Instale as dependências
   ```
   pip install -r requirements.txt
   ```

3. Crie um usuário administrador (opcional)
   ```
   python create_admin.py nome_usuario senha
   ```

4. Inicie o backend:
   ```
   uvicorn main:app --reload
   ```

5. Acesse o frontend através de um servidor web simples:
   ```
   python -m http.server 8080 --directory static
   ```

6. Acesse a aplicação em seu navegador:
   - Frontend: http://localhost:8080
   - API (documentação): http://localhost:8000/docs

## Tecnologias Utilizadas

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Autenticação**: JWT

## API Endpoints

### Autenticação
- `POST /token` - Obter token de acesso
- `POST /users/` - Criar novo usuário

### Tarefas
- `GET /tasks/` - Listar todas as tarefas do usuário atual
- `POST /tasks/` - Criar nova tarefa
- `GET /tasks/{task_id}` - Obter detalhes de uma tarefa
- `PUT /tasks/{task_id}` - Atualizar tarefa existente
- `DELETE /tasks/{task_id}` - Excluir tarefa
- `GET /tasks/pending/` - Listar tarefas pendentes
- `GET /tasks/search/` - Buscar tarefas por palavra-chave

### Administração
- `GET /admin/users/` - Listar todos os usuários
- `DELETE /admin/users/{user_id}` - Remover usuário
- `GET /admin/logs/` - Acessar logs do sistema
