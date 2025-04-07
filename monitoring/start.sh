#!/bin/bash

# Iniciar Loki
loki -config.file=/etc/loki/local-config.yaml &

# Iniciar Promtail
promtail -config.file=/etc/promtail/config.yml &

# Iniciar Prometheus
prometheus --config.file=/etc/prometheus/prometheus.yml &

# Iniciar SQLite Exporter
sqlite-exporter --config.file=/etc/sqlite-exporter/sqlite-exporter.yml &

# Iniciar Grafana
/run.sh
