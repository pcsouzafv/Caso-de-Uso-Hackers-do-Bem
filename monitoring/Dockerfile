FROM grafana/grafana:10.2.2-ubuntu

# Instalar dependências necessárias
USER root
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário grafana
RUN useradd -ms /bin/bash grafana

# Instalar Loki e Promtail
RUN curl -LO https://github.com/grafana/loki/releases/download/v2.9.0/loki-linux-amd64.zip && \
    unzip loki-linux-amd64.zip && mv loki-linux-amd64 /usr/local/bin/loki && chmod +x /usr/local/bin/loki && \
    curl -LO https://github.com/grafana/loki/releases/download/v2.9.0/promtail-linux-amd64.zip && \
    unzip promtail-linux-amd64.zip && mv promtail-linux-amd64 /usr/local/bin/promtail && chmod +x /usr/local/bin/promtail

# Criar diretórios necessários
RUN mkdir -p /etc/loki /etc/promtail /var/log/task_manager

# Copiar configurações
COPY loki-config.yaml /etc/loki/
COPY promtail-config.yaml /etc/promtail/
COPY start.sh /usr/local/bin/

# Garantir permissões corretas
RUN chmod +x /usr/local/bin/start.sh && \
    chown -R grafana:grafana /etc/loki /etc/promtail /usr/local/bin/start.sh /var/log/task_manager

# Usar usuário grafana
USER grafana

# Expor portas
EXPOSE 3000 3100 9080

# Comando para iniciar
CMD ["/usr/local/bin/start.sh"]
