"""
🎨 rich_format.py

Funciones auxiliares para imprimir mensajes estilizados en consola usando Rich.
Estas utilidades permiten centralizar la estética de logs importantes, como la
inicialización de bases de datos, mensajes de éxito, error o advertencia.
"""

# ─────────────────
# 📦 Importaciones
# ─────────────────

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.text import Text

# 🏗️  Módulos internos de la aplicación
from .validators import is_list_of_tuples_with_n_elements

# Forzar salida con colores incluso en entornos como contenedores Docker
console = Console(force_terminal=True)

def print_panel(
    title: str,
    messages: list[str] | list[tuple],
    border_style: str = "bold green",
    style: str | None  = None,
) -> None:
    """
    Imprime un panel estilizado en consola con Rich.

    Args:
        title (str): Título del panel.
        messages (list[str] | list[tuple]): Lista de mensajes.
        border_style (str): Estilo del borde del panel.
        style (str, optional): Estilo del mensaje, ej. "check arrow".

    Returns:
        None
    """
    def render_panel(lines: list[str]) -> None:
        print() # Salto de línea para separar el panel
        console.print(
            Panel.fit(
                "\n".join(lines),
                title=f"[bold green]{title}[/bold green]",
                border_style=border_style,
                title_align="center",
            )
        )

    # Generar los mensajes a mostrar según el estilo
    if style == "check arrow" and is_list_of_tuples_with_n_elements(messages, 2):
        lines = [
            f"[bold green]✔[/bold green] [cyan]{key}[/cyan] → [bold]{value}[/bold]"
            for key, value in messages  # type: ignore
        ]
    else:
        lines = [str(m) for m in messages]

    render_panel(lines)

def print_success_message(message:str, success: bool = True) -> None:
    """
    Imprime un mensaje de éxito o error en la consola.
    """
    if success:
        message = Text(f"✔ {message}", style="bold green")
    else:
        message = Text(f"❌ {message}", style="bold red")

    console.print(message)