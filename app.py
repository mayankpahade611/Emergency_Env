from fastapi import FastAPI
from env.emergency_env import EmergencyEnv
from env.models import Action

app = FastAPI()

env = EmergencyEnv()


@app.post("/reset")
async def reset():
    result = await env.reset()
    return {
        "observation": result.observation.dict(),
        "done": result.done
    }


@app.post("/step")
async def step(action: dict):
    act = Action(**action)

    result = await env.step(act)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done,
        "info": {}
    }


@app.get("/state")
async def state():
    return env.state()