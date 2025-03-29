##################################################################################
#   Author:     Tim Rothenhäusler
#   Date:       29-03-2025
#   Topic:      Enter all Devices you want to test the VISA Connection
#   Interface:  USB + LAN (current support only LAN)
##################################################################################
import pyvisa
from tabulate import tabulate

# LAN-ADRs (VISA over TCPIPx)           my Devices
lan_addresses = [
    "TCPIP0::192.168.178.146::INSTR",  # SDG1032X
    "TCPIP0::192.168.178.27::INSTR",   # SDM3065X
    "TCPIP0::192.168.178.162::INSTR"   # SPD4323X
]

# USB-ADRs (VISA over USBx)
usb_addresses = [
    # Example: "USB0::0xF4EC::0x0100::SDG1XCAQ5RXXXX::INSTR"
]

all_addresses = lan_addresses + usb_addresses

# Resource Manager öffnen
rm = pyvisa.ResourceManager()

# Ergebnisse sammeln
results = []

for addr in all_addresses:
    try:
        with rm.open_resource(addr) as inst:
            inst.timeout = 2000  # 2 Sekunden Timeout
            idn = inst.query("*IDN?")
            results.append([addr, idn.strip()])
    except Exception as e:
        results.append([addr, f"Error: {str(e)}"])

# Tabelle anzeigen
print(tabulate(results, headers=["Address", "*IDN? Rsp"], tablefmt="github"))
