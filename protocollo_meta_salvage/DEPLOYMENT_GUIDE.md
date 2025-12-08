# Protocollo Meta Salvage - Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Monitoring Setup](#monitoring-setup)
5. [Workflow Orchestration](#workflow-orchestration)
6. [Security Configuration](#security-configuration)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python**: 3.9 or higher
- **Docker**: 20.10 or higher
- **Kubernetes**: 1.24 or higher
- **kubectl**: Matching your K8s version
- **Terraform**: 1.4 or higher
- **Helm**: 3.10 or higher (optional, for charts)

### Required Services

- **Apache Kafka**: For event streaming
- **PostgreSQL**: For persistent storage
- **Redis**: For caching and rate limiting
- **Prometheus**: For metrics collection
- **Grafana**: For visualization

## Local Development Setup

### Step 1: Clone and Install

```bash
# Clone repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio/protocollo_meta_salvage

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/protocollo
REDIS_URL=redis://localhost:6379

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_PREFIX=protocollo_

# Kubernetes
K8S_NAMESPACE=protocollo-meta-salvage
K8S_CONTEXT=minikube

# Monitoring
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3000

# ML Configuration
ML_MODEL_TYPE=gradient_boosting
ML_FRAMEWORK=tensorflow

# Logging
LOG_LEVEL=INFO
AUDIT_LOG_PATH=./audit_logs
```

### Step 3: Initialize Database

```bash
# Create database schema
python scripts/init_database.py

# Run migrations (if using Alembic)
alembic upgrade head
```

### Step 4: Start Local Services

```bash
# Start Kafka (using Docker)
docker run -d --name kafka \
  -p 9092:9092 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  wurstmeister/kafka

# Start PostgreSQL
docker run -d --name postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=protocollo \
  postgres:14

# Start Redis
docker run -d --name redis \
  -p 6379:6379 \
  redis:7
```

### Step 5: Run the System

```bash
# Run coordinator
python -m protocollo_meta_salvage.coordinator

# Or run individual components
python -m protocollo_meta_salvage.monitoring
python -m protocollo_meta_salvage.decision_engine
python -m protocollo_meta_salvage.automation
```

## Kubernetes Deployment

### Step 1: Prepare Cluster

```bash
# Create namespace
kubectl create namespace protocollo-meta-salvage

# Label namespace
kubectl label namespace protocollo-meta-salvage \
  purpose=ethical-preservation
```

### Step 2: Configure Secrets

```bash
# Create secret for database credentials
kubectl create secret generic db-credentials \
  --namespace=protocollo-meta-salvage \
  --from-literal=username=protocollo \
  --from-literal=password=<your-password> \
  --from-literal=database=protocollo

# Create secret for Kafka
kubectl create secret generic kafka-config \
  --namespace=protocollo-meta-salvage \
  --from-literal=bootstrap-servers=kafka:9092

# Create secret for ML models
kubectl create secret generic ml-config \
  --namespace=protocollo-meta-salvage \
  --from-literal=model-type=gradient_boosting
```

### Step 3: Deploy Infrastructure

```bash
# Apply ConfigMap
kubectl apply -f config/kubernetes_manifests.yaml

# Verify ConfigMap
kubectl get configmap protocollo-config \
  -n protocollo-meta-salvage -o yaml
```

### Step 4: Deploy Components

```bash
# Deploy all components
kubectl apply -f config/kubernetes_manifests.yaml

# Watch deployment progress
kubectl get pods -n protocollo-meta-salvage -w

# Check status
kubectl get deployments -n protocollo-meta-salvage
kubectl get services -n protocollo-meta-salvage
```

### Step 5: Verify Deployment

```bash
# Check pod logs
kubectl logs -n protocollo-meta-salvage \
  -l app=symbiosis-monitor --tail=50

# Test service connectivity
kubectl port-forward -n protocollo-meta-salvage \
  svc/symbiosis-monitor 8001:8001

curl http://localhost:8001/health
```

## Monitoring Setup

### Prometheus Configuration

```bash
# Create Prometheus namespace
kubectl create namespace monitoring

# Deploy Prometheus
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --values config/prometheus-values.yaml

# Configure scraping for Protocollo components
kubectl apply -f config/prometheus-servicemonitor.yaml
```

### Grafana Setup

```bash
# Deploy Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set adminPassword=<your-password>

# Get Grafana URL
kubectl port-forward -n monitoring \
  svc/grafana 3000:80

# Import dashboard
# Navigate to http://localhost:3000
# Import config/grafana_dashboard.json
```

### Alert Configuration

```bash
# Configure Alertmanager
kubectl apply -f config/alertmanager-config.yaml

# Test alerts
kubectl port-forward -n monitoring \
  svc/alertmanager 9093:9093
```

## Workflow Orchestration

### Apache Airflow Setup

```bash
# Deploy Airflow using Helm
helm repo add apache-airflow \
  https://airflow.apache.org
helm repo update

helm install airflow apache-airflow/airflow \
  --namespace protocollo-meta-salvage \
  --set dags.gitSync.enabled=true \
  --set dags.gitSync.repo=https://github.com/hannesmitterer/Euystacio.git \
  --set dags.gitSync.subPath=protocollo_meta_salvage/orchestration

# Access Airflow UI
kubectl port-forward -n protocollo-meta-salvage \
  svc/airflow-webserver 8080:8080

# Trigger DAG
airflow dags trigger protocollo_meta_salvage_monitoring
```

### Argo Workflows Setup

```bash
# Install Argo Workflows
kubectl create namespace argo
kubectl apply -n argo -f \
  https://github.com/argoproj/argo-workflows/releases/download/v3.4.8/install.yaml

# Deploy Protocollo workflows
kubectl apply -f orchestration/argo_workflows.yaml

# Submit workflow
argo submit -n protocollo-meta-salvage \
  orchestration/argo_workflows.yaml
```

## Security Configuration

### RBAC Setup

```bash
# Create service accounts
kubectl apply -f config/kubernetes_manifests.yaml

# Verify RBAC
kubectl auth can-i create resourcequotas \
  --as=system:serviceaccount:protocollo-meta-salvage:resource-enforcer-sa
```

### Network Policies

```bash
# Apply network policies
kubectl apply -f config/network-policies.yaml

# Test connectivity
kubectl run test-pod -n protocollo-meta-salvage \
  --image=busybox --rm -it -- /bin/sh
```

### Secret Management

```bash
# Use Sealed Secrets (recommended)
kubectl apply -f \
  https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.20.5/controller.yaml

# Seal secrets
kubeseal --format yaml < secret.yaml > sealed-secret.yaml
kubectl apply -f sealed-secret.yaml
```

## Production Best Practices

### High Availability

```bash
# Scale deployments
kubectl scale deployment symbiosis-monitor \
  -n protocollo-meta-salvage --replicas=3

kubectl scale deployment peace-bond-engine \
  -n protocollo-meta-salvage --replicas=3
```

### Resource Limits

```yaml
# Ensure all pods have resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Backup Strategy

```bash
# Backup audit logs
kubectl exec -n protocollo-meta-salvage \
  deployment/audit-logger -- \
  tar czf /tmp/audit-backup.tar.gz /audit_logs

# Backup database
pg_dump -h <db-host> -U protocollo protocollo > backup.sql
```

### Monitoring and Alerts

```yaml
# Configure critical alerts
- alert: SymbiosisScoreCritical
  expr: symbiosis_score < 0.3
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Critical symbiosis score detected"

- alert: PeaceBondActivationFailure
  expr: rate(peace_bond_activation_failures[5m]) > 0.1
  for: 5m
  labels:
    severity: high
```

## Troubleshooting

### Common Issues

#### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n protocollo-meta-salvage

# Check events
kubectl get events -n protocollo-meta-salvage --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name> -n protocollo-meta-salvage --previous
```

#### Database Connection Issues

```bash
# Test database connectivity
kubectl run pg-test -n protocollo-meta-salvage \
  --image=postgres:14 --rm -it -- \
  psql -h postgres -U protocollo -d protocollo

# Check secret
kubectl get secret db-credentials \
  -n protocollo-meta-salvage -o yaml
```

#### Kafka Connection Issues

```bash
# Test Kafka connectivity
kubectl run kafka-test -n protocollo-meta-salvage \
  --image=wurstmeister/kafka --rm -it -- \
  kafka-console-producer.sh \
  --broker-list kafka:9092 --topic test
```

#### Permission Issues

```bash
# Check RBAC
kubectl auth can-i --list \
  --as=system:serviceaccount:protocollo-meta-salvage:resource-enforcer-sa

# View service account
kubectl get serviceaccount resource-enforcer-sa \
  -n protocollo-meta-salvage -o yaml
```

### Debug Mode

```bash
# Enable debug logging
kubectl set env deployment/symbiosis-monitor \
  -n protocollo-meta-salvage \
  LOG_LEVEL=DEBUG

# Restart pods
kubectl rollout restart deployment/symbiosis-monitor \
  -n protocollo-meta-salvage
```

### Performance Tuning

```bash
# Adjust resource limits
kubectl set resources deployment symbiosis-monitor \
  -n protocollo-meta-salvage \
  --limits=cpu=1000m,memory=1Gi \
  --requests=cpu=500m,memory=512Mi

# Scale horizontally
kubectl autoscale deployment symbiosis-monitor \
  -n protocollo-meta-salvage \
  --min=2 --max=10 --cpu-percent=80
```

## Maintenance

### Updating the System

```bash
# Build new image
docker build -t protocollo-meta-salvage:v1.1.0 .

# Update deployment
kubectl set image deployment/symbiosis-monitor \
  -n protocollo-meta-salvage \
  monitor=protocollo-meta-salvage:v1.1.0

# Monitor rollout
kubectl rollout status deployment/symbiosis-monitor \
  -n protocollo-meta-salvage
```

### Database Migration

```bash
# Run migration job
kubectl apply -f config/migration-job.yaml

# Check migration status
kubectl logs -n protocollo-meta-salvage \
  job/database-migration
```

## Support

For additional support:
- GitHub Issues: https://github.com/hannesmitterer/Euystacio/issues
- Documentation: See README.md and docs/
- Community: GitHub Discussions

---

**Last Updated**: 2025-12-08
