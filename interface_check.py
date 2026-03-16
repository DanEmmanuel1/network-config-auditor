import psutil
from rich.console import Console
from rich.table import Table

console = Console()

def run_interface_check():
    console.print("\n[bold cyan]═══ NETWORK INTERFACES ═══[/bold cyan]\n")

    table = Table(title="Network Interfaces", show_header=True, header_style="bold magenta")
    table.add_column("Interface", style="cyan", width=20)
    table.add_column("IP Address", style="yellow", width=20)
    table.add_column("Status", style="green", width=10)
    table.add_column("Notes", style="red", width=35)

    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()

    for iface, stat in stats.items():
        ip = "N/A"
        if iface in addrs:
            for addr in addrs[iface]:
                if addr.family.name == "AF_INET":
                    ip = addr.address

        status = "UP" if stat.isup else "DOWN"
        notes = []

        if ip.startswith("169.254"):
            notes.append("APIPA — no DHCP response")
        if ip == "127.0.0.1":
            notes.append("Loopback — normal")
        if stat.isup and ip == "N/A":
            notes.append("Active but no IPv4 assigned")
        if not stat.isup:
            notes.append("Interface is down")

        note_str = ", ".join(notes) if notes else "OK"
        table.add_row(iface, ip, status, note_str)

    console.print(table)