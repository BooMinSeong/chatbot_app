from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from typing import Optional

console = Console()

def print_welcome():
    welcome_text = Text("Welcome to the ", style="bold cyan") + Text("ChatBot!", style="bold magenta")
    console.print(Panel(welcome_text, expand=False, style="bold green"))

    commands_table = Table(title="Available Commands", show_header=True, header_style="bold blue")
    commands_table.add_column("Command", style="cyan", no_wrap=True)
    commands_table.add_column("Description", style="magenta")

    commands = [
        ["/change_model <model_name>", "Change the AI model."],
        ["/model_list", "List the available models."],
        ["/undo", "Remove the last interaction."],
        ["/clear_history", "Clear the conversation history."],
        ["/help", "Show help message."],
        ["/exit or /quit or /bye", "Exit the chat."]
    ]

    for cmd, desc in commands:
        commands_table.add_row(cmd, desc)

    console.print(commands_table)
    console.print("\nType your message and press Enter to chat. Use the commands listed above as needed.\n")

def print_model_status(model:str):
    console.print(f"Cuurent answering model: [bold green]{model}[/bold green]")

def print_user_message(message: str):
    # user_text = Text("You: ", style="bold cyan") + Text(message, style="white")
    user_text = message
    user_text = Markdown(user_text)
    console.print(Panel(user_text, title="User", border_style="cyan"))

def print_bot_message(message: str):
    # bot_text = Text("ChatBot: ", style="bold magenta") + Text(message, style="white")
    bot_text = message
    bot_text = Markdown(bot_text)
    console.print(Panel(bot_text, title="Assistant", border_style="magenta"))

def print_error(message: str):
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_info(message: str):
    console.print(f"[bold yellow]Info:[/bold yellow] {message}")

def prompt_save_conversation(summary: str) -> bool:
    prompt_text = f"Do you want to save this conversation summary: \"{summary}\"? (yes/no)"
    return Prompt.ask(prompt_text, choices=["yes", "no"], default="no").lower() == "yes"

def print_model_list(models: list):
    table = Table(title="Available Models", show_header=True, header_style="bold blue")
    table.add_column("Model Name", style="cyan")
    for model in models:
        table.add_row(model)
    console.print(table)

def print_help():
    print_welcome()

