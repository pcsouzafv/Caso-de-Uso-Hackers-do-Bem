# Stage 1: Build Grafana base
FROM grafana/grafana:9.5.15 as grafana-base

# Stage 2: Build Prometheus
FROM prom/prometheus:latest as prometheus

# Stage 3: Build Loki
FROM grafana/loki:2.9.0 as loki

# Stage 4: Build Promtail
FROM grafana/promtail:2.9.0 as promtail

# Stage 5: Build SQLite Exporter
FROM prom/sqlite-exporter:latest as sqlite-exporter

# Stage 6: Final image
FROM grafana/grafana:9.5.15

# Copiar configurações do Grafana
COPY grafana-dashboard.json /etc/grafana/provisioning/dashboards/task-manager.json
COPY grafana-sqlite-dashboard.json /etc/grafana/provisioning/dashboards/sqlite.json
COPY grafana-sqlite-dashboard-queries.json /etc/grafana/provisioning/dashboards/sqlite-queries.json
COPY grafana-prometheus-dashboard.json /etc/grafana/provisioning/dashboards/prometheus.json
COPY grafana-sqlite-datasource.json /etc/grafana/provisioning/datasources/sqlite.json

# Copiar configurações do Prometheus
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Copiar configurações do Loki
COPY loki-config.yaml /etc/loki/local-config.yaml

# Copiar configurações do Promtail
COPY promtail-config.yaml /etc/promtail/config.yml

# Copiar configurações do SQLite Exporter
COPY sqlite-exporter-config.yaml /etc/sqlite-exporter/sqlite-exporter.yml

# Expor as portas necessárias
EXPOSE 3000 3100 9090 9321 8086

# Configurações do Grafana
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_SECURITY_ADMIN_USER=admin

# Comando para iniciar o Grafana
CMD ["/run.sh"]
