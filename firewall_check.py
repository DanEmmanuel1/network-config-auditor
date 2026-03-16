import subprocess
import psutil
from rich.console import Console
from rich.table import Table

console = Console()

def run_firewall_check():
    console.print("\n[bold cyan]═══ WINDOWS FIREWALL STATUS ═══[/bold cyan]\n")
    _check_firewall()
    _check_active_connections()
    _check_listening_services()

def _check_firewall():
    try:
        result = subprocess.check_output(
            'netsh advfirewall show allprofiles state',
            shell=True
        ).decode(errors="ignore")

        profiles = {"Domain": None, "Private": None, "Public": None}
        current_profile = None

        for line in result.splitlines():
            line = line.strip()
            for profile in profiles:
                if profile in line and "Profile Settings" in line:
                    current_profile = profile
            if current_profile and "State" in line:
                state = line.split()[-1]
                profiles[current_profile] = state
                current_profile = None

        for profile, state in profiles.items():
            if state and state.upper() == "ON":
                console.print(f"[green]✔ {profile} Firewall: ON[/green]")
            elif state and state.upper() == "OFF":
                console.print(f"[red]✘ {profile} Firewall: OFF — RISK! Enable immediately[/red]")
            else:
                console.print(f"[yellow]⚠ {profile} Firewall: Could not determine state[/yellow]")

    except Exception as e:
        console.print(f"[red]Error checking firewall: {e}[/red]")

def _check_active_connections():
    console.print("\n[bold]Active Outbound Connections:[/bold]")
    try:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Local Address", style="cyan", width=25)
        table.add_column("Remote Address", style="yellow", width=25)
        table.add_column("Status", style="green", width=15)
        table.add_column("PID", style="white", width=10)

        connections = psutil.net_connections(kind="inet")
        count = 0
        for conn in connections:
            if conn.status == "ESTABLISHED" and conn.raddr:
                local = f"{conn.laddr.ip}:{conn.laddr.port}"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}"
                table.add_row(local, remote, conn.status, str(conn.pid))
                count += 1
                if count >= 15:
                    break

        if count == 0:
            console.print("[green]✔ No active outbound connections found[/green]")
        else:
            console.print(table)

    except Exception as e:
        console.print(f"[red]Error checking connections: {e}[/red]")

def _check_listening_services():
    console.print("\n[bold]Listening Services (open to incoming connections):[/bold]")
    try:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Address", style="cyan", width=25)
        table.add_column("Port", style="yellow", width=10)
        table.add_column("PID", style="white", width=10)
        table.add_column("Risk", style="red", width=35)

        risky = {
            21: "FTP — unencrypted",
            23: "Telnet — unencrypted",
            135: "RPC — attack vector",
            139: "NetBIOS — legacy",
            445: "SMB — ransomware target",
            3389: "RDP — brute force target",
            5900: "VNC — remote access",
        }

        connections = psutil.net_connections(kind="inet")
        seen = set()
        for conn in connections:
            if conn.status == "LISTEN" and conn.laddr:
                port = conn.laddr.port
                if port in seen:
                    continue
                seen.add(port)
                risk = risky.get(port, "Low risk")
                table.add_row(
                    conn.laddr.ip,
                    str(port),
                    str(conn.pid),
                    risk
                )

        if not seen:
            console.print("[green]✔ No listening services found[/green]")
        else:
            console.print(table)

    except Exception as e:
        console.print(f"[red]Error checking listening services: {e}[/red]")