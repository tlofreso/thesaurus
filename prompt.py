from rich import print
from openai import Client
from time import sleep
import json, os

def use_thesaurus(word):

    ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
    THESAURUS_PROMPT = f"""Respond with three synonyms for "{word}". Your response should be a valid JSON array. Every object in the array represents a synonym paired with its definition.

    ###Example Response###

    [
      {{
        "synonym": "arrogant",
        "definition": "having or revealing an exaggerated sense of one's own importance or abilities."
      }}
    ]
    """
    client = Client()
    assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id = thread.id,
        content=THESAURUS_PROMPT,
        role="user"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while run.status in ["queued", "in_progress", "cancelling"]:
        sleep(2)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    client.beta.threads.delete(thread.id)

    response_string = messages.data[0].content[0].text.value
    json_str = response_string[response_string.find("[") : response_string.rfind("]") + 1]
    response_json = json.loads(json_str)

    return response_json

if __name__ == "__main__":
    response = use_thesaurus("test")
    print(response)