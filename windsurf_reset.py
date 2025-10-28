import json
import os
import shutil
import uuid
import logging
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.prompt import Confirm, Prompt
from rich.theme import Theme
from rich.layout import Layout
from rich.table import Table
from rich import print as rprint
from rich.style import Style
from rich.text import Text

# Importar sistema de versionamiento
try:
    from version import __version__, __license__, __copyright__
except ImportError:
    __version__ = "2.1.0"  # Actualizado
    __license__ = "MIT"
    __copyright__ = "2024"

# Importar psutil para verificar procesos
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Importar enhanced logger si está disponible
try:
    from enhanced_logger import get_logger, EnhancedLogger
    ENHANCED_LOGGER_AVAILABLE = True
except ImportError:
    ENHANCED_LOGGER_AVAILABLE = False

# --- Import OS-specific modules ---
if platform.system() == "Windows":
    import msvcrt
    import os as win_os
else:
    import tty
    import termios
    import os as unix_os


# --- Set terminal title (cross-platform) ---
def set_terminal_title(title: str):
    """Set the terminal title in a cross-platform way."""
    if platform.system() == "Windows":
        os.system(f"title {title}")
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")
        sys.stdout.flush()


# --- Clear terminal screen (cross-platform) ---
def clear_screen():
    """Clear the terminal screen in a cross-platform way."""
    if platform.system() == "Windows":
        win_os.system("cls")
    else:
        unix_os.system("clear")


# --- Convert HEX color to RGB ---
def hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to RGB format."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r},{g},{b}"


# --- Define custom Rich theme ---
custom_theme = Theme(
    {
        "info": f"bold rgb({hex_to_rgb('#0A4A43')})",
        "warning": f"bold rgb({hex_to_rgb('#158F82')})",
        "error": "bold red",
        "success": f"bold rgb({hex_to_rgb('#21c0ae')})",
        "header": f"bold rgb({hex_to_rgb('#0A4A43')})",
        "prompt": f"bold rgb({hex_to_rgb('#158F82')})",
        "progress.bar": f"rgb({hex_to_rgb('#21c0ae')})",
        "progress.percentage": f"rgb({hex_to_rgb('#0A4A43')})",
        "menu.border": f"rgb({hex_to_rgb('#158F82')})",
        "menu.title": f"bold rgb({hex_to_rgb('#0A4A43')})",
        "dialog.border": f"rgb({hex_to_rgb('#21c0ae')})",
        "dialog.title": f"bold rgb({hex_to_rgb('#0A4A43')})",
    }
)

console = Console(theme=custom_theme)

logging.basicConfig(
    level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# --- Custom exception for Windsurf reset errors ---
class WindsurfResetError(Exception):
    """Custom exception for Windsurf reset-related errors."""

    pass


# --- Check if Windsurf is running ---
def check_windsurf_running() -> list:
    """Check if Windsurf processes are running."""
    if not PSUTIL_AVAILABLE:
        return []
    
    windsurf_processes = []
    process_names = ["Windsurf.exe", "windsurf", "Windsurf", "windsurf.exe"]
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in process_names:
                windsurf_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return windsurf_processes


# --- Kill Windsurf processes ---
def kill_windsurf_processes(processes: list) -> bool:
    """Terminate Windsurf processes."""
    if not processes:
        return True
    
    console.print(f"\n[warning]Found {len(processes)} Windsurf process(es) running.[/warning]")
    
    for proc in processes:
        try:
            console.print(f"[info]Closing process: {proc.info['name']} (PID: {proc.info['pid']})[/info]")
            proc.terminate()
            proc.wait(timeout=5)
            console.print(f"[success]Process {proc.info['pid']} closed successfully.[/success]")
        except psutil.TimeoutExpired:
            console.print(f"[warning]Forcing process {proc.info['pid']} to close...[/warning]")
            try:
                proc.kill()
            except:
                pass
        except Exception as e:
            console.print(f"[warning]Could not close process {proc.info['pid']}: {str(e)}[/warning]")
    
    return True


# --- Display header ---
def display_header():
    """Display header with version and info."""
    message = Text(
        "This tool will reset your Windsurf device identifiers and create a backup of your existing configuration.\n\n"
        f"Version: {__version__} | License: {__license__} | © {__copyright__}\n"
        "Educational Purpose - Use Responsibly",
        justify="center",
    )
    console.print(
        Panel(
            message,
            title=f"🔧 Windsurf Reset Tool v{__version__}",
            border_style="menu.border",
            title_align="center",
            padding=(1, 2),
        )
    )


# --- Display interactive menu ---
def display_menu() -> str:
    menu_items = {
        "1": "Reset device identifiers",
        "2": "View current configuration",
        "3": "Exit",
    }

    menu = Table.grid(padding=2)
    menu.add_column(style="prompt")
    menu.add_column(style="info")

    for key, value in menu_items.items():
        menu.add_row(f"[{key}]", value)

    console.print(Panel(menu, title="Main Menu", border_style="menu.border", padding=(1, 2)))
    console.print("[prompt]Press a key to choose an option[/prompt]")

    while True:
        choice = get_single_keypress()
        if choice in menu_items:
            return choice


# --- Confirmation dialog (y/n) ---
def confirm_action(message: str) -> bool:
    console.print(f"\n[dialog.title]{message} (y/n)[/dialog.title]")
    while True:
        choice = get_single_keypress()
        if choice == "y":
            return True
        elif choice == "n":
            return False


# --- Single keypress input ---
def get_single_keypress() -> str:
    if platform.system() == "Windows":
        return msvcrt.getch().decode("utf-8").lower()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# --- Create backup ---
def backup_file(file_path: Path) -> Optional[Path]:
    try:
        if file_path.exists():
            backup_path = file_path.with_name(
                f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Creating backup...", total=100)
                shutil.copy2(file_path, backup_path)
                progress.update(task, advance=100)

            message = Text(f"Backup created:\n{backup_path}", justify="center")
            console.print(
                Panel(message, title="[+] Backup Created", border_style="success", padding=(1, 2))
            )
            return backup_path
        return None
    except Exception as e:
        raise WindsurfResetError(f"Failed to create backup: {str(e)}") from e


# --- Get Windsurf base directory ---
def get_windsurf_base_path() -> Path:
    """Get the base Windsurf configuration directory."""
    try:
        system = platform.system()
        paths = {
            "Windows": Path(os.getenv("APPDATA", "")),
            "Darwin": Path.home() / "Library" / "Application Support",
            "Linux": Path.home() / ".config",
        }

        base_path = paths.get(system)
        if not base_path:
            supported_os = ", ".join(paths.keys())
            raise WindsurfResetError(
                f"Unsupported OS: {system}. Supported systems: {supported_os}"
            )

        windsurf_path = base_path / "Windsurf"

        if not base_path.exists():
            raise WindsurfResetError(f"Base directory does not exist: {base_path}")
        if not os.access(str(base_path), os.W_OK):
            raise WindsurfResetError(f"No write permission for directory: {base_path}")

        return windsurf_path
    except Exception as e:
        if isinstance(e, WindsurfResetError):
            raise
        raise WindsurfResetError(f"Failed to determine base path: {str(e)}") from e


# --- Get Windsurf storage file path ---
def get_storage_file() -> Path:
    """Get the main storage.json file path."""
    return get_windsurf_base_path() / "User" / "globalStorage" / "storage.json"


# --- Generate new Windsurf device IDs ---
def generate_device_ids() -> Dict[str, str]:
    return {
        "telemetry.machineId": os.urandom(32).hex(),
        "telemetry.macMachineId": os.urandom(32).hex(),
        "telemetry.devDeviceId": str(uuid.uuid4()),
    }


# --- Display device IDs ---
def display_device_ids(ids: Dict[str, str], title: str = "Device Identifiers"):
    table = Table.grid(padding=2)
    table.add_column(style=f"rgb({hex_to_rgb('#0A4A43')})")
    table.add_column(style=f"rgb({hex_to_rgb('#158F82')})")

    filtered_ids = {k: v for k, v in ids.items() if k != "telemetry.sqmId"}

    for key, value in filtered_ids.items():
        table.add_row(f"{key}:", value)

    console.print(Panel(table, title=title, border_style="info", padding=(1, 2)))


# --- Clean authentication and session files ---
def clean_auth_files(base_path: Path, stats: Optional['ResetStatistics'] = None) -> int:
    """Remove authentication, session, and cache files."""
    files_removed = 0
    
    # Archivos y directorios a eliminar para resetear completamente
    paths_to_clean = [
        # Cookies y sesiones
        base_path / "Cookies",
        base_path / "Cookies-journal",
        base_path / "Network Persistent State",
        
        # Cache y datos temporales
        base_path / "Cache",
        base_path / "CachedData",
        base_path / "Code Cache",
        base_path / "GPUCache",
        
        # Sesiones y estado
        base_path / "Session Storage",
        base_path / "Local Storage",
        base_path / "IndexedDB",
        
        # Archivos de estado específicos de Windsurf
        base_path / "User" / "globalStorage" / "codeium.windsurf",
        base_path / "User" / "workspaceStorage",
        
        # Archivos de log que pueden contener tokens
        base_path / "logs",
    ]
    
    for path in paths_to_clean:
        try:
            if path.exists():
                if path.is_file():
                    path.unlink()
                    files_removed += 1
                    if stats:
                        stats.add_file_deleted()
                elif path.is_dir():
                    shutil.rmtree(path)
                    files_removed += 1
                    if stats:
                        stats.add_dir_deleted()
        except Exception as e:
            console.print(f"[warning]Warning: Could not remove {path.name}: {str(e)}[/warning]")
            if stats:
                stats.add_warning()
    
    return files_removed


# --- Statistics tracker ---
class ResetStatistics:
    """Rastrea estadísticas de la operación de reset."""
    
    def __init__(self):
        self.files_deleted = 0
        self.dirs_deleted = 0
        self.errors = 0
        self.warnings = 0
        self.backup_created = False
        self.processes_closed = 0
        self.start_time = datetime.now()
    
    def add_file_deleted(self):
        self.files_deleted += 1
    
    def add_dir_deleted(self):
        self.dirs_deleted += 1
    
    def add_error(self):
        self.errors += 1
    
    def add_warning(self):
        self.warnings += 1
    
    def get_summary(self) -> Dict:
        """Retorna un resumen de las estadísticas."""
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            'files_deleted': self.files_deleted,
            'dirs_deleted': self.dirs_deleted,
            'total_deleted': self.files_deleted + self.dirs_deleted,
            'errors': self.errors,
            'warnings': self.warnings,
            'backup_created': self.backup_created,
            'processes_closed': self.processes_closed,
            'duration_seconds': duration
        }


# --- Reset Windsurf device IDs and authentication ---
def reset_windsurf_id() -> bool:
    stats = ResetStatistics()
    
    try:
        # Verificar si Windsurf está en ejecución
        running_processes = check_windsurf_running()
        
        if running_processes:
            warning_message = Text(
                f"⚠️  Windsurf is currently running ({len(running_processes)} process(es) detected).\n\n"
                "The reset will not work properly if Windsurf is open.",
                justify="center"
            )
            console.print(
                Panel(
                    warning_message,
                    title="[!] Warning - Windsurf Running",
                    border_style="warning",
                    padding=(1, 2),
                )
            )
            
            if PSUTIL_AVAILABLE:
                if confirm_action("Would you like to automatically close Windsurf processes?"):
                    kill_windsurf_processes(running_processes)
                    stats.processes_closed = len(running_processes)
                    console.print("[success]Windsurf processes have been closed.[/success]\n")
                else:
                    error_message = Text(
                        "Please close Windsurf manually and run this tool again.",
                        justify="center"
                    )
                    console.print(
                        Panel(
                            error_message,
                            title="[x] Cannot Continue",
                            border_style="error",
                            padding=(1, 2),
                        )
                    )
                    return False
            else:
                console.print(
                    "[warning]Install 'psutil' to automatically close Windsurf: pip install psutil[/warning]"
                )
                if not confirm_action("Continue anyway? (Not recommended)"):
                    return False
        
        storage_file = get_storage_file()
        base_path = get_windsurf_base_path()

        if storage_file.exists():
            if confirm_action("Would you like to create a backup before continuing?"):
                backup_file(storage_file)
                stats.backup_created = True
            else:
                warning_message = Text("Continuing without creating a backup", justify="center")
                console.print(
                    Panel(
                        warning_message,
                        title="[!] Warning",
                        border_style="warning",
                        padding=(1, 2),
                    )
                )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            total_steps = 7
            current_step = 0

            task = progress.add_task("🔍 Locating configuration files...", total=total_steps)
            current_step += 1
            progress.update(task, completed=current_step)

            progress.update(task, description="🧹 Cleaning authentication and session files...")
            files_removed = clean_auth_files(base_path, stats)
            current_step += 1
            progress.update(task, completed=current_step)
            console.print(f"[info]Removed {files_removed} cache/session files[/info]")

            progress.update(task, description="📁 Creating directories if missing...")
            storage_file.parent.mkdir(parents=True, exist_ok=True)
            current_step += 1
            progress.update(task, completed=current_step)

            progress.update(task, description="📖 Loading configuration...")
            data = {}
            if storage_file.exists():
                try:
                    with open(storage_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    warning_message = Text(
                        "Invalid JSON format in config file. Creating a new configuration.",
                        justify="center",
                    )
                    console.print(
                        Panel(
                            warning_message,
                            title="[!] Warning",
                            border_style="warning",
                            padding=(1, 2),
                        )
                    )
            current_step += 1
            progress.update(task, completed=current_step)

            progress.update(task, description="🔄 Generating new identifiers...")
            new_ids = generate_device_ids()
            
            # Eliminar todas las claves relacionadas con telemetría y autenticación
            keys_to_remove = [
                k for k in data.keys() 
                if k.startswith(('telemetry', 'codeium', 'windsurf', 'auth', 'session'))
            ]
            for key in keys_to_remove:
                del data[key]
            
            # Agregar los nuevos IDs
            data.update(new_ids)
            current_step += 1
            progress.update(task, completed=current_step)

            progress.update(task, description="💾 Saving updated configuration...")
            with open(storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            current_step += 1
            progress.update(task, completed=current_step)
            
            progress.update(task, description="✅ Finalizing reset...")
            current_step += 1
            progress.update(task, completed=current_step)

        success_message = Text(
            "Device identifiers and authentication have been successfully reset!\n\n"
            "IMPORTANT: You must RESTART Windsurf completely for changes to take effect.",
            justify="center"
        )
        console.print(Panel(success_message, title="Success", border_style="success", padding=(1, 2)))

        display_device_ids(new_ids, "New Device Identifiers")
        
        # Mostrar estadísticas
        summary = stats.get_summary()
        console.print("\n" + "="*60)
        console.print("[bold cyan]📊 ESTADÍSTICAS DE LA OPERACIÓN[/bold cyan]")
        console.print("="*60)
        
        stats_table = Table.grid(padding=1)
        stats_table.add_column(style="cyan")
        stats_table.add_column(style="green")
        
        stats_table.add_row("⏱️  Duración:", f"{summary['duration_seconds']:.2f} segundos")
        stats_table.add_row("📁 Archivos eliminados:", str(summary['files_deleted']))
        stats_table.add_row("📂 Directorios eliminados:", str(summary['dirs_deleted']))
        stats_table.add_row("📦 Total eliminado:", str(summary['total_deleted']))
        stats_table.add_row("🔒 Backup creado:", "Sí" if summary['backup_created'] else "No")
        stats_table.add_row("🚫 Procesos cerrados:", str(summary['processes_closed']))
        stats_table.add_row("⚠️  Advertencias:", str(summary['warnings']))
        stats_table.add_row("❌ Errores:", str(summary['errors']))
        
        console.print(stats_table)
        console.print("="*60 + "\n")
        
        return True

    except WindsurfResetError as e:
        error_message = Text(f"Reset error: {str(e)}", justify="center")
        console.print(Panel(error_message, title="[x] Error", border_style="error", padding=(1, 2)))
        raise
    except Exception as e:
        error_message = Text(f"Unexpected error: {str(e)}", justify="center")
        console.print(Panel(error_message, title="[x] Error", border_style="error", padding=(1, 2)))
        raise WindsurfResetError(f"Failed to reset Windsurf identifiers: {str(e)}") from e


# --- View current configuration ---
def view_current_config():
    try:
        storage_file = get_storage_file()
        if storage_file.exists():
            with open(storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                display_device_ids(
                    {k: v for k, v in data.items() if k.startswith("telemetry")},
                    "Current Device Identifiers",
                )
        else:
            info_message = Text("Configuration file not found", justify="center")
            console.print(Panel(info_message, title="[i] Info", border_style="info", padding=(1, 2)))
    except Exception as e:
        error_message = Text(f"Failed to read configuration: {str(e)}", justify="center")
        console.print(Panel(error_message, title="[x] Error", border_style="error", padding=(1, 2)))


# --- Main Entry Point ---
if __name__ == "__main__":
    try:
        set_terminal_title("Windsurf Reset Tool v1.0")
        clear_screen()
        while True:
            display_header()
            choice = display_menu()

            if choice == "1":
                if confirm_action("Are you sure you want to reset the device identifiers?"):
                    reset_windsurf_id()
            elif choice == "2":
                view_current_config()
            else:
                goodbye_message = Text("Windsurf Reset Tool closed. (Sparki boost)", justify="center")
                console.print(Panel(goodbye_message, title="[-] Goodbye", border_style="info", padding=(1, 2)))
                break

            if choice != "3":
                if not confirm_action("Would you like to perform another operation?"):
                    goodbye_message = Text(
                        "Thank you for using the Windsurf Device ID Reset Tool!", justify="center"
                    )
                    console.print(
                        Panel(goodbye_message, title="[-] Goodbye", border_style="info", padding=(1, 2))
                    )
                    break

    except WindsurfResetError as e:
        error_message = Text(f"Error: {str(e)}", justify="center")
        console.print(Panel(error_message, title="[x] Error", border_style="error", padding=(1, 2)))
        exit(1)
    except KeyboardInterrupt:
        warning_message = Text("Operation cancelled by user", justify="center")
        console.print(Panel(warning_message, title="[!] Warning", border_style="warning", padding=(1, 2)))
        exit(1)
