from openai import OpenAI
import os
import dynamo

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)


def handle_response(thread_id: str, content: str) -> str:
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=os.environ.get("OPENAI_ASSISTANTS_ID"),
        max_completion_tokens=128
    )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            run_id=run.id
        )

        message = messages.data[0].content[0].text.value
        print(f"Message: {message}")

        return message
    
    if run.status == "incomplete":
        guild_id = dynamo.get_guild_id_by_thread_id(thread_id)
        new_thread_id = create_thread().id

        dynamo.remove_thread_id(guild_id)
        dynamo.insert_thread_id(guild_id, new_thread_id)

        print("Conversation has been reset automatically after completion token limit has reached.")


def create_thread():
    thread = client.beta.threads.create()
    return thread