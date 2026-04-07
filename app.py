from fastapi import FastAPI
from Environment.emergency_env import EmergencyEnv
from Environment.models import Action

app = FastAPI()

envi = EmergencyEnv()


@app.post("/reset")
async def reset():
    result = await envi.reset()
    return {
        "observation": result.observation.dict(),
        "done": result.done
    }


@app.post("/step")
async def step(action: dict):
    act = Action(**action)

    result = await envi.step(act)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done,
        "info": {}
    }


@app.get("/state")
async def state():
    return envi.state()