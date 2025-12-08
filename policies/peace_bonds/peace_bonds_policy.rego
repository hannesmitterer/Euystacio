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
    violations := [v |
        violation_check := violation_checks[_]
        violation_check.condition
        v := {
            "type": violation_check.type,
            "severity": violation_check.severity,
            "message": violation_check.message
        }
    ]
}

# Violation check definitions
violation_checks := [
    {
        "type": "symbiosis_score_low",
        "condition": input.symbiosis_score < 0.75,
        "severity": "high",
        "message": "Symbiosis Score below acceptable threshold"
    },
    {
        "type": "unauthorized_access",
        "condition": not is_authorized_user,
        "severity": "critical",
        "message": "Unauthorized access attempt detected"
    },
    {
        "type": "resource_abuse",
        "condition": input.resource_usage > input.resource_limit,
        "severity": "medium",
        "message": "Resource usage exceeds allocated limit"
    },
    {
        "type": "anomalous_behavior",
        "condition": input.anomaly_detected == true,
        "severity": "high",
        "message": "Anomalous behavior pattern detected"
    }
]

# Check if user is authorized
is_authorized_user if {
    input.user.id in data.authorized_users
}

is_authorized_user if {
    input.user.role in {"admin", "operator", "trusted_agent"}
}

# Generate recommendations based on violations
generate_recommendations := recommendations if {
    recommendations := [r |
        violation := detected_violations[_]
        recommendation := violation_recommendations[violation.type]
        r := recommendation
    ]
}

# Recommendations for each violation type
violation_recommendations := {
    "symbiosis_score_low": "Increase symbiosis score through positive interactions and trust-building activities",
    "unauthorized_access": "Verify user credentials and permissions before granting access",
    "resource_abuse": "Reduce resource consumption or request additional allocation",
    "anomalous_behavior": "Investigate the source of anomalous behavior and take corrective action",
    "policy_bypass_attempt": "Review security policies and strengthen access controls"
}

# Test data for authorized users (in production, this would come from external data)
authorized_users := {
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
