#######################################################################################
#   Author:     Tim Rothenhäusler
#   Date:       30-03-2025
#   Topic:      Siglent SDL1020X-E 200W Electronic Load Setup and CSV Measurement
#   Testcase:   T001 - Battery Endurance Test
#   Interface:  USB + LAN (current support only LAN)
#   Describtion:A Battery for Example CR2032 could be assumed empty with no
#               usable energy left by passing 1.8 V. BUT this DC-Load is not
#               capable in this supply region so we will use a 9V Block Battery
#               as reference. Adjust the variables as you like and maybe you have
#               the more precise version of this equipment at home.
#######################################################################################
import pyvisa
import time
import csv
import os

################################# Battery Type Config #################################
bat_test_active = 1                     #   activate setup for bat testing
bat_brand       = "Panasonic"           #   Manufacturer / Brand of the Bat
bat_model       = "6F22_ZinkChlorid"    #   Model Number of the Bat
bat_date        = "05-2023"             #   Production Date
bat_test_date   = "31-03-2025"          #   Add todays date
bat_nominal_u   = 9     #V                  nominal voltage level of the new battery
bat_nominal_i   = 0.1   #A                  suggested nominal discharge current
bat_peak_i      = 0.25  #A                  max. capable discharge current
bat_dead_u      = 6     #V                  assume dead after falling under this
bat_cp_value    = (bat_dead_u * bat_nominal_i)
#######################################################################################

# === Config ===
visa_address = "SDL1020X-E"             # Overwise VISA Adr TCPIP0::192.168.178.148::inst0::INSTR
load_mode = "cp"                        # "cc", "cv", "cp"
target_path  = "../../DataAnalyticsTools/meas/T001"

if bat_test_active == 1:
    csv_name = f"T001_{bat_test_date}_{bat_brand}_{bat_model}_{bat_date}.csv"
    cp_value = bat_cp_value
    voltage_threshold_stop = bat_dead_u
else:
    csv_name = f"T001_Testmeasure_{bat_test_date}.csv"
    cp_value = 0.1                      # watts
    voltage_threshold_stop = 1          # volts – stop if voltage falls below

cv_value = 3.0                          # volts
cc_value = 0.1                          # amps
meas_interval_s = 1                     # seconds

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

def printConfig():
    print("Battery Test Configuration:")
    print("-" * 45)
    print(f"{'Test Active:':20} {bat_test_active}")
    print(f"{'Brand:':20} {bat_brand}")
    print(f"{'Model:':20} {bat_model}")
    print(f"{'Production Date:':20} {bat_date}")
    print(f"{'Test Date:':20} {bat_test_date}")
    print(f"{'Nominal Voltage:':20} {bat_nominal_u} V")
    print(f"{'Nominal Current:':20} {bat_nominal_i} A")
    print(f"{'Peak Current:':20} {bat_peak_i} A")
    print(f"{'End-of-Life Voltage:':20} {bat_dead_u} V")
    print(f"{'calculated CP Value:':20} {bat_cp_value} W")
    print("-" * 45)
    print()


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
        voltage = float(inst.query("MEAS:VOLT:DC?").strip())
        current = float(inst.query("MEAS:CURR:DC?").strip())
        power = float(inst.query("MEAS:POW:DC?").strip())
        resistance = float(inst.query("MEAS:RES:DC?").strip())
        return voltage, current, power, resistance
    except Exception as e:
        print(f"Measurement failed: {e}")
        return None, None, None, None

def takeMeasCSV(inst):
    os.makedirs(target_path, exist_ok=True)
    filepath = os.path.join(target_path, csv_name)

    print(f"Starting measurement loop. Abort below {voltage_threshold_stop} V.")
    with open(filepath, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index", "Timestamp", "Voltage [V]", "Current [A]", "Power [W]", "Resistance [Ohm]"])

        index = 1
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            voltage, current, power, resistance = updateMeasurements(inst)

            if None in (voltage, current, power, resistance):
                print(f"[{index}] Error during readout")
                continue

            writer.writerow([index, timestamp, voltage, current, power, resistance])
            print(f"[{index}] V={voltage:.3f} V | I={current:.6f} A | P={power:.6f} W | R={resistance:.3f} Ohm")

            if voltage < voltage_threshold_stop:
                print(f"Voltage dropped below {voltage_threshold_stop} V – ending test.")
                break

            index += 1
            time.sleep(meas_interval_s)

def main():
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(visa_address)
    inst.timeout = 5000
    inst.write_termination = '\r\n'
    inst.read_termination = '\r\n'

    try:
        test(inst)
        writeConfig(inst)
        takeMeasCSV(inst)
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        inst.write("INPUT OFF")
        inst.close()
        rm.close()

if __name__ == "__main__":
    printConfig()
    main()
