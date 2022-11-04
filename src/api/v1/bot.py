import asyncio
import json

import requests
from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from config import llm_settings
from schemas import UserRequest


router = APIRouter()


@router.post("/chat", response_model=str)
async def chat(request: Request, data: UserRequest):
    bot = request.app.state.bot
    endpoint = llm_settings.llm_endpoint
    request_data = bot["generate_parameters"]

    request_data["prompt"] = f"{bot['prompt']}\n\n{bot['human']}: {data.message}\n{bot['bot']}:"
    try:
        res = requests.post(
            f"{endpoint}/generate",
            headers={"Content-Type": "application/json", "accept": "application/json"},
            data=json.dumps(request_data),
        )
    except Exception as e:
        logger.error(f"Request Error :{e}")
        raise HTTPException(500, "Server Request Error")
    if res.status_code == 200:
        task_id = res.json()["task_id"]
        logger.info(f"TaskID: {task_id}")
        for i in range(300):
            logger.info(f"Try ({i + 1}/300)")
            res = requests.get(
                f"{endpoint}/result/{task_id}",
                headers={
                    "accept": "application/json",
                },
            )
            if res.status_code == 200 and res.json()["status"] == "completed":
                result = res.json()["result"][0][len(request_data["prompt"]) :]
                ret_text = ""
                for i in range(0, len(result)):
                    if (
                        result[i] == "\n"
                        or result[i:].startswith(f"{bot['human']}:")
                        or result[i:].startswith(f"{bot['bot']}:")
                    ):
                        break
                    ret_text += result[i]
                ret_text = ret_text.strip()
                return ret_text
            await asyncio.sleep(1)
        raise HTTPException(500, "Server Error")
    else:
        logger.error(f"{res.text}")
        raise HTTPException(500, "Server Error")
