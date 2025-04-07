FROM grafana/grafana:10.2.2-ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y curl unzip gnupg software-properties-common adduser libfontconfig1 && \
    useradd -ms /bin/bash grafana

# Install Loki
RUN curl -LO https://github.com/grafana/loki/releases/download/v2.9.0/loki-linux-amd64.zip && \
    unzip loki-linux-amd64.zip && mv loki-linux-amd64 /usr/local/bin/loki && chmod +x /usr/local/bin/loki

# Install Promtail
RUN curl -LO https://github.com/grafana/loki/releases/download/v2.9.0/promtail-linux-amd64.zip && \
    unzip promtail-linux-amd64.zip && mv promtail-linux-amd64 /usr/local/bin/promtail && chmod +x /usr/local/bin/promtail

COPY loki-config.yaml /etc/loki-config.yaml
COPY promtail-config.yaml /etc/promtail-config.yaml
COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 3000 3100 9080

CMD ["/start.sh"]
