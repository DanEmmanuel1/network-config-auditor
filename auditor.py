import sys
from rich.console import Console
from rich.panel import Panel
from port_scanner import run_port_scan
from ssh_auditor import run_ssh_audit
from interface_check import run_interface_check
from dns_check import run_dns_check
from firewall_check import run_firewall_check

console = Console()

def print_banner():
    console.print(Panel.fit(
        "[bold cyan]Network Config Auditor[/bold cyan]\n"
        "[yellow]Version 2.0 — Free & Open Source[/yellow]\n"
        "[white]Auditing: Ports | SSH | Interfaces | DNS | Firewall[/white]",
        border_style="cyan"
    ))

def main():
    print_banner()

    target = "127.0.0.1"
    if len(sys.argv) > 1:
        target = sys.argv[1]

    console.print(f"\n[bold white]Target:[/bold white] [cyan]{target}[/cyan]")
    console.print("[bold white]Starting full audit...[/bold white]\n")

    run_port_scan(target)
    run_ssh_audit()
    run_interface_check()
    run_dns_check()
    run_firewall_check()

    console.print("\n[bold green]═══ AUDIT COMPLETE ═══[/bold green]\n")

if __name__ == "__main__":
    main()