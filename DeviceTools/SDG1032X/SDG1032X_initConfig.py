##################################################################################
#   Author:     Tim Rothenhäusler
#   Date:       28-03-2025
#   Topic:      Siglent SDG1032X Function Generator Python Control Interface
#   Interface:  USB + LAN (current support only LAN)
##################################################################################

import pyvisa

# VISA-ADR of your device - see Connection IO Suite or other VISA Lib
VISA_ADDRESS = "TCPIP0::192.168.178.27::inst0::INSTR"

def read_config(instr):
    print("📋 current configuration:")
    idn = instr.query('*IDN?').strip()
    print(f"Model:         {idn}")

    func_raw = instr.query("FUNC?").strip().strip('"')
    print(f"Measurement function:   {func_raw}")

    # Mapping zur vollen SCPI-Funktion
    full_func_map = {
        "VOLT": "VOLT:DC",
        "CURR": "CURR:DC",
        "RES": "RES",
        "FREQ": "FREQ",
        "PER": "PER",
        "CAP": "CAP",
        "CONT": "CONT",
        "DIODE": "DIODe",
        "TEMP": "TEMP"
    }

    if func_raw not in full_func_map:
        print("⚠️ Unknown function - No details.")
        return

    mode = full_func_map[func_raw]
    base_func = mode.split(":")[0]

    # Bereich und Auto-Range
    try:
        print(f"Measured range: {instr.query(f'{mode}:RANG?').strip()} V/A/Ohm")
        print(f"Auto-Range:     {instr.query(f'{mode}:RANG:AUTO?').strip()}")
    except Exception as e:
        print(f"❌ Error in range response: {e}")

    # NPLC
    try:
        print(f"NPLC:           {instr.query(f'{base_func}:NPLC?').strip()}")
    except Exception as e:
        print(f"❌ Error on NPLC: {e}")

    # Triggersource
    try:
        print(f"Triggerquelle:  {instr.query('TRIG:SOUR?').strip()}")
    except Exception as e:
        print(f"❌ Error in Trigger Source: {e}")

    # Filterstatus
    try:
        print(f"Filter aktiv?:  {instr.query(f'{base_func}:AVER:STAT?').strip()}")
    except Exception as e:
        print(f"❌ Error in filterstate: {e}")


def set_config(instr, mode="VOLT:DC", range_val=10, auto_range=True, nplc=1, filter_on=False):
    print(f"\n⚙️ new configuration set: {mode}")
    instr.write(f"FUNC '{mode}'")

    if auto_range:
        instr.write(f"{mode}:RANG:AUTO ON")
    else:
        instr.write(f"{mode}:RANG {range_val}")

    base_func = mode.split(":")[0]
    instr.write(f"{base_func}:NPLC {nplc}")

    if filter_on:
        instr.write(f"{base_func}:AVER:STAT ON")
    else:
        instr.write(f"{base_func}:AVER:STAT OFF")

    instr.write("TRIG:SOUR IMM")
    print("✅ Configuration set.")

def main():
    rm = pyvisa.ResourceManager()
    instr = rm.open_resource(VISA_ADDRESS)
    instr.timeout = 3000
    instr.write_termination = '\n'
    instr.read_termination = '\n'

    # read current config
    read_config(instr)

    # Example: set new configuration (optional)
    # set_config(instr, mode="VOLT:DC", range_val=10, auto_range=True, nplc=1, filter_on=True)

    instr.close()
    rm.close()

if __name__ == "__main__":
    main()
