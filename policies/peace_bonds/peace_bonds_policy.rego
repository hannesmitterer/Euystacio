# Protocollo Meta Salvage - Peace Bonds Policy
# Open Policy Agent (OPA) policy for enforcing Peace Bonds

package peace_bonds

import future.keywords.if
import future.keywords.in

# Default deny
default allow = false

# Peace Bonds violation categories
violation_categories := {
    "symbiosis_score_low",
    "unauthorized_access",
    "resource_abuse",
    "policy_bypass_attempt",
    "anomalous_behavior"
}

# Symbiosis Score threshold enforcement
allow if {
    input.symbiosis_score >= 0.75
    not has_active_violations
}

# Check for active violations
has_active_violations if {
    count(input.violations) > 0
}

# Evaluate symbiosis score risk level
symbiosis_risk_level := level if {
    score := input.symbiosis_score
    score >= 0.75
    level := "low"
} else := level if {
    score := input.symbiosis_score
    score >= 0.50
    score < 0.75
    level := "medium"
} else := level if {
    level := "high"
}

# Peace Bonds enforcement rules
enforce_peace_bonds := result if {
    result := {
        "allowed": allow,
        "risk_level": symbiosis_risk_level,
        "violations": detected_violations,
        "recommendations": generate_recommendations
    }
}

# Detect violations based on input data
detected_violations := violations if {
    violations := array.concat(
        symbiosis_violations,
        array.concat(auth_violations, array.concat(resource_violations, anomaly_violations))
    )
}

# Symbiosis score violations
symbiosis_violations := [v] if {
    input.symbiosis_score < 0.75
    v := {
        "type": "symbiosis_score_low",
        "severity": "high",
        "message": "Symbiosis Score below acceptable threshold"
    }
} else := []

# Authorization violations
auth_violations := [v] if {
    not is_authorized_user
    v := {
        "type": "unauthorized_access",
        "severity": "critical",
        "message": "Unauthorized access attempt detected"
    }
} else := []

# Resource abuse violations
resource_violations := [v] if {
    input.resource_usage > input.resource_limit
    v := {
        "type": "resource_abuse",
        "severity": "medium",
        "message": "Resource usage exceeds allocated limit"
    }
} else := []

# Anomaly detection violations
anomaly_violations := [v] if {
    input.anomaly_detected == true
    v := {
        "type": "anomalous_behavior",
        "severity": "high",
        "message": "Anomalous behavior pattern detected"
    }
} else := []

# Check if user is authorized
is_authorized_user if {
    input.user.id in data.authorized_users
}

is_authorized_user if {
    input.user.role in {"admin", "operator", "trusted_agent"}
}

# Generate recommendations based on violations
generate_recommendations := recommendations if {
    recommendations := [recommendation |
        violation := detected_violations[_]
        recommendation := get_recommendation(violation.type)
    ]
}

# Get recommendation for violation type
get_recommendation(violation_type) := recommendation if {
    violation_type == "symbiosis_score_low"
    recommendation := "Increase symbiosis score through positive interactions and trust-building activities"
} else := recommendation if {
    violation_type == "unauthorized_access"
    recommendation := "Verify user credentials and permissions before granting access"
} else := recommendation if {
    violation_type == "resource_abuse"
    recommendation := "Reduce resource consumption or request additional allocation"
} else := recommendation if {
    violation_type == "anomalous_behavior"
    recommendation := "Investigate the source of anomalous behavior and take corrective action"
} else := recommendation if {
    violation_type == "policy_bypass_attempt"
    recommendation := "Review security policies and strengthen access controls"
} else := "Review and correct the violation"

# SECURITY NOTE: This is test/example data only
# In production, authorized users MUST be loaded from external data source:
# Example: opa run --set-file data.authorized_users=authorized_users.json
# The data.authorized_users reference should replace this hardcoded set
authorized_users := data.authorized_users_override {
    data.authorized_users_override
} else := {
    "user-001",
    "user-002",
    "admin-001"
}

# Risk assessment for Peace Bonds
risk_assessment := assessment if {
    assessment := {
        "overall_risk": calculate_overall_risk,
        "symbiosis_score": input.symbiosis_score,
        "violation_count": count(detected_violations),
        "critical_violations": count([v | v := detected_violations[_]; v.severity == "critical"]),
        "high_violations": count([v | v := detected_violations[_]; v.severity == "high"]),
        "medium_violations": count([v | v := detected_violations[_]; v.severity == "medium"])
    }
}

# Calculate overall risk based on violations and symbiosis score
calculate_overall_risk := risk if {
    critical_count := count([v | v := detected_violations[_]; v.severity == "critical"])
    critical_count > 0
    risk := "critical"
} else := risk if {
    high_count := count([v | v := detected_violations[_]; v.severity == "high"])
    high_count > 2
    risk := "high"
} else := risk if {
    input.symbiosis_score < 0.5
    risk := "high"
} else := risk if {
    input.symbiosis_score < 0.75
    risk := "medium"
} else := risk if {
    risk := "low"
}
