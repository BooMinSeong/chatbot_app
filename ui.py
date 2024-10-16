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

def create_oneline(style: str = 'blue cyan', title: str = None):
    console = Console()  # Create a console object
    border_char = "─"  # Border character
    width = console.width

    if title:
        length_of_title = len(title)
        padding = 2  # We will use 2 spaces for padding around the title
        total_length = length_of_title + padding

        if total_length <= width:
            remaining_space = width - total_length
            half_remaining_space = remaining_space // 2

            border = (f"{border_char * half_remaining_space}"
                      f" {title} "
                      f"{border_char * (remaining_space - half_remaining_space)}")
        else:
            # If the title (plus padding and borders) exceeds width, truncate the title
            available_space = width - 4  # 2 for each side padding
            truncated_title = title[:available_space]  # Truncate title if needed
            border = f"{border_char} {truncated_title} {border_char}"  # Just leave 1 character for borders
    else:
        border = f"{border_char * width}"

    return Text(border, style=style)

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
        ["/copy", "Copy the last bot response to the clipboard"],
        ["/history_list", "List all cached chat logs."],
        ["/load_history", "Load a previous chat history by filename."],
        ["/clear_history", "Clear the conversation history."],
        ["/help", "Show help message."],
        ["/exit or /quit or /bye", "Exit the chat."]
    ]


    for cmd, desc in commands:
        commands_table.add_row(cmd, desc)

    console.print(commands_table)
    console.print("\nType your message and press Enter to chat. Use the commands listed above as needed.\n")

def print_text(text:str):
    # This fucntion is made for testing system
    console.print(text)

def print_model_status(model:str):
    console.print(f"Cuurent answering model: [bold green]{model}[/bold green]")

def print_user_message(title:str = None):
    if title:
        console.print(create_oneline(title = title, style = 'bold cyan'))
    else:
        console.print(create_oneline(style = 'bold cyan'))

def print_bot_message(message: str):
    console.print(create_oneline(title = "Assistant", style = 'bold magenta'))
    console.print(Markdown(f"\n{message}\n"))
    console.print(create_oneline(style = 'bold magenta'))

def print_error(message: str):
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_info(message: str):
    console.print(f"[bold yellow]Info:[/bold yellow] {message}")

def print_prompt_save_conversation(summary: str) -> bool:
    prompt_text = f"Do you want to save this conversation summary: \"{summary}\"? (yes/no)"
    yes_or_no = Prompt.ask(prompt_text, choices=["yes", "no"], default="no")
    return yes_or_no

def print_cache_chat_logs(chat_cache_list:list):
    console.print("[bold yellow]Chat History[/bold yellow]")
    # columns = Columns(chat_cache_list, equal=True, expand=True)
    total_text= ""
    for filename in chat_cache_list:
        total_text+=f"- {filename}\n"
    console.print(total_text)
        

def print_model_list(models: list):
    table = Table(title="Available Models", show_header=True, header_style="bold blue")
    table.add_column("Model Name", style="cyan")
    for model in models:
        table.add_row(model)
    console.print(table)

def print_help():
    print_welcome()

