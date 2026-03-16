import nmap
from rich.console import Console
from rich.table import Table

console = Console()

def run_port_scan(target="127.0.0.1"):
    console.print("\n[bold cyan]═══ PORT SCANNER ═══[/bold cyan]")
    console.print(f"[yellow]Scanning target:[/yellow] {target}\n")

    scanner = nmap.PortScanner()

    try:
        scanner.scan(target, '1-1024', '-T4')
    except Exception as e:
        console.print(f"[red]Error running scan: {e}[/red]")
        console.print("[red]Make sure Nmap is installed and you are running as Administrator.[/red]")
        return

    table = Table(title="Open Ports", show_header=True, header_style="bold magenta")
    table.add_column("Port", style="cyan", width=10)
    table.add_column("State", style="green", width=10)
    table.add_column("Service", style="yellow", width=20)
    table.add_column("Risk", style="red", width=30)

    risky_ports = {
        21: "FTP - unencrypted file transfer",
        22: "SSH - ensure strong auth",
        23: "Telnet - completely unencrypted",
        80: "HTTP - unencrypted web traffic",
        135: "RPC - common attack vector",
        139: "NetBIOS - legacy, often exploited",
        443: "HTTPS - generally safe",
        445: "SMB - ransomware target",
        3389: "RDP - brute force target",
    }

    found_open = False
    for host in scanner.all_hosts():
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in sorted(ports):
                state = scanner[host][proto][port]['state']
                service = scanner[host][proto][port]['name']
                risk = risky_ports.get(port, "Low risk")
                if state == 'open':
                    found_open = True
                    table.add_row(str(port), state, service, risk)

    if found_open:
        console.print(table)
    else:
        console.print("[green]✔ No open ports found in range 1-1024[/green]")