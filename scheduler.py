import schedule
import time
import nmap
import psutil
import subprocess
from datetime import datetime
from rich.console import Console
from emailer import send_alert, build_alert_body

console = Console()

# ============================================================
# SETTINGS — change these to your preference
SCAN_TARGET = "127.0.0.1"
SCAN_INTERVAL_HOURS = 6      # how often to scan (in hours)
EMAIL_ON_RISK_ONLY = False    # True = only email if risks found
# ============================================================

RISKY_PORTS = {
    21: "FTP - unencrypted file transfer",
    23: "Telnet - completely unencrypted",
    135: "RPC - common attack vector",
    139: "NetBIOS - legacy, often exploited",
    445: "SMB - ransomware target",
    3389: "RDP - brute force target",
    5900: "VNC - remote access exposed",
}

def run_scheduled_audit():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[bold cyan]═══ SCHEDULED AUDIT — {now} ═══[/bold cyan]\n")

    findings = {
        "OPEN RISKY PORTS": [],
        "FIREWALL ISSUES": [],
        "SUSPICIOUS CONNECTIONS": [],
    }

    # --- Port Scan ---
    try:
        scanner = nmap.PortScanner()
        scanner.scan(SCAN_TARGET, '1-1024', '-T4')
        for host in scanner.all_hosts():
            for proto in scanner[host].all_protocols():
                for port in scanner[host][proto].keys():
                    state = scanner[host][proto][port]['state']
                    if state == 'open' and port in RISKY_PORTS:
                        findings["OPEN RISKY PORTS"].append(
                            f"Port {port} is OPEN — {RISKY_PORTS[port]}"
                        )
        console.print("[green]✔ Port scan complete[/green]")
    except Exception as e:
        console.print(f"[red]Port scan error: {e}[/red]")

    # --- Firewall Check ---
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
            if state and state.upper() == "OFF":
                findings["FIREWALL ISSUES"].append(
                    f"{profile} Firewall is OFF — enable immediately"
                )
        console.print("[green]✔ Firewall check complete[/green]")
    except Exception as e:
        console.print(f"[red]Firewall check error: {e}[/red]")

    # --- Suspicious Connections ---
    try:
        connections = psutil.net_connections(kind="inet")
        for conn in connections:
            if conn.status == "ESTABLISHED" and conn.raddr:
                port = conn.raddr.port
                if port in [4444, 1337, 31337, 6666, 6667]:
                    findings["SUSPICIOUS CONNECTIONS"].append(
                        f"Connection to {conn.raddr.ip}:{port} — known malware port"
                    )
        console.print("[green]✔ Connection check complete[/green]")
    except Exception as e:
        console.print(f"[red]Connection check error: {e}[/red]")

    # --- Send Email ---
    total_issues = sum(len(v) for v in findings.values())

    if total_issues == 0:
        console.print("\n[green]✔ No risks found — system is clean[/green]")
        if not EMAIL_ON_RISK_ONLY:
            body = build_alert_body({"STATUS": ["All clear — no risks detected"]})
            send_alert("✔ Network Audit — All Clear", body)
    else:
        console.print(f"\n[red]✘ {total_issues} issue(s) found — sending alert email[/red]")
        body = build_alert_body(findings)
        send_alert(f"⚠ Network Audit ALERT — {total_issues} Issue(s) Found", body)

    console.print(f"\n[yellow]Next scan in {SCAN_INTERVAL_HOURS} hour(s)...[/yellow]\n")

def main():
    console.print("[bold cyan]Network Auditor Scheduler Started[/bold cyan]")
    console.print(f"[yellow]Scanning every {SCAN_INTERVAL_HOURS} hour(s)[/yellow]")
    console.print(f"[yellow]Target: {SCAN_TARGET}[/yellow]")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]\n")

    # Run immediately on start
    run_scheduled_audit()

    # Then run on schedule
    schedule.every(SCAN_INTERVAL_HOURS).hours.do(run_scheduled_audit)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
