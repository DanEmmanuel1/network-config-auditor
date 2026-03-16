import os
from rich.console import Console

console = Console()

def run_ssh_audit():
    console.print("\n[bold cyan]═══ SSH AUDITOR ═══[/bold cyan]")

    ssh_config_paths = [
        "C:\\ProgramData\\ssh\\sshd_config",
        os.path.expanduser("~\\.ssh\\config"),
    ]

    found = False
    for path in ssh_config_paths:
        if os.path.exists(path):
            found = True
            console.print(f"[yellow]Found SSH config at:[/yellow] {path}\n")
            _analyze_ssh_config(path)

    if not found:
        console.print("[yellow]⚠ No SSH config file found on this machine.[/yellow]")
        console.print("[green]✔ This likely means SSH server is not installed — low risk.[/green]")

def _analyze_ssh_config(path):
    checks = {
        "PermitRootLogin": {"safe": "no", "found": None},
        "PasswordAuthentication": {"safe": "no", "found": None},
        "PermitEmptyPasswords": {"safe": "no", "found": None},
        "Protocol": {"safe": "2", "found": None},
        "MaxAuthTries": {"safe": "3", "found": None},
    }

    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line and " " not in line:
                    continue
                for key in checks:
                    if line.lower().startswith(key.lower()):
                        parts = line.split()
                        if len(parts) >= 2:
                            checks[key]["found"] = parts[1]

        for key, val in checks.items():
            found_val = val["found"]
            safe_val = val["safe"]
            if found_val is None:
                console.print(f"[yellow]⚠ {key}: not set (recommend setting to '{safe_val}')[/yellow]")
            elif found_val.lower() == safe_val.lower():
                console.print(f"[green]✔ {key}: {found_val} (secure)[/green]")
            else:
                console.print(f"[red]✘ {key}: {found_val} (RISK — recommended: '{safe_val}')[/red]")

    except Exception as e:
        console.print(f"[red]Could not read SSH config: {e}[/red]")