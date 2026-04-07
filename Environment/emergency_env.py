from Environment.models import Observation, Action
from Environment.tasks import SCENARIOS
from Environment.grader import grade

class EmergencyEnv:

    def __init__(self):
        self.index = 0
        self.current = None

    async def reset(self):
        self.index = 0
        self.current = SCENARIOS[self.index]

        return type("Result", (), {
            "observation": Observation(
                incident=self.current["input"]["text"],
                location=self.current["input"]["location"]
            ),
            "done": False
        })

    async def step(self, action: Action):
        truth = self.current["truth"]

        score = grade(action, truth)

        self.index += 1
        done = self.index >= len(SCENARIOS)

        if not done:
            self.current = SCENARIOS[self.index]
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