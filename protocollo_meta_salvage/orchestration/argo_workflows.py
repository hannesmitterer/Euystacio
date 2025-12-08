"""
Argo Workflows Definitions
===========================

Defines Argo Workflows for Kubernetes-native orchestration of Peace Bonds.
"""

from typing import Dict, Any


def create_peace_bond_workflow() -> Dict[str, Any]:
    """
    Create Argo Workflow for Peace Bond activation and enforcement.
    
    This workflow orchestrates the complete Peace Bond lifecycle in Kubernetes.
    
    Returns:
        Argo Workflow specification
    """
    
    workflow_spec = {
        'apiVersion': 'argoproj.io/v1alpha1',
        'kind': 'Workflow',
        'metadata': {
            'name': 'peace-bond-enforcement',
            'namespace': 'protocollo-meta-salvage'
        },
        'spec': {
            'entrypoint': 'peace-bond-pipeline',
            'arguments': {
                'parameters': [
                    {'name': 'provider', 'value': '{{workflow.parameters.provider}}'},
                    {'name': 'severity', 'value': '{{workflow.parameters.severity}}'}
                ]
            },
            'templates': [
                {
                    'name': 'peace-bond-pipeline',
                    'steps': [
                        [
                            {
                                'name': 'monitor',
                                'template': 'monitor-metrics'
                            }
                        ],
                        [
                            {
                                'name': 'decide',
                                'template': 'make-decision'
                            }
                        ],
                        [
                            {
                                'name': 'enforce',
                                'template': 'enforce-constraints',
                                'when': '{{steps.decide.outputs.result}} == "activate"'
                            }
                        ],
                        [
                            {
                                'name': 'audit',
                                'template': 'log-audit'
                            }
                        ]
                    ]
                },
                {
                    'name': 'monitor-metrics',
                    'container': {
                        'image': 'protocollo-meta-salvage:latest',
                        'command': ['python', '-m', 'protocollo_meta_salvage.monitoring'],
                        'args': ['--provider', '{{workflow.parameters.provider}}']
                    }
                },
                {
                    'name': 'make-decision',
                    'container': {
                        'image': 'protocollo-meta-salvage:latest',
                        'command': ['python', '-m', 'protocollo_meta_salvage.decision_engine'],
                        'args': ['--provider', '{{workflow.parameters.provider}}']
                    }
                },
                {
                    'name': 'enforce-constraints',
                    'resource': {
                        'action': 'apply',
                        'manifest': '''
apiVersion: v1
kind: ResourceQuota
metadata:
  name: peace-bond-{{workflow.parameters.provider}}
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 10Gi
    limits.cpu: "20"
    limits.memory: 20Gi
'''
                    }
                },
                {
                    'name': 'log-audit',
                    'container': {
                        'image': 'protocollo-meta-salvage:latest',
                        'command': ['python', '-m', 'protocollo_meta_salvage.audit'],
                        'args': ['--provider', '{{workflow.parameters.provider}}', '--action', 'log']
                    }
                }
            ]
        }
    }
    
    return workflow_spec


def create_compliance_workflow() -> Dict[str, Any]:
    """
    Create Argo Workflow for compliance monitoring.
    
    Returns:
        Argo Workflow specification for compliance checking
    """
    
    workflow_spec = {
        'apiVersion': 'argoproj.io/v1alpha1',
        'kind': 'Workflow',
        'metadata': {
            'name': 'compliance-monitoring',
            'namespace': 'protocollo-meta-salvage'
        },
        'spec': {
            'entrypoint': 'compliance-check',
            'templates': [
                {
                    'name': 'compliance-check',
                    'dag': {
                        'tasks': [
                            {
                                'name': 'check-provider-1',
                                'template': 'check-compliance',
                                'arguments': {
                                    'parameters': [{'name': 'provider', 'value': 'provider-1'}]
                                }
                            },
                            {
                                'name': 'check-provider-2',
                                'template': 'check-compliance',
                                'arguments': {
                                    'parameters': [{'name': 'provider', 'value': 'provider-2'}]
                                }
                            },
                            {
                                'name': 'aggregate-results',
                                'template': 'aggregate',
                                'dependencies': ['check-provider-1', 'check-provider-2']
                            }
                        ]
                    }
                },
                {
                    'name': 'check-compliance',
                    'inputs': {
                        'parameters': [{'name': 'provider'}]
                    },
                    'container': {
                        'image': 'protocollo-meta-salvage:latest',
                        'command': ['python', '-m', 'protocollo_meta_salvage.decision_engine.constraint_manager'],
                        'args': ['--check-compliance', '--provider', '{{inputs.parameters.provider}}']
                    }
                },
                {
                    'name': 'aggregate',
                    'container': {
                        'image': 'protocollo-meta-salvage:latest',
                        'command': ['python', '-m', 'protocollo_meta_salvage.audit'],
                        'args': ['--aggregate-compliance']
                    }
                }
            ]
        }
    }
    
    return workflow_spec
