from rich.console import Console, Group
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.markdown import Markdown
from rich.measure import measure_renderables
from typing import Optional

console = Console()

def create_partial_border(content,style,title:str= None):
    # Define the border characters
    border_char = "─"  # Any character you prefer for the border
    # width = measure_renderables(console,content)
    width = console.width
    wrapped_content = f"\n{content}\n"


    # Create the top and bottom borders
    length_of_title = len(title) if title else 0
    space_for_title = length_of_title+4 # Adding space for borders and padding
    remaining_space = width - space_for_title -2
    half_remaining_space = remaining_space//2

    if title:
        top_border = (f"┌{border_char * half_remaining_space}  "
                      f"{title}  "
                      f"{border_char * (remaining_space - half_remaining_space)}┐")
    else:
        top_border = f"┌{border_char * (width-2)}┐"
    bottom_border = f"└{border_char * (width-2)}┘"

    # Combine the top border, content, and bottom border
    bordered_content = Group(
            Text(top_border, style = style),
            Markdown(wrapped_content),
            Text(bottom_border,style = style),
            )

    return bordered_content


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
    console.print(create_partial_border(message, title = "User", style = 'bold cyan'))

def print_bot_message(message: str):
    console.print(create_partial_border(message, title = "Assistant", style = 'bold magenta'))

def print_error(message: str):
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_info(message: str):
    console.print(f"[bold yellow]Info:[/bold yellow] {message}")

def print_prompt_save_conversation(summary: str) -> bool:
    prompt_text = f"Do you want to save this conversation summary: \"{summary}\"? (yes/no)"
    yes_or_no = Prompt.ask(prompt_text, choices=["yes", "no"], default="no")
    return yes_or_no

def print_cache_chat_logs(chat_list:list):
    columns = Columns(directory, equal=True, expand=True)
    console.print("[bold yellow]Chat History[/bold yellow]")
    console.print(columns)

def print_model_list(models: list):
    table = Table(title="Available Models", show_header=True, header_style="bold blue")
    table.add_column("Model Name", style="cyan")
    for model in models:
        table.add_row(model)
    console.print(table)

def print_help():
    print_welcome()

