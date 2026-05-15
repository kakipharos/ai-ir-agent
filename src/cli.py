import typer
from rich.console import Console
from .agent import IRAgent
from .retrieval import DocumentIndex

app = typer.Typer()
console = Console()

@app.command()
def index():
    """Build or rebuild the local document index."""
    idx = DocumentIndex()
    result = idx.build()
    console.print(f"[green]Indexed {result['chunks']} chunks.[/green]")
    console.print(f"Embedding index used: {result['used_embeddings']}")

@app.command()
def chat():
    """Start the CLI AI IR Agent."""
    agent = IRAgent()
    console.print("[bold green]AI IR Agent started.[/bold green]")
    console.print("Commands: /exit, /debug on, /debug off, /memory <text>")

    while True:
        query = console.input("\n[bold blue]You:[/bold blue] ").strip()
        if not query:
            continue
        if query == "/exit":
            break
        if query == "/debug on":
            agent.debug = True
            console.print("[yellow]Debug mode on.[/yellow]")
            continue
        if query == "/debug off":
            agent.debug = False
            console.print("[yellow]Debug mode off.[/yellow]")
            continue
        if query.startswith("/memory "):
            text = query.replace("/memory ", "", 1).strip()
            agent.memory.add(text)
            console.print(f"[green]Saved memory:[/green] {text}")
            continue

        try:
            answer = agent.answer(query)
            console.print(f"\n[bold green]Agent:[/bold green] {answer}")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    app()
