import sys
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from port_scanner import run_port_scan
from ssh_auditor import run_ssh_audit
from interface_check import run_interface_check
from dns_check import run_dns_check
from firewall_check import run_firewall_check

console = Console()

REPORT_FILE = "network_report.txt"

def print_banner():
    console.print(Panel.fit(
        "[bold cyan]Network Config Auditor[/bold cyan]\n"
        "[yellow]Version 2.0 — Free & Open Source[/yellow]\n"
        "[white]Auditing: Ports | SSH | Interfaces | DNS | Firewall[/white]",
        border_style="cyan"
    ))

def save_report(target, findings):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("=" * 60)
    lines.append(f"Network Config Audit Report")
    lines.append(f"Generated:  {now}")
    lines.append(f"Target:     {target}")
    lines.append("=" * 60)
    lines.append("")
    for item in findings:
        lines.append(f"  {item}")
    lines.append("")
    lines.append("=" * 60)

    with open(REPORT_FILE, "a", encoding="utf-8", errors="replace") as f:
        f.write("\n".join(lines) + "\n")

    console.print(f"[green]✔ Report saved to {REPORT_FILE}[/green]")

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

    # Save report
    findings = [
        f"Target scanned: {target}",
        "Modules run: Port Scanner, SSH Auditor, Interface Check, DNS Check, Firewall Check",
        f"Audit completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "See terminal output above for full details",
    ]
    save_report(target, findings)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")