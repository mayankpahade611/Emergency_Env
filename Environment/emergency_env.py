from Environment.models import Observation, Action
from Environment.tasks import TASKS
from Environment.grader import grade


class EmergencyEnv:

    def __init__(self):
        self.index = 0
        self.current = None

    # 🔹 Helper: get current task
    def get_current_task(self):
        return TASKS[self.index]

    # 🔹 Helper: explicit grader per task
    def grade_current_task(self, action: Action):
        task = self.get_current_task()
        return grade(action, task["truth"])

    async def reset(self):
        self.index = 0
        self.current = self.get_current_task()

        return type("Result", (), {
            "observation": Observation(
                incident=self.current["input"]["text"],
                location=self.current["input"]["location"]
            ),
            "done": False
        })

    async def step(self, action: Action):
        
        score = self.grade_current_task(action)

        self.index += 1
        done = self.index >= len(TASKS)

        if not done:
            self.current = self.get_current_task()
            obs = Observation(
                incident=self.current["input"]["text"],
                location=self.current["input"]["location"]
            )
        else:
            obs = Observation(incident="done", location="none")

        return type("Result", (), {
            "observation": obs,
            "reward": score,
            "done": done
        })

    async def close(self):
        pass

    @classmethod
    async def from_docker_image(cls, image_name):
        return cls()