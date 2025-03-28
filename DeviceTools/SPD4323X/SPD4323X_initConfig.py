import pyvisa
import time

# VISA-Adresse des Netzteils
visa_address = 'TCPIP::192.168.178.162::inst0::INSTR'

# Resource Manager initialisieren
rm = pyvisa.ResourceManager()

try:
    # Verbindung zum Gerät herstellen
    instrument = rm.open_resource(visa_address)
    instrument.timeout = 5000  # Timeout in Millisekunden
    instrument.write_termination = '\n'
    instrument.read_termination = '\n'

    # Geräteidentifikation abfragen
    idn = instrument.query("*IDN?")
    print(f"Gerät erkannt: {idn}")

    # Kanal 1 auswählen
    instrument.write("INST:NSEL 1")
    time.sleep(0.1)  # Kurze Pause zur Verarbeitung

    # Spannung auf 3V setzen
    instrument.write("VOLT 3.0")
    time.sleep(0.1)

    # Strom auf 0,5A setzen
    instrument.write("CURR 0.5")
    time.sleep(0.1)

    # Ausgang aktivieren
    instrument.write("OUTP ON")
    time.sleep(0.1)

    print("Kanal 1 wurde auf 3V / 0,5A eingestellt und aktiviert.")

except Exception as e:
    print(f"Fehler beim Zugriff auf das Gerät: {e}")

finally:
    # Verbindung schließen
    instrument.close()
    rm.close()
