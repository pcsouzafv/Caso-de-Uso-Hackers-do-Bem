# Sistema de Gerenciamento de Tarefas

Uma aplicação web para gerenciar suas tarefas diárias, construída com Flask e SQLite.

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

- Python 3.8+
- pip

Execute o seguinte comando para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

## Uso

1. Clone o repositório

2. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente (opcional)
   ```bash
   cp config.py.example config.py
   ```

4. Inicie o servidor de desenvolvimento:
   ```bash
   python app.py
   ```

5. Acesse a aplicação em http://localhost:5000

## Estrutura do Projeto

```
.
├── app/                # Código principal da aplicação
│   ├── __init__.py    # Inicialização do Flask
│   ├── models.py      # Modelos do SQLAlchemy
│   └── routes.py      # Rotas da aplicação
├── tests/             # Testes da aplicação
│   ├── functional/    # Testes funcionais
│   ├── integration/   # Testes de integração
│   └── unit/          # Testes unitários
├── config.py          # Configurações da aplicação
└── requirements.txt   # Dependências do projeto
```

## Testes

Para executar os testes:

```bash
pytest
```

Para gerar relatório de cobertura:

```bash
pytest --cov=app
```

## Tecnologias Utilizadas

- **Backend**: Flask, SQLAlchemy, SQLite
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

## Licença

MIT
