# Monitoring Infrastructure

This directory contains the configuration for the Euystacio monitoring stack.

## Components

- **Grafana**: Visualization and dashboarding (http://localhost:3000)
- **Loki**: Log aggregation and querying
- **Promtail**: Log shipping agent
- **Prometheus**: Metrics collection

## Quick Start

```bash
# Start all monitoring services
docker-compose -f ../docker-compose.monitoring.yml up -d

# Check status
docker-compose -f ../docker-compose.monitoring.yml ps

# View logs
docker-compose -f ../docker-compose.monitoring.yml logs -f

# Stop services
docker-compose -f ../docker-compose.monitoring.yml down
```

## Access

- **Grafana**: http://localhost:3000 (default: admin/admin)
- **Prometheus**: http://localhost:9090
- **Loki**: http://localhost:3100

## Configuration Files

```
monitoring/
├── grafana/
│   ├── dashboards/
│   │   └── euystacio-dashboard.json    # Main monitoring dashboard
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboards.yml          # Dashboard provisioning
│       └── datasources/
│           └── datasources.yml         # Loki and Prometheus datasources
├── loki/
│   └── loki-config.yml                 # Log aggregation config
├── promtail/
│   └── promtail-config.yml            # Log shipping config
└── prometheus.yml                      # Metrics collection config
```

## Customization

### Add New Dashboard

1. Create dashboard in Grafana UI
2. Export as JSON
3. Save to `grafana/dashboards/`
4. Restart Grafana container

### Add New Log Source

Edit `promtail/promtail-config.yml`:

```yaml
scrape_configs:
  - job_name: my-app
    static_configs:
      - targets:
          - localhost
        labels:
          job: my-app
          __path__: /var/log/my-app/*.log
```

### Add New Metrics Source

Edit `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'my-service'
    static_configs:
      - targets: ['my-service:9090']
```

## Troubleshooting

### Grafana won't start

```bash
# Check if port 3000 is in use
netstat -tuln | grep 3000

# Check logs
docker-compose -f ../docker-compose.monitoring.yml logs grafana
```

### Loki not receiving logs

```bash
# Verify Promtail is running
docker-compose -f ../docker-compose.monitoring.yml ps promtail

# Check Promtail logs
docker-compose -f ../docker-compose.monitoring.yml logs promtail

# Test Loki API
curl http://localhost:3100/ready
```

### Prometheus not scraping

```bash
# Check targets in Prometheus UI
open http://localhost:9090/targets

# Verify configuration
docker-compose -f ../docker-compose.monitoring.yml exec prometheus \
  promtool check config /etc/prometheus/prometheus.yml
```

## Data Retention

- **Loki**: 30 days (configurable in `loki/loki-config.yml`)
- **Prometheus**: 15 days (default)

To change retention:

**Loki** (`loki/loki-config.yml`):
```yaml
limits_config:
  retention_period: 720h  # 30 days
```

**Prometheus** (`docker-compose.monitoring.yml`):
```yaml
command:
  - '--storage.tsdb.retention.time=30d'
```

## Security

- Change default Grafana password on first login
- Use environment variables for sensitive configuration
- Restrict network access to monitoring services
- Enable HTTPS for production deployments

## See Also

- [RESILIENCE_SECURITY_GUIDE.md](../RESILIENCE_SECURITY_GUIDE.md) - Complete guide
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Prometheus Documentation](https://prometheus.io/docs/)
