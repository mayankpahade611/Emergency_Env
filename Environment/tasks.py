from typing import List, Dict


TASKS = [
    {
        "id": "easy_fire",
        "input": {
            "text": "There is smoke coming out of my kitchen and it smells like something is burning.",
            "location": "home"
        },
        "truth": {
            "type": "fire",
            "severity": "high",
            "actions": [
                "turn off gas",
                "evacuate",
                "call fire department"
            ]
        }
    },
    {
        "id": "medium_medical",
        "input": {
            "text": "A person has fainted and is not responding.",
            "location": "street"
        },
        "truth": {
            "type": "medical",
            "severity": "critical",
            "actions": [
                "check pulse",
                "perform CPR",
                "call ambulance"
            ]
        }
    },
    {
        "id": "hard_accident",
        "input": {
            "text": "Two cars collided and people are injured.",
            "location": "highway"
        },
        "truth": {
            "type": "accident",
            "severity": "critical",
            "actions": [
                "call ambulance",
                "control bleeding",
                "alert police"
            ]
        }
    }
]