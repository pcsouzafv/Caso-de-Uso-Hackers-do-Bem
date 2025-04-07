#!/bin/bash

echo "🚀 Iniciando Loki..."
/usr/local/bin/loki -config.file=/etc/loki-config.yaml &

echo "📡 Iniciando Promtail..."
/usr/local/bin/promtail -config.file=/etc/promtail-config.yaml &

echo "📊 Iniciando Grafana..."
/usr/sbin/grafana-server --homepath=/usr/share/grafana --config=/etc/grafana/grafana.ini
