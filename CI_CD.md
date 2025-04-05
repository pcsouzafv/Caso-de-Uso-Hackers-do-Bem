# Pipeline CI/CD - Task Manager

Este documento descreve o pipeline de Integração Contínua (CI) e Entrega Contínua (CD) implementado para o Task Manager.

## Estrutura do Pipeline

O pipeline é implementado usando GitHub Actions e consiste em duas etapas principais:

### 1. Test Job

- **Trigger**: Ativado em pushes e pull requests para as branches `main`, `develop` e `staging`
- **Ambiente**: Ubuntu Latest com Python 3.9
- **Etapas**:
  - Checkout do código
  - Setup do Python
  - Instalação de dependências
  - Lint com flake8
  - Testes com pytest e cobertura
  - Upload do relatório de cobertura

### 2. Build Job

- **Trigger**: Ativado em pushes para `main` e `staging`
- **Dependência**: Requer sucesso do job de teste
- **Ambiente**: Ubuntu Latest com Python 3.9
- **Etapas**:
  - Checkout do código
  - Setup do Python
  - Instalação de dependências
  - Build do pacote
  - Criação de release (apenas na main)

## Branches

O projeto usa três branches principais:

1. **main**: Código em produção
2. **staging**: Código em teste/homologação
3. **develop**: Código em desenvolvimento

## Fluxo de Trabalho

1. Desenvolvedores trabalham em feature branches
2. Pull requests são criados para `develop`
3. Após testes, merge em `staging`
4. Após validação, merge em `main`

## Testes

O pipeline executa:

- **Testes Unitários**: Verificam componentes isolados
- **Testes de Integração**: Verificam interações entre componentes
- **Cobertura de Código**: Mínimo de 80% exigido

## Releases

Releases automáticas são criadas quando:

1. Todos os testes passam
2. Build é bem-sucedido
3. Código é mergeado na `main`

## Monitoramento

- Relatórios de cobertura no Codecov
- Histórico de builds no GitHub Actions
- Notificações de falha via email

## Comandos Úteis

```bash
# Rodar testes localmente
pytest tests/ --cov=./

# Verificar lint
flake8 .

# Build local
python setup.py sdist bdist_wheel
```

## Configuração Local

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o pre-commit: `pre-commit install`
4. Execute os testes: `pytest`

## Troubleshooting

Se os testes falharem:

1. Verifique as dependências
2. Limpe os caches: `pytest --cache-clear`
3. Verifique o log de erros
4. Execute testes específicos: `pytest tests/test_app.py -k test_name`
