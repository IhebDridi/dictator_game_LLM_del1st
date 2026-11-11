import openai
import json
import time
import settings


class ChatGPTAssistant:
    def __init__(self):
        """Initializes the ChatGPT assistant with instructions from a file."""
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.openai_model
        self.assistant_id = None
        self.thread_id = None

        self.instructions = self.load_instructions(settings.instructions_path)

        self.create_or_load_assistant()

    def load_instructions(self, file_path):
        """Reads the assistant's instructions from a file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            print('Could not find instructions file')
            return "You are a helpful AI assistant."

    def create_or_load_assistant(self):
        """Creates an OpenAI assistant if it doesn't already exist."""
        if self.assistant_id:
            return self.assistant_id

        assistant = openai.beta.assistants.create(
            name="Dictator Game Assistant",
            instructions=self.instructions,
            model=self.model,
        )

        self.assistant_id = assistant.id
        print(f"✅ Assistant Created: {self.assistant_id}")
        return self.assistant_id

    def create_thread(self):
        """Creates a new thread to maintain conversation memory."""
        if self.thread_id:
            return self.thread_id

        thread = openai.beta.threads.create()
        self.thread_id = thread.id
        print(f"✅ New Thread Created: {self.thread_id}")
        return self.thread_id

    def send_message(self, user_message):
        """Sends a user message and gets a response from the assistant."""
        self.create_thread()

        openai.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=user_message
        )
        assistant = openai.beta.assistants.retrieve(self.assistant_id)
        print("✅ Assistant Instructions:", assistant.instructions)
        run = openai.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )

        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run.id)
            if run_status.status == "completed":
                messages = openai.beta.threads.messages.list(thread_id=self.thread_id)
                return messages.data[0].content[0].text.value

