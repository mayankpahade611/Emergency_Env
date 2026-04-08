from fastapi import FastAPI
from Environment.emergency_env import EmergencyEnv
from Environment.models import Action
import uvicorn

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


@app.get("/")
async def root():
    return {"message": "Emergency OpenEnv API running"}


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()