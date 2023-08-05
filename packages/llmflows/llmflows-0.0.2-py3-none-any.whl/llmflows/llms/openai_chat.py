"""
This module provides interaction with the OpenAI chat API via OpenAIChat.
"""

import os
from typing import List, Dict
import openai
from .llm import BaseLLM


class OpenAIChat(BaseLLM):
    """
    A class for interacting with the OpenAI chat API.

    Args:
        system_prompt (str): The initial prompt to send to the chat API.
        model (str): The name of the OpenAI model to use.
        verbose (bool): Whether to print debug information.

    Attributes:
        api_key (str): The API key to use for authentication.
        model (str): The name of the OpenAI model to use.
        messages (List[Dict[str, str]]): A list of messages sent to the chat API.
        temperature (float): The temperature to use for text generation.
        verbose (bool): Whether to print debug information.

    Methods:
        add_message(message_str: str, role: str = "user") -> List[Dict[str, str]]:
            Adds a message to the list of messages sent to the chat API.
        replace_message(new_message, idx=-2):
            Replaces a message in the list of messages sent to the chat API.
        remove_message(idx=-1):
            Removes a message from the list of messages sent to the chat API.
        update_system_prompt(new_prompt: str) -> None:
            Updates the system prompt sent to the chat API.
        chat() -> str:
            Sends the messages to the OpenAI chat API and returns the response.
    """

    def __init__(
        self,
        system_prompt: str = "",
        model: str = "gpt-3.5-turbo",
        verobse: bool = False,
    ):
        super().__init__(model)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        self.temperature = 0.7
        self.verbose = verobse

    def add_message(self, message_str: str, role: str = "user") -> List[Dict[str, str]]:
        """
        Adds a message to the list of messages sent to the chat API.

        Args:
            message_str (str): The message to add.
            role (str): The role of the message (either "user" or "assistant").

        Returns:
            The updated list of messages.
        """

        self.messages.append({"role": role, "content": message_str})
        return self.messages

    def replace_message(self, new_message, idx=-2):
        """
        Replaces a message in the list of messages sent to the chat API.

        Args:
            new_message: The new message to replace the old message with.
            idx (int): The index of the message to replace.
        """
        self.messages[idx] = new_message

    def remove_message(self, idx=-1):
        """
        Removes a message from the list of messages sent to the chat API.

        Args:
            idx (int): The index of the message to remove.
        """
        self.messages.pop(idx)

    def update_system_prompt(self, new_prompt: str) -> None:
        """
        Updates the system prompt sent to the chat API.

        Args:
            new_prompt (str): The new system prompt.
        """
        self.messages[0] = {"role": "system", "content": new_prompt}

    def chat(self) -> str:
        """
        Sends the messages to the OpenAI chat API and returns the response.

        Returns:
            The response from the OpenAI chat API.
        """
        if self.verbose:
            print("[SYSTEM] printing messages")
            for msg in self.messages:
                print(msg)
            print("--------")
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )

        self.add_message(response.choices[0].message.content, "assistant")

        return self.messages[-1]["content"]
