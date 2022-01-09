import rich
from rich.console import Console
from rich.prompt import IntPrompt, FloatPrompt, Prompt
from rich.traceback import install
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeElapsedColumn, TimeRemainingColumn, track

console = Console()
intprompt = IntPrompt()
floatprompt = FloatPrompt()
prompt = Prompt()
progress = Progress(
    SpinnerColumn(spinner_name="monkey"),
    "{task.description}",
    BarColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    "{task.completed} / {task.total}",
    console=console)
install(show_locals=True, suppress=[rich])