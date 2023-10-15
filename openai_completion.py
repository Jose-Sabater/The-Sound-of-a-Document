import os
import openai
from typing import List, Dict
import logging
import time
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAIAssistant:
    def __init__(self, model: str, **kwargs):
        self.model = model

    def get_openai_completion(
        self,
        system_message: str,
        user_messages: List[str],
        assistant_messages: List[str],
        max_retries: int = 4,
    ) -> Dict:
        """Invoke OpenAI's ChatCompletion with the provided messages."""
        messages = [
            {"role": "system", "content": f"{system_message}"},
            *self.user_assistant_message(user_messages, assistant_messages),
        ]

        for retry in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                )
                return response

            except Exception as e:
                if retry < max_retries - 1:  # if it's not the last retry
                    logging.warning(
                        f"Attempt {retry + 1} failed invoking OpenAI's ChatCompletion. Retrying..."
                    )
                    time.sleep(2)  # wait for some time before retrying

                else:
                    logging.error(
                        f"Error invoking OpenAI's ChatCompletion after {max_retries} attempts: {e}"
                    )
                    raise e  # Re-raise the exception after logging the error

    @staticmethod
    def user_assistant_message(
        user_messages: List[str], assistant_messages: List[str]
    ) -> List[Dict[str, str]]:
        """Returns a list of dictionaries of the user and assistant messages."""
        user_assistant_messages = []
        assistant_count = len(assistant_messages)

        # Iterate over all user messages
        for i, user_message in enumerate(user_messages):
            user_assistant_messages.append(
                {"role": "user", "content": f"{user_message}"}
            )

            # Only add an assistant message if one exists for the current user message
            if i < assistant_count:
                assistant_message = assistant_messages[i]
                user_assistant_messages.append(
                    {"role": "assistant", "content": f"{assistant_message}"}
                )

        return user_assistant_messages
