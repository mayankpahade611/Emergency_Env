from typing import Callable, Dict
from Environment.grader import grade


def create_task(task_id: str, input_data: dict, truth: dict) -> Dict:
    return {
        "id": task_id,
        "input": input_data,
        "truth": truth,
        "grader": lambda action: grade(action, truth)  
    }


TASKS = [

    create_task(
        "easy_fire",
        {
            "text": "There is smoke coming out of my kitchen and it smells like something is burning.",
            "location": "home"
        },
        {
            "type": "fire",
            "severity": "high",
            "actions": ["turn off gas", "evacuate", "call fire department"]
        }
    ),

    create_task(
        "medium_medical",
        {
            "text": "A person has fainted and is not responding.",
            "location": "street"
        },
        {
            "type": "medical",
            "severity": "critical",
            "actions": ["check pulse", "perform CPR", "call ambulance"]
        }
    ),

    create_task(
        "hard_accident",
        {
            "text": "Two cars collided and people are injured.",
            "location": "highway"
        },
        {
            "type": "accident",
            "severity": "critical",
            "actions": ["call ambulance", "control bleeding", "alert police"]
        }
    ),
]