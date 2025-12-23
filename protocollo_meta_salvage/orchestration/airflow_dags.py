"""
Apache Airflow DAG Definitions
===============================

Defines DAGs for automated workflows in the Protocollo Meta Salvage system.
"""

from typing import Dict, Any


def create_monitoring_dag() -> Dict[str, Any]:
    """
    Create Apache Airflow DAG for continuous monitoring.
    
    This DAG runs periodically to:
    - Collect metrics from providers
    - Analyze symbiosis scores
    - Check triggers
    - Activate Peace Bonds if needed
    
    Returns:
        DAG configuration dictionary
    """
    
    dag_config = {
        'dag_id': 'protocollo_meta_salvage_monitoring',
        'description': 'Continuous monitoring for ethical preservation',
        'schedule_interval': '*/15 * * * *',  # Every 15 minutes
        'default_args': {
            'owner': 'protocollo_meta_salvage',
            'depends_on_past': False,
            'retries': 3,
            'retry_delay': '5m'
        },
        'tasks': [
            {
                'task_id': 'collect_metrics',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.monitoring.collect_all_metrics',
                'op_kwargs': {}
            },
            {
                'task_id': 'analyze_scores',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.monitoring.analyze_symbiosis_scores',
                'op_kwargs': {}
            },
            {
                'task_id': 'check_triggers',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.monitoring.check_all_triggers',
                'op_kwargs': {}
            },
            {
                'task_id': 'evaluate_decisions',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.decision_engine.evaluate_all_situations',
                'op_kwargs': {},
                'trigger_rule': 'all_success'
            }
        ],
        'task_dependencies': [
            'collect_metrics >> analyze_scores >> check_triggers >> evaluate_decisions'
        ]
    }
    
    return dag_config


def create_enforcement_dag() -> Dict[str, Any]:
    """
    Create Apache Airflow DAG for Peace Bond enforcement.
    
    This DAG handles:
    - Enforcing Peace Bond constraints
    - Monitoring compliance
    - Handling violations
    - Updating audit logs
    
    Returns:
        DAG configuration dictionary
    """
    
    dag_config = {
        'dag_id': 'protocollo_meta_salvage_enforcement',
        'description': 'Peace Bond enforcement and compliance monitoring',
        'schedule_interval': '*/30 * * * *',  # Every 30 minutes
        'default_args': {
            'owner': 'protocollo_meta_salvage',
            'depends_on_past': False,
            'retries': 2,
            'retry_delay': '10m'
        },
        'tasks': [
            {
                'task_id': 'enforce_active_bonds',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.automation.enforce_all_active_bonds',
                'op_kwargs': {}
            },
            {
                'task_id': 'check_compliance',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.decision_engine.check_all_compliance',
                'op_kwargs': {}
            },
            {
                'task_id': 'handle_violations',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.decision_engine.handle_violations',
                'op_kwargs': {},
                'trigger_rule': 'all_done'
            },
            {
                'task_id': 'update_audit_logs',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.audit.finalize_audit_logs',
                'op_kwargs': {}
            }
        ],
        'task_dependencies': [
            'enforce_active_bonds >> check_compliance >> handle_violations >> update_audit_logs'
        ]
    }
    
    return dag_config


def create_feedback_dag() -> Dict[str, Any]:
    """
    Create Apache Airflow DAG for ML feedback loop.
    
    This DAG runs daily to:
    - Collect audit data
    - Prepare training data
    - Retrain ML models
    - Analyze improvements
    
    Returns:
        DAG configuration dictionary
    """
    
    dag_config = {
        'dag_id': 'protocollo_meta_salvage_feedback',
        'description': 'ML feedback loop and continuous improvement',
        'schedule_interval': '0 2 * * *',  # Daily at 2 AM
        'default_args': {
            'owner': 'protocollo_meta_salvage',
            'depends_on_past': True,
            'retries': 1,
            'retry_delay': '1h'
        },
        'tasks': [
            {
                'task_id': 'collect_audit_data',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.feedback.collect_recent_audit_data',
                'op_kwargs': {'hours': 24}
            },
            {
                'task_id': 'prepare_training_data',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.feedback.prepare_training_data',
                'op_kwargs': {}
            },
            {
                'task_id': 'train_ml_model',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.feedback.train_model',
                'op_kwargs': {}
            },
            {
                'task_id': 'analyze_improvements',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.feedback.analyze_improvements',
                'op_kwargs': {}
            },
            {
                'task_id': 'publish_model',
                'operator': 'PythonOperator',
                'python_callable': 'protocollo_meta_salvage.feedback.publish_model_version',
                'op_kwargs': {}
            }
        ],
        'task_dependencies': [
            'collect_audit_data >> prepare_training_data >> train_ml_model >> analyze_improvements >> publish_model'
        ]
    }
    
    return dag_config
