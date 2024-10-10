from typing import List

async def validation_post_prompt(title_text: str) -> List[dict]:

    prompt = [

        {

            "role": "system",
            "content": (f"""You are analyzing a post title or content to identify personal insults, obscene language, and inappropriate criticism. 
            Analyze the following title or content and return only one of the following responses in JSON format. There are only four possible responses, all listed below:
            {{
                "answer": "good"
            }} if no issues are found,
            {{
                "answer": "personal insult"
            }} if a personal insult is detected,
            {{
                "answer": "obscene language"
            }} if obscene language is detected,
            {{
                "answer": "inappropriate criticism"
            }} if inappropriate criticism is detected.
            """)

        },

        {

            "role": "user",
            "content": f"{title_text}"

        },

    ]

    return prompt

async def get_summary_prompt(text: str) -> List[dict]:

    prompt = [

        {

            "role": "system",
            "content": (f"""Please provide a detailed and comprehensive summary of the following text.
            The summary should include all the key points, main ideas, and any important details.
            Ensure that the summary is clear, concise, and captures the essence of the original text.
            Return the summary as a JSON object with a single key 'summary' and the summary text as its value.
            """)

        },

        {

            "role": "user",
            "content": f"{text}"

        },

    ]

    return prompt

