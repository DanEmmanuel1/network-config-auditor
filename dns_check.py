import subprocess
from rich.console import Console

console = Console()

SAFE_DNS = [
    "8.8.8.8", "8.8.4.4",
    "1.1.1.1", "1.0.0.1",
    "9.9.9.9",
    "208.67.222.222",
]

def run_dns_check():
    console.print("\n[bold cyan]═══ DNS & ROUTING CHECK ═══[/bold cyan]\n")
    _check_dns()
    _check_default_gateway()

def _check_dns():
    console.print("[bold]DNS Servers:[/bold]")
    try:
        result = subprocess.check_output("ipconfig /all", shell=True).decode(errors="ignore")
        dns_servers = []
        for line in result.splitlines():
            if "DNS Servers" in line or "DNS Server" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    ip = parts[-1].strip()
                    if ip:
                        dns_servers.append(ip)
        if not dns_servers:
            console.print("[yellow]No DNS servers found[/yellow]")
            return
        for dns in dns_servers:
            if dns in SAFE_DNS:
                console.print(f"[green]✔ {dns} — known safe DNS provider[/green]")
            else:
                console.print(f"[yellow]⚠ {dns} — unknown DNS server (verify this is trusted)[/yellow]")
    except Exception as e:
        console.print(f"[red]Error checking DNS: {e}[/red]")

def _check_default_gateway():
    console.print("\n[bold]Default Gateway:[/bold]")
    try:
        result = subprocess.check_output("ipconfig", shell=True).decode(errors="ignore")
        for line in result.splitlines():
            if "Default Gateway" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    gw = parts[-1].strip()
                    if gw:
                        console.print(f"[green]✔ Gateway: {gw}[/green]")
                        return
        console.print("[yellow]⚠ No default gateway found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error checking gateway: {e}[/red]")
