import openai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from os.path import join, dirname


class ChatBot:
    """
    A chatbot class that interfaces with OpenAI's API to handle conversations.
    It maintains conversation history to preserve context across multiple API calls.
    """

    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: str = "gpt-4o-mini", 
        max_history_length: int = 20
    ):
        """
        Initializes the ChatBot with the provided API key and model.

        :param api_key: Your OpenAI API key. If not provided, it will be fetched from the
                        'OPENAI_API_KEY' environment variable.
        :param model: The OpenAI model to use for generating responses.
        :param max_history_length: The maximum number of messages to retain in history.
        """
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or via the OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.model = model
        self.max_history_length = max_history_length
        self.system_prompt = [{"role":"system", "content": "You are a helpful assistant"}]
        self.chat_history: List[Dict[str, str]] = []



    def send_message(self, user_input: str, model: Optional[str] = None) -> str:
        """
        Sends a user message to the OpenAI API and returns the chatbot's response.

        :param user_input: The input message from the user.
        :param model: (Optional) The model to use for this specific message.
        :return: The chatbot's response.
        """
        # Append the user message to the history
        self.chat_history.append({"role": "user", "content": user_input})
        self._enforce_history_limit()
        # Change the model if the model value was given

        if model:
            self.set_model(model)

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=self._format_system_prompt(),
            )
            # Extract the assistant's reply
            assistant_message = response.choices[0].message.content.strip()
            # Append the assistant's reply to the history
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            self._enforce_history_limit()
            return assistant_message

        except openai.error.OpenAIError as e:
            # Handle API errors gracefully
            print(f"An error occurred: {e}")
            return "I'm sorry, but I'm unable to process your request at the moment."


    def clear_history(self):
        """
        Clears the conversation history.
        """
        self.chat_history = []

    def _enforce_history_limit(self):
        """
        Ensures that the chat history does not exceed the maximum allowed length.
        This helps manage the token usage and maintain performance.
        """
        if len(self.chat_history) > self.max_history_length:
            # Remove the oldest messages to maintain the limit
            excess = len(self.chat_history) - self.max_history_length
            self.chat_history = self.chat_history[excess:]

    def set_model(self, model: str):
        """
        Updates the model used for generating responses.

        :param model: The new OpenAI model to use.
        """
        self.model = model

    def set_max_history_length(self, max_length: int):
        """
        Updates the maximum history length.

        :param max_length: The new maximum number of messages to retain in history.
        """
        self.max_history_length = max_length
        self._enforce_history_limit()

    def remove_last_interaction(self):
        """
        Removes the last user message and the corresponding assistant reply from the history.
        """
        if len(self.chat_history) >= 2:
            # Remove assistant message
            removed_assistant = self.chat_history.pop()
            # Remove user message
            removed_user = self.chat_history.pop()
            print("Last interaction removed from history.")
        else:
            print("No interaction to remove.")
    def _detach_system_prompt(self):
        return self.chat_history[1:]

    def _attach_system_prompt(self):
        return self.system_prompt+self.chat_history

    def _format_system_prompt(self):
        if self.model.lower().startswith('o1'):
            return self.chat_history
        else:
            return self._attach_system_prompt()

    def set_system_prompt(self,prompt):
        self.system_prompt = [{"role": 'system', 'content': prompt}]


    def get_history(self) -> str:
        """
        Returns a string representation of the conversation history.

        :return: A formatted string of the chat history.
        """
        history_str = ""
        for message in self.chat_history[:-1]: # remove final summary
            role = "User" if message["role"] == "user" else "Assistant"
            history_str += f"**{role}**: \n{message['content']}\n\n"
        return history_str.strip()
