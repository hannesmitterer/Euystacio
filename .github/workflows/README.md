# Protocollo Meta Salvage - CI/CD Workflows

This directory contains GitHub Actions workflows for the Protocollo Meta Salvage automation and continuous delivery system.

## Overview

The Protocollo Meta Salvage CI/CD system provides comprehensive testing, deployment, and monitoring automation for ensuring Peace Bonds enforcement and risk detection across the Euystacio ecosystem.

## Workflows

### 1. Integration Testing (`protocollo-integration-test.yml`)

**Purpose:** Validates orchestration and monitoring layers

**Triggers:**
- Push to `main` or `protocollo/**` branches
- Pull requests to `main`
- Manual dispatch with custom parameters

**Key Features:**
- Apache Kafka/Flink orchestration testing
- Prometheus monitoring validation
- Service health checks
- Integration layer testing
- Automated service cleanup

**Services Tested:**
- Kafka (with Zookeeper)
- Prometheus
- Redis
- Custom orchestration layers

**Usage:**
```bash
# Trigger manually with custom settings
gh workflow run protocollo-integration-test.yml \
  -f enable-kafka=true \
  -f enable-prometheus=true
```

### 2. End-to-End Testing (`protocollo-e2e-test.yml`)

**Purpose:** Simulates real-world scenarios for Peace Bonds enforcement

**Triggers:**
- Push to `main` or `protocollo/**` branches
- Pull requests to `main`
- Manual dispatch with scenario selection

**Test Scenarios:**
1. **Peace Bonds Enforcement** - Tests complete policy enforcement workflow
2. **Risk Detection Pipeline** - Validates risk detection mechanisms
3. **Symbiosis Score Validation** - Tests scoring and threshold enforcement

**Matrix Strategy:**
- Runs scenarios in parallel
- Fail-fast disabled for comprehensive results

**Usage:**
```bash
# Run specific scenario
gh workflow run protocollo-e2e-test.yml \
  -f scenario=peace-bonds
```

### 3. Infrastructure Deployment (`protocollo-infrastructure-deploy.yml`)

**Purpose:** Automates infrastructure provisioning with Terraform and Kubernetes

**Triggers:**
- Push to `main` with infrastructure changes
- Manual dispatch with environment selection

**Features:**
- Terraform plan/apply/destroy operations
- Kubernetes manifest generation and validation
- Multi-environment support (staging/production)
- PR comments with Terraform plans

**Terraform Actions:**
- `plan` - Preview infrastructure changes
- `apply` - Apply infrastructure changes
- `destroy` - Tear down infrastructure

**Usage:**
```bash
# Plan infrastructure changes for staging
gh workflow run protocollo-infrastructure-deploy.yml \
  -f environment=staging \
  -f terraform-action=plan

# Apply changes to production
gh workflow run protocollo-infrastructure-deploy.yml \
  -f environment=production \
  -f terraform-action=apply
```

### 4. Monitoring Deployment (`protocollo-monitoring-deploy.yml`)

**Purpose:** Deploys and configures monitoring stack (Prometheus, Grafana)

**Triggers:**
- Push to `main` with monitoring config changes
- Manual dispatch with component selection

**Components:**
- Prometheus with custom scrape configs
- Grafana dashboards for Protocollo Meta Salvage
- Alert rules for Peace Bonds violations
- Alertmanager configuration

**Dashboards:**
- **Protocollo Overview** - System-wide metrics
- **Peace Bonds** - Policy enforcement metrics
- **Symbiosis Score** - Risk assessment metrics

**Usage:**
```bash
# Deploy complete monitoring stack
gh workflow run protocollo-monitoring-deploy.yml \
  -f deploy-prometheus=true \
  -f deploy-grafana=true
```

### 5. Workflow Dispatcher (`protocollo-workflow-dispatcher.yml`)

**Purpose:** Orchestrates coordinated execution of multiple workflows

**Triggers:**
- Manual dispatch only

**Workflow Types:**
- `full-pipeline` - Run all workflows in sequence
- `integration-only` - Only integration tests
- `e2e-only` - Only E2E tests
- `deploy-only` - Only infrastructure deployment
- `monitoring-only` - Only monitoring deployment

**Execution Flow:**
```
Dispatcher → Integration Tests → E2E Tests → Infrastructure Deploy → Monitoring Deploy → Final Summary
```

**Usage:**
```bash
# Run complete pipeline for staging
gh workflow run protocollo-workflow-dispatcher.yml \
  -f workflow-type=full-pipeline \
  -f environment=staging
```

## Reusable Actions

### Risk Detection Test (`actions/risk-detection-test`)

**Purpose:** Reusable action for testing risk detection mechanisms

**Inputs:**
- `python-version` (default: 3.9)
- `test-path` (default: tests/risk_detection)
- `symbiosis-threshold` (default: 0.75)
- `enable-coverage` (default: true)

**Outputs:**
- `test-results` - Test execution summary
- `coverage-percentage` - Code coverage

**Example:**
```yaml
- uses: ./.github/actions/risk-detection-test
  with:
    symbiosis-threshold: '0.80'
    enable-coverage: 'true'
```

### Policy Enforcement Test (`actions/policy-enforcement-test`)

**Purpose:** Reusable action for OPA policy validation

**Inputs:**
- `opa-version` (default: 0.59.0)
- `policy-path` (default: policies/peace_bonds)
- `test-data-path` (default: tests/policy_enforcement/data)
- `python-version` (default: 3.9)

**Outputs:**
- `test-results` - Policy test summary
- `violations-found` - Number of violations detected

**Example:**
```yaml
- uses: ./.github/actions/policy-enforcement-test
  with:
    policy-path: 'policies/peace_bonds'
```

### Integration Test Setup (`actions/integration-test-setup`)

**Purpose:** Sets up infrastructure services for integration testing

**Inputs:**
- `enable-kafka` (default: true)
- `enable-prometheus` (default: true)
- `enable-grafana` (default: false)
- `wait-timeout` (default: 60)

**Outputs:**
- `kafka-ready` - Kafka service status
- `prometheus-ready` - Prometheus service status
- `services-endpoint` - Service connection strings

**Example:**
```yaml
- uses: ./.github/actions/integration-test-setup
  with:
    enable-kafka: 'true'
    enable-prometheus: 'true'
    wait-timeout: '90'
```

## Configuration Files

### Prometheus Configuration
**Location:** `config/prometheus/prometheus.yml`

Defines scrape targets for:
- Protocollo API services
- Kafka metrics
- Symbiosis Score service
- Peace Bonds policy engine

### Alert Rules
**Location:** `config/prometheus/alerts/protocollo-alerts.yml`

Key alerts:
- `SymbiosisScoreLow` - Score below threshold
- `PeaceBondsViolation` - Policy violations detected
- `KafkaConsumerLag` - Event processing delays
- `ServiceDown` - Service health issues

### Grafana Dashboards
**Location:** `config/grafana/dashboards/`

Available dashboards:
- `protocollo-overview.json` - System overview
- `peace-bonds.json` - Policy enforcement metrics

### Terraform Configuration
**Location:** `infrastructure/terraform/main.tf`

Defines:
- Kubernetes namespace creation
- Resource provisioning
- Environment-specific configurations

### Kubernetes Manifests
**Location:** `k8s/protocollo/`

Includes:
- Namespace definitions
- Service deployments (Prometheus, etc.)
- ConfigMaps and secrets

## OPA Policies

### Peace Bonds Policy
**Location:** `policies/peace_bonds/peace_bonds_policy.rego`

**Key Rules:**
- Symbiosis Score threshold enforcement (≥0.75)
- Authorization checks
- Resource usage validation
- Anomaly detection
- Risk level calculation

**Policy Tests:**
**Location:** `policies/peace_bonds/peace_bonds_test.rego`

Comprehensive test coverage for all policy rules.

## Python Tests

### Risk Detection Tests
**Location:** `tests/risk_detection/test_symbiosis_score.py`

Tests:
- Symbiosis Score calculation
- Anomaly detection
- Risk assessment
- Threshold validation

### Policy Enforcement Tests
**Location:** `tests/policy_enforcement/test_peace_bonds.py`

Tests:
- Peace Bonds policy evaluation
- Violation detection
- Risk level calculation
- Recommendation generation

## Environment Variables

Required for workflows:

```bash
# GitHub (automatically provided)
GITHUB_TOKEN

# Custom (set in repository secrets)
KUBECONFIG  # For Kubernetes deployments
```

## Best Practices

### 1. Running Tests Locally

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run risk detection tests
pytest tests/risk_detection -v

# Run policy enforcement tests
pytest tests/policy_enforcement -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### 2. OPA Policy Validation

```bash
# Install OPA
curl -L -o opa https://openpolicyagent.org/downloads/v0.59.0/opa_linux_amd64_static
chmod +x opa
sudo mv opa /usr/local/bin/

# Test policies
opa test policies/peace_bonds/*.rego -v
```

### 3. Local Service Testing

```bash
# Start services with Docker Compose
docker-compose -f docker-compose.test.yml up -d

# Wait for services
sleep 30

# Run integration tests
pytest tests/integration -v

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

### 4. Terraform Validation

```bash
# Format check
terraform fmt -check -recursive infrastructure/terraform/

# Validate configuration
cd infrastructure/terraform
terraform init
terraform validate
```

## Monitoring and Alerts

### Accessing Prometheus

Local: `http://localhost:9090`
Production: Configure via ingress

### Accessing Grafana

Local: `http://localhost:3000`
Default credentials: admin/admin

### Key Metrics

- `symbiosis_score` - Current Symbiosis Score
- `peace_bonds_violations_total` - Total violations
- `peace_bonds_evaluations_total` - Policy evaluations
- `kafka_consumer_lag` - Event processing lag
- `events_processed_total` - Processing throughput

## Troubleshooting

### Workflow Failures

1. Check workflow logs in Actions tab
2. Review artifact uploads for detailed results
3. Verify service health in integration tests
4. Check resource availability

### OPA Policy Errors

```bash
# Validate policy syntax
opa check policies/peace_bonds/peace_bonds_policy.rego

# Run specific test
opa test policies/peace_bonds/peace_bonds_test.rego -v
```

### Terraform Issues

```bash
# View detailed plan
terraform plan -detailed-exitcode

# Check state
terraform show

# Refresh state
terraform refresh
```

## Contributing

When adding new workflows:

1. Follow existing naming conventions
2. Include comprehensive documentation
3. Add test coverage
4. Update this README
5. Test locally before committing

## Support

For issues or questions:
- Open an issue in the repository
- Tag with `protocollo-meta-salvage` label
- Include workflow run logs

## License

See [SACRED_COMMONS_LICENSE.md](../../SACRED_COMMONS_LICENSE.md)
