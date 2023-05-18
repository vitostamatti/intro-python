import openai  # pip install openai
import typer  # pip install "typer[all]"
from rich import print  # pip install rich
from rich.table import Table
import os


def load_environs(filename):
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            else:
                value = value.strip()
            os.environ[key] = value



def main():
    
    load_environs(".env")

    openai.api_key = os.environ["OPENAI_KEY"]

    print("💬 [bold green]ChatGPT API en Python[/bold green]")

    table = Table("Command", "Description")
    table.add_row("exit", "Exit application")
    table.add_row("new", "Create new conversation")

    print(table)

    # Contexto del asistente
    context = {"role": "system", "content": "You are the best AI assistant to cowork with."}
    messages = [context]

    while True:
        content = __prompt()

        if content == "new":
            print("New conversation created")
            messages = [context]
            content = __prompt()

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold green]assistant: [/bold green] [green]{response_content}[/green]")


def __prompt() -> str:
    prompt = typer.prompt("\nyou")

    if prompt == "exit":
        exit = typer.confirm("Are you sure you want to exit this conversation?")
        if exit:
            raise typer.Abort()

        return __prompt()

    return prompt


if __name__ == "__main__":
    typer.run(main)
