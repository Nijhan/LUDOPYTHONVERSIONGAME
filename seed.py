from rich.console import Console
from rich.table import Table

console = Console()

# Print styled text
console.print("Hello [bold magenta]World[/bold magenta]!", style="bold green")

# Create a table
table = Table(title="Demo Table")
table.add_column("Name", style="cyan")
table.add_column("Age", style="red")

table.add_row("Alice", "24")
table.add_row("Bob", "30")

console.print(table)