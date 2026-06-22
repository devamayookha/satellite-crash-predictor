"""
risk_logic.py - Satellite Collision Risk Assessor
Simplified heuristic scoring. NOT a physics simulation.
"""

# Miss distance thresholds (km)
MISS_DIST_HIGH   = 1.0
MISS_DIST_MEDIUM = 5.0
MISS_DIST_LOW    = 10.0

# Relative velocity thresholds (km/s)
VEL_HIGH   = 10.0
VEL_MEDIUM = 5.0

# Size category scores
SIZE_SCORES = {
    "debris":          20,
    "cubesat":         12,
    "large satellite": 20,
}

# Score thresholds for risk levels
THRESHOLD_HIGH   = 70
THRESHOLD_MEDIUM = 40

# Time thresholds (hours) for urgency escalation
TIME_URGENT      = 6
TIME_VERY_URGENT = 2


def _score_miss_distance(miss_km):
    if miss_km <= MISS_DIST_HIGH:
        return 50, f"the predicted miss distance is critically small ({miss_km} km)"
    elif miss_km <= MISS_DIST_MEDIUM:
        points = int(50 - ((miss_km - MISS_DIST_HIGH) / (MISS_DIST_MEDIUM - MISS_DIST_HIGH)) * 30)
        return points, f"the predicted miss distance is small ({miss_km} km)"
    elif miss_km <= MISS_DIST_LOW:
        points = int(20 - ((miss_km - MISS_DIST_MEDIUM) / (MISS_DIST_LOW - MISS_DIST_MEDIUM)) * 20)
        return points, f"the miss distance is moderate ({miss_km} km)"
    else:
        return 0, f"the miss distance is large ({miss_km} km), reducing collision concern"


def _score_velocity(vel_kms):
    if vel_kms >= VEL_HIGH:
        return 30, f"the relative velocity is very high ({vel_kms} km/s)"
    elif vel_kms >= VEL_MEDIUM:
        points = int(15 + ((vel_kms - VEL_MEDIUM) / (VEL_HIGH - VEL_MEDIUM)) * 15)
        return points, f"the relative velocity is significant ({vel_kms} km/s)"
    else:
        points = int((vel_kms / VEL_MEDIUM) * 15)
        return points, f"the relative velocity is low ({vel_kms} km/s)"


def _score_size(category):
    key = category.strip().lower()
    points = SIZE_SCORES.get(key, 10)
    fragments = {
        "debris":          "the object is classified as debris (high tracking uncertainty)",
        "cubesat":         "the object is a CubeSat (moderate size and cross-section)",
        "large satellite": "the object is a large satellite (significant physical cross-section)",
    }
    explanation = fragments.get(key, f"the object category '{category}' has moderate risk weighting")
    return points, explanation


def _altitude_note(alt1_km, alt2_km):
    diff = abs(alt1_km - alt2_km)
    if diff < 10:
        return (f"Both objects orbit at nearly the same altitude "
                f"({alt1_km} km and {alt2_km} km), meaning repeated conjunctions are possible.")
    elif diff < 50:
        return f"The objects orbit at close but distinct altitudes ({alt1_km} km and {alt2_km} km)."
    else:
        return (f"The objects orbit at significantly different altitudes "
                f"({alt1_km} km and {alt2_km} km); this is likely a crossing geometry.")


def _determine_action(risk_level, time_hours):
    base_actions = {
        "Low":    "Monitor",
        "Medium": "Prepare maneuver",
        "High":   "Immediate maneuver",
    }
    action = base_actions[risk_level]

    if time_hours <= TIME_VERY_URGENT:
        if risk_level == "Low":
            action = "Prepare maneuver"
        else:
            action = "Immediate maneuver"
    elif time_hours <= TIME_URGENT:
        if risk_level == "Low":
            action = "Monitor (closely)"
        elif risk_level == "Medium":
            action = "Immediate maneuver"

    return action


def assess_risk(altitude_obj1_km, altitude_obj2_km, relative_velocity_kms,
                miss_distance_km, object_size_category, time_to_closest_approach_hours):

    dist_score,  dist_note  = _score_miss_distance(miss_distance_km)
    vel_score,   vel_note   = _score_velocity(relative_velocity_kms)
    size_score,  size_note  = _score_size(object_size_category)
    alt_note                = _altitude_note(altitude_obj1_km, altitude_obj2_km)

    total_score = dist_score + vel_score + size_score

    if total_score >= THRESHOLD_HIGH:
        risk_level = "High"
    elif total_score >= THRESHOLD_MEDIUM:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    action = _determine_action(risk_level, time_to_closest_approach_hours)

    explanation = (
        f"Risk score: {total_score}/100 ({risk_level}). "
        f"The primary factors are: {dist_note}; {vel_note}; and {size_note}. "
        f"{alt_note} "
        f"Time to closest approach is {time_to_closest_approach_hours} hours."
    )

    if time_to_closest_approach_hours <= TIME_URGENT and risk_level != "High":
        explanation += (
            f" Note: the short time window ({time_to_closest_approach_hours} h) "
            f"has escalated the recommended action beyond what the risk score alone would suggest."
        )

    return {
        "risk_level":  risk_level,
        "risk_score":  total_score,
        "action":      action,
        "explanation": explanation,
    }


if __name__ == "__main__":
    result = assess_risk(
        altitude_obj1_km=400,
        altitude_obj2_km=405,
        relative_velocity_kms=7.0,
        miss_distance_km=3.0,
        object_size_category="CubeSat",
        time_to_closest_approach_hours=24,
    )
    print("Risk Level :", result["risk_level"])
    print("Score      :", result["risk_score"])
    print("Action     :", result["action"])
    print("Explanation:", result["explanation"])