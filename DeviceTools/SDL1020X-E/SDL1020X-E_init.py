##################################################################################
#   Author:     Tim Rothenhäusler
#   Date:       30-03-2025
#   Topic:      Siglent SDL1020X-E 200W Electronic Load Setup and CSV Measurement
#   Interface:  USB + LAN (current support only LAN)
##################################################################################

import pyvisa
import time
import csv
import os

# === Config ===
#visa_address = "USB0::0xF4EC::0x1621::SDL13GCD5R0910::0::INSTR"    # USB
#visa_address = "TCPIP0::192.168.178.148::inst0::INSTR"             # LAN/IP
visa_address = "SDL1020X-E"                                         # ALIAS
target_path  = "../../DataAnalyticsTools/meas/T001"
csv_name     = "loadmeasurement_001.csv"
load_mode = "cp"  # "cc", "cv", "cp"
cv_value = 3.0    # volts
cc_value = 0.1    # amps
cp_value = 0.1    # watts

# === SCPI Mapping ===
mode_map = {
    "cc": "CURR",
    "cv": "VOLT",
    "cp": "POW"
}
value_map = {
    "cc": cc_value,
    "cv": cv_value,
    "cp": cp_value
}

def test(inst):
    idn = inst.query("*IDN?").strip()
    print(f"Connected to: {idn}")

def writeConfig(inst):
    if load_mode not in mode_map:
        raise ValueError(f"Unsupported mode: {load_mode}")

    scpi_mode = mode_map[load_mode]
    set_value = value_map[load_mode]

    inst.write("SYSTEM:REMOTE")
    inst.write(f"MODE {scpi_mode}")
    inst.write(f"{scpi_mode} {set_value}")
    inst.write("INPUT ON")

    print(f"Device configured: MODE = {load_mode.upper()}, VALUE = {set_value}")

def updateMeasurements(inst):
    try:
        voltage = inst.query("MEAS:VOLT:DC?").strip()
        current = inst.query("MEAS:CURR:DC?").strip()
        power = inst.query("MEAS:POW:DC?").strip()
        resistance = inst.query("MEAS:RES:DC?").strip()
        return voltage, current, power, resistance
    except Exception as e:
        print(f"Measurement failed: {e}")
        return None, None, None, None

def takeMeasCSV(inst, count=10, interval_sec=1.0):
    os.makedirs(target_path, exist_ok=True)
    filepath = os.path.join(target_path, csv_name)

    print(f"Starting measurement loop: {count} samples every {interval_sec}s")
    with open(filepath, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index", "Timestamp", "Voltage [V]", "Current [A]", "Power [W]", "Resistance [Ohm]"])

        for i in range(count):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            voltage, current, power, resistance = updateMeasurements(inst)

            if None in (voltage, current, power, resistance):
                print(f"[{i+1}] Error during readout")
                continue

            writer.writerow([i+1, timestamp, voltage, current, power, resistance])
            print(f"[{i+1}] V={voltage} V | I={current} A | P={power} W | R={resistance} Ohm")
            time.sleep(interval_sec)

def main():
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(visa_address)
    inst.timeout = 5000
    inst.write_termination = '\r\n'
    inst.read_termination = '\r\n'

    try:
        test(inst)
        writeConfig(inst)
        takeMeasCSV(inst, count=10, interval_sec=2)
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        inst.close()
        rm.close()

if __name__ == "__main__":
    main()
