# Caso de Uso - Hackers do Bem

## Descrição
Um sistema de gerenciamento de tarefas construído com Flask e SQLite, com recursos de monitoramento e segurança.

## Funcionalidades
- Gerenciamento de usuários
- Sistema de autenticação
- CRUD de tarefas
- Interface administrativa
- Monitoramento com Loki, Promtail, Prometheus e Grafana
- Testes automatizados

## Requisitos
- Python 3.13+
- Docker e Docker Compose
- Git

## Instalação
```bash
# Clonar o repositório
git clone https://github.com/pcsouzafv/Caso-de-Uso-Hackers-do-Bem.git
cd Caso-de-Uso-Hackers-do-Bem

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar o banco de dados
python init_db.py
```

## Configuração do Monitoramento
```bash
# Iniciar os serviços de monitoramento
docker-compose -f monitoring/docker-compose.yml up -d

# Acessar os serviços
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
# Loki: http://localhost:3100
# Login padrão: admin/admin
```

## Testes
```bash
# Executar testes unitários
pytest tests/unit/

# Executar testes funcionais
pytest tests/functional/

# Executar testes de segurança
bandit -r .
```
