import os
import sys
from chatbot import ChatBot
from dotenv import load_dotenv
from ui import (
    print_welcome,
    print_user_message,
    print_bot_message,
    print_error,
    print_info,
    prompt_save_conversation,
    print_model_list,
    print_help,
    print_model_status
)

from rich.console import Console
import sys

def del_cached_chatlog():
    pass

def load_cached_chatlog():
    pass

def save_data(chat_history: str, filename: str):
    # change to prompt toolkit?
    """Saves the chat history to a file."""
    save_path = os.getenv('SAVE_PATH')
    if not save_path:
        print_error("SAVE_PATH environment variable not set.")
        return

    file_path = os.path.join(save_path, f'{filename}.txt')
    try:
        with open(file_path, 'w') as file:
            file.write(chat_history)
        print_info(f"Chat history saved to {file_path}.")
    except Exception as e:
        print_error(f"Failed to save chat history: {e}")

def multi_line_input(prompt_text):
    print_user_message(title = 'User')
    print(f"{prompt_text} (Press Ctrl+D to submit input or Ctrl+Z on Windows)")
    print("You:")
    lines = sys.stdin.read()  # Reads until EOF (Ctrl+D or Ctrl+Z)
    print_user_message()
    return lines.strip()

def main():
    # Load environment variables
    load_dotenv()
    console = Console()

    # Initialize the chatbot (API key is fetched from the environment variable)
    try:
        bot = ChatBot(api_key=os.getenv('OPENAI_API_KEY'))
    except ValueError as ve:
        print_error(str(ve))
        return

    # Welcome message and commands
    print_welcome()

    while True:
        print_model_status(bot.model)
        user_input = multi_line_input("Ask your question.")

        if not user_input.strip():
            continue  # Ignore empty inputs

        # Check for commands (prefix with '/')
        if user_input.startswith('/'):
            command_parts = user_input.split()
            command = command_parts[0].lower()

            if command in ['/exit', '/quit', '/bye']:
                print_bot_message("Goodbye!")
                break

            elif command == '/change_model':
                if len(command_parts) < 2:
                    print_error("Please specify the model name. Usage: /change_model <model_name>")
                    continue
                new_model = command_parts[1]
                bot.set_model(new_model)
                print_info(f"Model has been changed to '{new_model}'.")
                continue

            elif command == '/model_list':
                available_models = ['gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini']
                print_model_list(available_models)
                continue

            elif command == '/undo':
                bot.remove_last_interaction()
                print_info("Last interaction has been removed from history.")
                continue

            elif command == '/clear_history':
                bot.clear_history()
                print_info("Conversation history has been cleared.")
                continue

            elif command == '/help':
                print_help()
                continue

            else:
                print_error("Unknown command. Type /help for a list of available commands.")
                continue

        else:
            # Regular user message
            # print_user_message()
            with console.status("[bold green]Working on tasks...") as status:
                response = bot.send_message(user_input)
            print_bot_message(response)

    print("---" * 8)
    print("| End of Conversation |")
    print("---" * 8)

    # Optionally, save the conversation history
    try:
        summary_prompt = "Think deeply about the conversation and give it an appropriate title. The title should be short and concise, replace the spaces with '_'."
        summary = bot.send_message(summary_prompt)
        if prompt_save_conversation(summary):
            save_data(bot.get_history(), summary)
    except Exception as e:
        print_error(f"An error occurred while summarizing: {e}")

if __name__ == "__main__":
    main()

