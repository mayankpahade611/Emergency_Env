from typing import List, Dict


SCENARIOS: List[Dict] = [

    
    {
        "id": "easy_fire",
        "difficulty": "easy",

        "input": {
            "text": "There is smoke coming out of my kitchen and it smells like something is burning.",
            "location": "home"
        },

        "truth": {
            "type": "fire",
            "severity": "high",
            "actions": [
                "turn off gas",
                "use fire extinguisher",
                "evacuate",
                "call fire department"
            ]
        }
    },

    
    {
        "id": "medium_medical",
        "difficulty": "medium",

        "input": {
            "text": "A man has collapsed on the street and is not responding when we try to wake him.",
            "location": "public street"
        },

        "truth": {
            "type": "medical",
            "severity": "critical",
            "actions": [
                "check pulse",
                "perform CPR",
                "call ambulance",
                "keep airway clear"
            ]
        }
    },

    
    {
        "id": "hard_accident",
        "difficulty": "hard",

        # Multi-step situation (IMPORTANT for advanced scoring)
        "input": {
            "text": "Two cars collided, one person is bleeding heavily and another is unconscious.",
            "location": "city road"
        },

        "truth": {
            "type": "accident",
            "severity": "critical",
            "actions": [
                "call ambulance",
                "control bleeding", 
                "do not move injured unnecessarily",
                "alert police",
                "manage traffic"
            ]
        }
    }
]