def normalize(text: str) -> str:
    return text.lower().strip()


# Synonym mapping for better matching
SYNONYMS = {
    "call ambulance": ["call 911", "call emergency services", "call help"],
    "call fire department": ["call firefighters", "call emergency services"],
    "control bleeding": ["stop bleeding", "apply pressure", "administer first aid"],
    "check pulse": ["check breathing", "check responsiveness"],
    "evacuate": ["leave the area", "get out", "evacuate immediately"],
    "alert police": ["call police", "inform police"]
}


def match_action(predicted: str, correct_actions: set) -> bool:
    predicted = normalize(predicted)

    # Direct match
    if predicted in correct_actions:
        return True

    # Synonym match
    for key, values in SYNONYMS.items():
        if predicted in values and key in correct_actions:
            return True

    return False


def grade(action, truth):
    score = 0.0

    # -------------------------
    # 🔹 TYPE MATCH (0.3)
    # -------------------------
    if normalize(action.type) == normalize(truth["type"]):
        score += 0.3

    # -------------------------
    # 🔹 SEVERITY MATCH (0.3)
    # (allow slight flexibility)
    # -------------------------
    pred_sev = normalize(action.severity)
    true_sev = normalize(truth["severity"])

    if pred_sev == true_sev:
        score += 0.3
    elif pred_sev in ["high", "critical"] and true_sev in ["high", "critical"]:
        score += 0.2  # partial credit

    # -------------------------
    # 🔹 ACTION MATCH (0.4)
    # -------------------------
    correct = set(normalize(a) for a in truth["actions"])
    predicted = set(normalize(a) for a in action.actions)

    matched = 0

    for p in predicted:
        if match_action(p, correct):
            matched += 1

    if len(correct) > 0:
        overlap = matched / len(correct)
        score += 0.4 * overlap

    # -------------------------
    # 🔹 PENALTY (optional)
    # -------------------------
    if action.type == "unknown":
        score -= 0.1

    # Clamp score
    return max(0.0, min(score, 1.0))