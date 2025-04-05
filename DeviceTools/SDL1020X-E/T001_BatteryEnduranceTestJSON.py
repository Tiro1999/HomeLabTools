#######################################################################################
#   Author:     Tim Rothenhäusler
#   Date:       05-04-2025
#   Topic:      Siglent SDL1020X-E 200W Electronic Load Setup and CSV Measurement
#   Testcase:   T001 - Battery Endurance Test
#   Interface:  USB + LAN (current support only LAN)
#   Describtion:This testscript is importing a JSON DB file for created DUTs and select
#               the wanted one to start the measurement loop once per second.
#######################################################################################
import pyvisa
import time
import csv
import os
import json

json_file_path  = '../../DataAnalyticsTools/meas/T001/battery_data.json'
target_path     = "../../DataAnalyticsTools/meas/T001/MeasureResultsFromJSONduts"
dutID           = "250405A"
dutInfoList     = []

# load and open JSON file
with open(json_file_path, 'r') as file:
    duts_data = json.load(file)

# look through all battery types
for battery_type, battery_info in duts_data.items():
    specific_duts = battery_info.get('SpecificDUT', [])
    # look through all DUTs of the wanted battery type
    for dut in specific_duts:
        if dut.get('dutID') == dutID:
            # General Data from the battery type
            nominal_voltage = battery_info.get('nominal_u')
            nominal_current = battery_info.get('nominal_i')
            peak_current = battery_info.get('peak_i')
            end_of_life_voltage = battery_info.get('dead_u')
            cp_max_value = battery_info.get('cp_max_value')

            # specific data of the wanted dutID
            brand = dut.get('Brand')
            format = dut.get('Format')
            model = dut.get('Model')
            test_date = dut.get('test_date')
            exp_date = dut.get('EXP_Date')
            merchant = dut.get('Merchant', 'unknown')                   # Optional
            name = dut.get('Name', 'unknown')                           # Optional Marketing Name of DUT
            prod_date = dut.get('PROD_Date', 'unknown')                 # Optional
            prod_marker = dut.get('PROD_Marker', 'unknown')             # Optional Charge number of DUT
            eur_price = dut.get('EUR_PricePer', 'unknown')              # Optional field for DUT cost per unit
            filepath_to_img = dut.get('FilepathToIMG')                  # Only needed for the result script

            dutInfoList = [
                dutID,                  # [0]  DUT ID
                battery_type,           # [1]  Battery Type
                nominal_voltage,        # [2]  Nominal Voltage
                nominal_current,        # [3]  Nominal Current
                peak_current,           # [4]  Peak Current
                end_of_life_voltage,    # [5]  End-of-Life Voltage
                cp_max_value,           # [6]  Max CP Value
                brand,                  # [7]  Brand
                format,                 # [8]  Format
                model,                  # [9]  Model
                test_date,              # [10] Test Date
                exp_date,               # [11] Expiration Date
                filepath_to_img,        # [12] File Path to Image
                merchant,               # [13] (optional) Merchant
                name,                   # [14] (optional) Marketing Name
                prod_date,              # [15] (optional) Production Date
                prod_marker,            # [16] (optional) Production Marker
                eur_price               # [17] (optional) EUR Price per Unit
            ]

            # print the results
            print(f"Test for {dutInfoList[7]} {dutInfoList[9]} {dutInfoList[14]} started.")
            print(f"battery format: {dutInfoList[8]}")
            print(f"Nominal voltage: {dutInfoList[2]} V")
            print(f"End-of-Life voltage: {dutInfoList[5]} V")
            print(f"Test date: {dutInfoList[10]}")
            print(f"Expiration date: {dutInfoList[11]}")
            print(f"Product date: {dutInfoList[15]}")
            print(f"Product marker: {dutInfoList[16]}")
            print(f"Merchant: {dutInfoList[13]}")
            print(f"Euro price per unit: {dutInfoList[17]}")
            print(f"File path to img: {dutInfoList[12]}")
            break
    else:
        continue
    break
else:
    print(f"No Data for DUT {dutInfoList[0]} found.")

################################# Battery Type Config #################################
bat_test_active = 1                                 #   activate setup for bat testing
bat_nominal_u   = dutInfoList[2]                    #V  nominal voltage level of the new battery
bat_nominal_i   = dutInfoList[3]                    #A  suggested nominal discharge current
bat_dead_u      = dutInfoList[5]                    #V  voltage level to consider dead
bat_cp_value    = ((bat_dead_u * bat_nominal_i)/2)  # Use half of cp_max value
#######################################################################################

# === Config ===
visa_address = "SDL1020X-E"             # Overwise VISA Adr TCPIP0::192.168.178.148::inst0::INSTR
load_mode = "cp"                        # "cc", "cv", "cp"

if bat_test_active == 1:
    csv_name = f"T001_{dutInfoList[0]}_{dutInfoList[7]}_{dutInfoList[11]}.csv"
    cp_value = bat_cp_value
    voltage_threshold_stop = bat_dead_u
else:
    csv_name = f"T001_Testmeasure_{dutInfoList[10]}.csv"
    cp_value = 0.1                      # watts
    voltage_threshold_stop = 6          # volts – stop if voltage falls below

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
    main()
