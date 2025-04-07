#!/bin/bash

<<<<<<< HEAD
echo "🚀 Iniciando Loki..."
/usr/local/bin/loki -config.file=/etc/loki-config.yaml &

echo "📡 Iniciando Promtail..."
/usr/local/bin/promtail -config.file=/etc/promtail-config.yaml &

echo "📊 Iniciando Grafana..."
/usr/sbin/grafana-server --homepath=/usr/share/grafana --config=/etc/grafana/grafana.ini
=======
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
>>>>>>> master
