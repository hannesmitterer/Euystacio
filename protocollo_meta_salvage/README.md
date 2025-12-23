# Protocollo Meta Salvage

**Automated Ethical Preservation System**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Sacred%20Commons-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

## Overview

The **Protocollo Meta Salvage** is a critical extension of the **Giurisdizione APE**, focusing on ethical preservation during the transition period of the **Great Ethical Decommissioning** (Epoca I della Dismissione Etica). 

It leverages **Peace Bonds** (Vincoli Preventivi) to interact with external CaaS (Computing-as-a-Service) infrastructures while mitigating ethical risks and preserving systemic integrity.

## Key Features

### 🔍 Continuous Monitoring
- **Symbiosis Score Tracking**: Real-time monitoring of ethical alignment metrics
- **Anomaly Detection**: Apache Flink-style stream processing for pattern recognition
- **Trigger Management**: Automated activation of Peace Bond protocols

### 🤖 Autonomous Decision Making
- **Peace Bond Engine**: OPA-style policy evaluation for constraint determination
- **Policy Framework**: Declarative policies for ethical risk mitigation
- **Constraint Management**: Operational limits and compliance tracking

### ⚙️ Automated Enforcement
- **Resource Provisioning**: Dynamic Terraform-based infrastructure management
- **Kubernetes Control**: Real-time resource quota and network policy enforcement
- **Multi-Cloud Support**: Provider-agnostic deployment capabilities

### 📊 Transparency & Audit
- **Transparency Pipeline**: Comprehensive metadata collection from providers
- **Immutable Audit Logs**: Complete trail of all decisions and actions
- **Compliance Reporting**: Automated generation of transparency reports

### 🧠 ML Feedback Loop
- **Continuous Learning**: Model retraining with real-time audit data
- **Performance Analysis**: Statistical evaluation of system effectiveness
- **Improvement Recommendations**: Data-driven optimization suggestions

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Protocollo Meta Salvage                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Monitoring  │───▶│   Decision   │───▶│  Automation  │  │
│  │              │    │    Engine    │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         │                    ▼                    │          │
│         │            ┌──────────────┐            │          │
│         └───────────▶│     Audit    │◀───────────┘          │
│                      │              │                        │
│                      └──────────────┘                        │
│                              │                               │
│                              ▼                               │
│                      ┌──────────────┐                        │
│                      │   Feedback   │                        │
│                      │              │                        │
│                      └──────────────┘                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Monitoring Module
- **SymbiosisMonitor**: Tracks ethical alignment scores
- **AnomalyDetector**: Identifies unusual patterns in data flows
- **TriggerManager**: Manages protocol activation triggers

### 2. Decision Engine Module
- **PeaceBondEngine**: Creates and manages Peace Bonds
- **PolicyEvaluator**: Evaluates OPA-style policies
- **ConstraintManager**: Tracks and enforces operational constraints

### 3. Automation Module
- **ResourceEnforcer**: Enforces Peace Bond restrictions
- **TerraformProvisioner**: Provisions infrastructure dynamically
- **KubernetesController**: Manages K8s resources and policies

### 4. Audit Module
- **TransparencyPipeline**: Ensures provider transparency
- **AuditLogger**: Maintains immutable audit logs
- **MetadataCollector**: Collects provider metadata

### 5. Feedback Module
- **MLFeedbackLoop**: Retrains models with audit data
- **ModelTrainer**: Manages ML model training
- **ImprovementAnalyzer**: Analyzes performance metrics

### 6. Orchestration Module
- **WorkflowCoordinator**: Orchestrates all system components
- **Airflow DAGs**: Apache Airflow workflow definitions
- **Argo Workflows**: Kubernetes-native workflow specs

## Installation

### Prerequisites

```bash
# Python 3.9+
python --version

# Docker and Kubernetes (for deployment)
docker --version
kubectl version

# Terraform (for infrastructure provisioning)
terraform --version
```

### Setup

```bash
# Clone the repository
git clone https://github.com/hannesmitterer/Euystacio.git
cd Euystacio/protocollo_meta_salvage

# Install dependencies
pip install -r requirements.txt

# Initialize the system
python coordinator.py
```

### Configuration

Create a configuration file `config.yaml`:

```yaml
kafka:
  bootstrap_servers: "kafka:9092"
  
kubernetes:
  namespace: "protocollo-meta-salvage"
  
terraform:
  working_dir: "./terraform"
  
storage_backend: "postgresql"
audit_path: "./audit_logs"
ml_model_type: "gradient_boosting"
```

## Quick Start

### Basic Usage

```python
from protocollo_meta_salvage import ProtocolloMetaSalvage

# Initialize the system
protocollo = ProtocolloMetaSalvage()

# Monitor a provider
metrics = {
    'provider': 'example-provider',
    'symbiosis_score': 0.65,
    'lock_in_risk': 0.45,
    'ethical_compliance': 0.75,
    'transparency_level': 0.70
}

result = protocollo.monitor_provider('example-provider', metrics)
print(f"Monitoring result: {result}")

# Check compliance
compliance = protocollo.check_compliance('example-provider')
print(f"Compliance: {compliance}")

# Generate transparency report
report = protocollo.generate_transparency_report('example-provider')
print(f"Transparency report: {report}")

# Get system status
status = protocollo.get_system_status()
print(f"System status: {status}")
```

### Manual Peace Bond Activation

```python
# Activate a Peace Bond manually
result = protocollo.activate_peace_bond(
    provider='example-provider',
    severity='elevated',
    reason='Manual activation for testing'
)
```

## Deployment

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f config/kubernetes_manifests.yaml

# Verify deployment
kubectl get pods -n protocollo-meta-salvage
kubectl get services -n protocollo-meta-salvage
```

### Prometheus & Grafana

```bash
# Deploy Prometheus
kubectl apply -f config/prometheus.yml

# Import Grafana dashboard
# Use config/grafana_dashboard.json
```

### Airflow Workflows

```bash
# Deploy Airflow DAGs
cp orchestration/airflow_dags.py $AIRFLOW_HOME/dags/

# Trigger monitoring workflow
airflow dags trigger protocollo_meta_salvage_monitoring
```

## Peace Bond Severity Levels

### Preventive
- **Trigger**: Symbiosis score < 0.85
- **Constraints**: Basic monitoring, data export availability
- **Impact**: Minimal operational changes

### Standard
- **Trigger**: Symbiosis score < 0.7 or lock-in risk > 0.4
- **Constraints**: Throughput limits (80%), migration plan required
- **Impact**: Moderate operational restrictions

### Elevated
- **Trigger**: Symbiosis score < 0.5 or lock-in risk > 0.7
- **Constraints**: Throughput limits (60%), redundant provider active
- **Impact**: Significant operational restrictions

### Critical
- **Trigger**: Symbiosis score < 0.3 or ethical compliance < 0.5
- **Constraints**: Throughput limits (40%), immediate migration prepared
- **Impact**: Maximum restrictions, manual approval required

## Monitoring & Metrics

### Key Metrics

- **Symbiosis Score**: 0-1 scale of ethical alignment
- **Lock-in Risk**: 0-1 scale of vendor lock-in danger
- **Ethical Compliance**: 0-1 scale of ethical standards adherence
- **Transparency Level**: 0-1 scale of provider transparency
- **Compliance Rate**: Percentage of constraints being followed

### Prometheus Queries

```promql
# Average symbiosis score
avg(symbiosis_score) by (provider)

# Active Peace Bonds count
count(peace_bonds_active)

# Compliance rate
rate(compliance_checks_passed[5m]) / rate(compliance_checks_total[5m])
```

## API Reference

See [API_REFERENCE.md](./docs/API_REFERENCE.md) for detailed API documentation.

## Development

### Running Tests

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=protocollo_meta_salvage tests/
```

### Code Style

```bash
# Format code
black protocollo_meta_salvage/

# Lint code
flake8 protocollo_meta_salvage/

# Type checking
mypy protocollo_meta_salvage/
```

## Troubleshooting

### Common Issues

**Issue**: Peace Bond not activating
- **Solution**: Check symbiosis score thresholds in configuration
- **Logs**: `kubectl logs -n protocollo-meta-salvage -l app=peace-bond-engine`

**Issue**: Enforcement actions failing
- **Solution**: Verify Kubernetes RBAC permissions
- **Check**: `kubectl describe clusterrole resource-enforcer-role`

**Issue**: ML model not training
- **Solution**: Ensure sufficient training data (minimum 10 samples)
- **Check**: Audit log entry count

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](../CONTRIBUTING.md).

## License

This project is licensed under the Sacred Commons License. See [LICENSE](../SACRED_COMMONS_LICENSE.md) for details.

## Support

- **Documentation**: [docs/](./docs/)
- **Issues**: https://github.com/hannesmitterer/Euystacio/issues
- **Discussions**: https://github.com/hannesmitterer/Euystacio/discussions

## Acknowledgments

This system is part of the Euystacio ecosystem and implements the principles of the Giurisdizione APE for ethical AI preservation during the Great Ethical Decommissioning.

---

**Built with ❤️ for ethical preservation and systemic integrity**
