from openai import OpenAI
import os

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)


async def handle_response(thread_id: str, content: str) -> str:
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=os.environ.get("OPENAI_ASSISTANTS_ID"),
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            run_id=run.id
        )
        return messages.data[0].content[0].text.value


async def create_thread():
    thread = client.beta.threads.create()
    return thread