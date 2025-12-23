# Protocollo Meta Salvage - Peace Bonds Policy Tests
# OPA test suite for Peace Bonds policies

package peace_bonds

# Test: Allow when symbiosis score is above threshold and no violations
test_allow_high_symbiosis_score {
    allow with input as {
        "symbiosis_score": 0.85,
        "violations": [],
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
}

# Test: Deny when symbiosis score is below threshold
test_deny_low_symbiosis_score {
    not allow with input as {
        "symbiosis_score": 0.60,
        "violations": [],
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
}

# Test: Symbiosis risk level calculation - low risk
test_symbiosis_risk_level_low {
    symbiosis_risk_level == "low" with input as {
        "symbiosis_score": 0.85
    }
}

# Test: Symbiosis risk level calculation - medium risk
test_symbiosis_risk_level_medium {
    symbiosis_risk_level == "medium" with input as {
        "symbiosis_score": 0.65
    }
}

# Test: Symbiosis risk level calculation - high risk
test_symbiosis_risk_level_high {
    symbiosis_risk_level == "high" with input as {
        "symbiosis_score": 0.40
    }
}

# Test: Detect low symbiosis score violation
test_detect_symbiosis_violation {
    violations := detected_violations with input as {
        "symbiosis_score": 0.60,
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    count(violations) > 0
    violations[_].type == "symbiosis_score_low"
}

# Test: Detect unauthorized access violation
test_detect_unauthorized_access {
    violations := detected_violations with input as {
        "symbiosis_score": 0.85,
        "user": {"id": "unknown-user", "role": "guest"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    count([v | v := violations[_]; v.type == "unauthorized_access"]) > 0
}

# Test: Detect resource abuse violation
test_detect_resource_abuse {
    violations := detected_violations with input as {
        "symbiosis_score": 0.85,
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 150,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    count([v | v := violations[_]; v.type == "resource_abuse"]) > 0
}

# Test: Detect anomalous behavior violation
test_detect_anomalous_behavior {
    violations := detected_violations with input as {
        "symbiosis_score": 0.85,
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": true
    }
    count([v | v := violations[_]; v.type == "anomalous_behavior"]) > 0
}

# Test: Authorized user with valid ID
test_authorized_user_by_id {
    is_authorized_user with input as {
        "user": {"id": "user-001"}
    }
    with data.authorized_users as {"user-001", "user-002"}
}

# Test: Authorized user with admin role
test_authorized_user_by_role {
    is_authorized_user with input as {
        "user": {"id": "unknown", "role": "admin"}
    }
}

# Test: Calculate overall risk - critical
test_calculate_overall_risk_critical {
    risk := calculate_overall_risk with input as {
        "symbiosis_score": 0.85,
        "user": {"id": "unknown-user", "role": "guest"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    risk == "critical"
}

# Test: Calculate overall risk - high
test_calculate_overall_risk_high {
    risk := calculate_overall_risk with input as {
        "symbiosis_score": 0.40,
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    risk == "high"
}

# Test: Calculate overall risk - low
test_calculate_overall_risk_low {
    risk := calculate_overall_risk with input as {
        "symbiosis_score": 0.85,
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    risk == "low"
}

# Test: Generate recommendations for violations
test_generate_recommendations {
    recommendations := generate_recommendations with input as {
        "symbiosis_score": 0.60,
        "user": {"id": "user-001", "role": "trusted_agent"},
        "resource_usage": 50,
        "resource_limit": 100,
        "anomaly_detected": false
    }
    count(recommendations) > 0
}
