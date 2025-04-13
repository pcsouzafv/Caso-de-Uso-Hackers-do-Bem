# Task Manager - Hackers do Bem

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

<p align="center">
  <video width="800" controls>
    <source src="https://github.com/user-attachments/assets/440ea7cd-7fcf-46b6-af10-1ba3e4e10153" type="video/mp4">
    Seu navegador não suporta vídeos HTML5.
  </video>
</p>




https://github.com/user-attachments/assets/f0f52fc1-9f97-4356-963a-43f63ffa9a53
## Sobre o Projeto

Este é um sistema de gerenciamento de tarefas desenvolvido durante o curso Hackers do Bem, com foco em segurança e boas práticas de desenvolvimento. O sistema oferece uma interface moderna e responsiva, com suporte a temas claro/escuro e recursos avançados de monitoramento.

## Funcionalidades Principais

- Autenticação segura com hash de senhas
- CRUD completo de tarefas com priorização
- Sistema de usuários com controle de administração
- Dashboard administrativo com estatísticas
- Sistema de logs com monitoramento em tempo real
- Interface moderna e responsiva com suporte a temas
- Implementação de segurança e proteção contra XSS/CSRF
- Testes automatizados (unitários, funcionais e de segurança)

## Tecnologias Utilizadas

- **Backend**: Flask 3.0+ com SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript moderno
- **Banco de Dados**: SQLite
- **Monitoramento**: Loki, Promtail, Prometheus e Grafana
- **Testes**: pytest, bandit
- **Temas**: Bootstrap 5, Font Awesome 6

## Requisitos

- Python 3.13 ou superior
- Docker e Docker Compose (para monitoramento)
- Git
- Node.js (opcional, para desenvolvimento frontend)

## Instalação

1. **Clonar o Repositório**
```bash
git clone https://github.com/pcsouzafv/Task-Manager-using-Flask.git
cd Task-Manager-using-Flask
```

2. **Configurar Ambiente Virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

3. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

4. **Iniciar o Banco de Dados**
```bash
python init_db.py
```

5. **Configurar Variáveis de Ambiente** (opcional)
```bash
cp .env.example .env
# Editar .env com suas configurações
```

## Configuração do Monitoramento

Para configurar o sistema de monitoramento (opcional):

```bash
# Iniciar serviços de monitoramento
docker-compose -f monitoring/docker-compose.yml up -d

# Acessar os serviços
Grafana: http://localhost:3000
Prometheus: http://localhost:9090
Loki: http://localhost:3100

# Login padrão: admin/admin
```

## Executando os Testes

```bash
# Testes unitários
pytest tests/unit/

# Testes funcionais
pytest tests/functional/

# Testes de segurança
bandit -r .
```

## Customização do Tema

O sistema suporta temas claro/escuro que podem ser alternados através da interface. As cores podem ser customizadas editando o arquivo `static/css/styles.css`.

## Estrutura do Projeto

```
Task-Manager-using-Flask/
├── app/                 # Aplicação principal
├── monitoring/          # Configurações de monitoramento
├── static/              # Arquivos estáticos
├── templates/           # Templates HTML
├── tests/              # Testes automatizados
├── .env.example        # Exemplo de variáveis de ambiente
└── requirements.txt    # Dependências do projeto
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona recurso incrível'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Agradecimentos

- Especial agradecimento ao curso Hackers do Bem
- Professora: Helena Carreço
- Desenvolvido por Ricardo Souza

## Documentação Adicional

- [Documentação Geral](https://github.com/pcsouzafv/Caso-de-Uso-Hackers-do-Bem/blob/main/docs/DOCUMENTACAO.md)
- [Guia de Segurança](https://github.com/pcsouzafv/Caso-de-Uso-Hackers-do-Bem/blob/main/docs/GUIA_SEGURANCA.md)
- [Guia de Contribuição](https://github.com/pcsouzafv/Caso-de-Uso-Hackers-do-Bem/blob/main/docs/GUIA_CONTRIBUICAO.md)
- [Guia de Monitoramento](https://github.com/pcsouzafv/Task-Manager-using-Flask/docs/GUIA_MONITORAMENTO.md)
