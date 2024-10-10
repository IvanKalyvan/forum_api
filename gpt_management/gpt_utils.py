import aiohttp
import asyncio
import os
import sys

from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(root_dir)

from config import openai_key, openai_organization
from .prompt_utils import validation_post_prompt, get_summary_prompt

async def create_tasks_for_gpt(params: List[dict]) -> List:

    tasks = []

    for param in params:

        for item in param.items():

            if item[0] == "text":

                tasks.append(get_summary_prompt(item[1]))

            else:

                tasks.append(validation_post_prompt(item[1]))

    results = await asyncio.gather(*tasks)
    del tasks[::]

    for result in results:

        tasks.append(get_completion({

            "model": "gpt-3.5-turbo-1106",
            "messages": result,
            "temperature": 0.01

        }))

    return await asyncio.gather(*tasks)

async def get_completion(json: dict):

    async with(aiohttp.ClientSession()) as session:

        headers = {

            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}",
            "OpenAI-Organization": f"{openai_organization}"

        }

        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json, ssl=False) as resp:

            response_json = await resp.json()

            result = response_json["choices"][0]["message"]["content"]

            return eval(result)
