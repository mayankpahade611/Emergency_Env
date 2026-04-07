import asyncio
import os
import json
import re
from dotenv import load_dotenv
from typing import List, Optional
from openai import OpenAI

from Environment.emergency_env import EmergencyEnv
from Environment.models import Action

load_dotenv()

API_KEY = os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL","https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME","Qwen/Qwen2.5-72B-Instruct")

MAX_STEPS = 3


def log_start(task: str, envi: str, model: str):
    print(f"[START] task={task} envi={envi} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


def get_model_response(client, incident):
    prompt = f"""
You are an expert emergency response AI.

Analyze the situation carefully and respond accurately.

Instructions:
1. Identify the emergency type:
   - fire
   - medical
   - crime
   - accident

2. Determine severity:
   - low (minor issue)
   - medium (needs attention)
   - high (serious danger)
   - critical (life-threatening)

3. Suggest realistic emergency actions.

Important Guidelines:
- Fire incidents → usually HIGH or CRITICAL
- Unconscious person → CRITICAL
- Accidents with injuries → CRITICAL
- Use standard emergency terms like:
  - "call ambulance"
  - "call fire department"
  - "control bleeding"
  - "check pulse"
  - "evacuate"

Return ONLY valid JSON. No explanation.

Format:
{{
  "type": "...",
  "severity": "...",
  "actions": ["...", "..."]
}}

Incident:
{incident}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()


async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    envi = await EmergencyEnv.from_docker_image(None)

    rewards = []
    steps_taken = 0

    log_start(task="emergency", envi="emergency_env", model=MODEL_NAME)

    result = await envi.reset()

    for step in range(1, MAX_STEPS + 1):
        if result.done:
            break

        incident = result.observation.incident

        raw = get_model_response(client, incident)

        match = re.search(r"\{.*\}", raw, re.DOTALL)

        if match:
            raw_json = match.group(0)
        else:
            raw_json = raw

        try:
            parsed = json.loads(raw)
        except:
            parsed = {"type": "unknown", "severity": "low", "actions": []}

        action = Action(**parsed)

        result = await envi.step(action)

        reward = result.reward or 0.0
        done = result.done

        rewards.append(reward)
        steps_taken = step

        log_step(step, str(parsed), reward, done, None)

        if done:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = score > 0.5

    await envi.close()

    log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())