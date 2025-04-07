# Stack de Monitoramento Docker

Esta imagem Docker contém uma stack completa de monitoramento com:
- Loki (armazenamento e consulta de logs)
- Promtail (coletor de logs)
- Grafana (visualização de dados)

## Requisitos

- Docker
- Docker Compose (opcional)
- Mínimo de 4GB de RAM

## Build da Imagem

```bash
docker build -t observabilidade-v1 .
```

## Executando a Imagem

```bash
docker run -d \
  -v /var/log/task_manager:/var/log/task_manager \
  -p 3000:3000 \
  -p 3100:3100 \
  -p 9080:9080 \
  --name monolith \
  observabilidade-v1
```

## Acessando os Serviços

- Grafana: http://localhost:3000
- Loki: http://localhost:3100
- Promtail: http://localhost:9080

## Configuração do Task Manager

Para que o Task Manager envie seus logs para esta stack de monitoramento, você precisa:

1. Configurar o Task Manager para escrever logs em `/var/log/task_manager`
2. Garantir que o diretório tenha as permissões corretas
3. Reiniciar o Task Manager para aplicar as mudanças

## Configuração do Grafana

1. Acesse http://localhost:3000
2. Login padrão:
   - Usuário: admin
   - Senha: admin
3. Adicione o Loki como data source:
   - URL: http://localhost:3100
   - Tipo: Loki

## Configuração do Loki

O Loki está configurado para:
- Armazenar logs por 24 horas
- Usar o sistema de arquivos como backend
- Não requer autenticação

## Configuração do Promtail

O Promtail está configurado para:
- Monitorar logs em `/var/log/task_manager/*.log`
- Enviar logs para o Loki na porta 3100
- Atualizar posições a cada 10 segundos

## Permissões

Certifique-se de que o diretório de logs tem as permissões corretas:

```bash
mkdir -p /var/log/task_manager
chmod 755 /var/log/task_manager
chown root:root /var/log/task_manager
```
