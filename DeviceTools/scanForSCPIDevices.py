import socket
import subprocess
import platform
import pyvisa
from tabulate import tabulate

# Optional: Layer 2 ARP-Scan versuchen
try:
    from scapy.all import ARP, Ether, srp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# ===== KONFIGURATION =====
subnet = "192.168.178.0/24"
scpi_port = 5025
timeout_sec = 1

# ===== SCAPY ARP-SCAN (Layer 2) =====
def find_alive_hosts_scapy(subnet):
    print("📡 Scanne Netzwerk mit Scapy/ARP ...")
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=2, verbose=0)[0]
    return [rcv.psrc for snd, rcv in result]

# ===== PING-Fallback (Layer 3) =====
def ping_host(ip):
    ping_cmd = ["ping", "-n", "1", "-w", "200", ip] if platform.system() == "Windows" \
        else ["ping", "-c", "1", "-W", "1", ip]
    result = subprocess.run(ping_cmd, stdout=subprocess.DEVNULL)
    return result.returncode == 0

def find_alive_hosts_ping(subnet):
    print("📡 Scanne Netzwerk mit Ping (Fallback) ...")
    base = subnet.rsplit('.', 1)[0]
    return [f"{base}.{i}" for i in range(1, 255) if ping_host(f"{base}.{i}")]

# ===== Port-Check auf 5025 (SCPI) =====
def is_port_open(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=timeout_sec):
            return True
    except:
        return False

# ===== *IDN? über PyVISA =====
def get_scpi_idn(ip):
    try:
        rm = pyvisa.ResourceManager('@py')
        instr = rm.open_resource(f"TCPIP::{ip}::INSTR")
        instr.timeout = 3000
        instr.write_termination = '\n'
        instr.read_termination = '\n'
        idn = instr.query("*IDN?")
        instr.close()
        return idn.strip()
    except Exception as e:
        return f"(Fehler: {e})"

# ===== Hauptfunktion =====
def main():
    # Host-Scan versuchen
    try:
        if SCAPY_AVAILABLE:
            hosts = find_alive_hosts_scapy(subnet)
        else:
            raise RuntimeError("Scapy nicht verfügbar oder nicht eingerichtet.")
    except Exception as e:
        print(f"⚠️  Fehler bei ARP-Scan: {e}\n→ Fallback auf Ping.")
        hosts = find_alive_hosts_ping(subnet)

    print(f"✅ {len(hosts)} aktive Hosts gefunden\n")

    # Ergebnisse sammeln
    table = []
    for ip in hosts:
        if is_port_open(ip, scpi_port):
            idn = get_scpi_idn(ip)
            table.append([ip, idn])
        else:
            table.append([ip, "Kein SCPI-Gerät (Port 5025 geschlossen)"])

    # Ausgabe
    print(tabulate(table, headers=["IP-Adresse", "*IDN?-Antwort"], tablefmt="grid"))

if __name__ == "__main__":
    main()
