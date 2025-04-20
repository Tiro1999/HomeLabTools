import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def import_dut_data(dut_id, json_file='battery_data.json'):
    """
    Imports DUT data from a JSON file based on the provided dut_id.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for battery_type, battery_info in data.items():
        for dut in battery_info.get('SpecificDUT', []):
            if dut.get('dutID') == dut_id:
                # Combine general battery info with specific DUT info
                return {
                    'battery_type': battery_type,
                    'nominal_voltage': battery_info.get('nominal_u'),
                    'nominal_current': battery_info.get('nominal_i'),
                    'peak_current': battery_info.get('peak_i'),
                    'end_of_life_voltage': battery_info.get('dead_u'),
                    'cp_max_value': battery_info.get('cp_max_value'),
                    'brand': dut.get('Brand'),
                    'format': dut.get('Format'),
                    'model': dut.get('Model'),
                    'test_date': dut.get('test_date'),
                    'exp_date': dut.get('EXP_Date'),
                    'merchant': dut.get('Merchant', 'unknown'),
                    'name': dut.get('Name', 'unknown'),
                    'prod_date': dut.get('PROD_Date', 'unknown'),
                    'prod_marker': dut.get('PROD_Marker', 'unknown'),
                    'eur_price': dut.get('EUR_PricePer', 'unknown'),
                    'filepath_to_img': dut.get('FilepathToIMG')
                }
    print(f"No data found for DUT ID '{dut_id}'.")
    return None

def analyze_battery_data(dut_id, data_dir='data', json_file='battery_data.json'):
    """
    Analyzes battery measurement data for the specified DUT ID.
    """
    # Import DUT data
    dut_info = import_dut_data(dut_id, json_file)
    if not dut_info:
        return

    # Construct the expected CSV filename
    csv_filename = f"T001_{dut_id}_{dut_info['brand']}_{dut_info['exp_date']}.csv"
    csv_path = os.path.join(data_dir, csv_filename)

    # Check if the CSV file exists
    if not os.path.isfile(csv_path):
        print(f"CSV file '{csv_path}' not found.")
        return

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Ensure the necessary columns are present
    required_columns = ["Timestamp", "Voltage [V]", "Current [A]", "Power [W]", "Resistance [Ohm]"]
    if not all(col in df.columns for col in required_columns):
        print("CSV file is missing required columns.")
        return

    # Convert Timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Calculate time differences in seconds
    df['Time_Diff'] = df['Timestamp'].diff().dt.total_seconds()
    df['Time_Diff'].fillna(0, inplace=True)

    # Calculate energy in watt-seconds (joules)
    df['Energy_J'] = df['Power [W]'] * df['Time_Diff']

    # Calculate cumulative energy in watt-hours
    df['Cumulative_Energy_Wh'] = df['Energy_J'].cumsum() / 3600

    # Plotting
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(df['Timestamp'], df['Voltage [V]'], label='Voltage [V]', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Voltage [V]')
    plt.title('Voltage over Time')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(df['Timestamp'], df['Current [A]'], label='Current [A]', color='green')
    plt.xlabel('Time')
    plt.ylabel('Current [A]')
    plt.title('Current over Time')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(df['Timestamp'], df['Power [W]'], label='Power [W]', color='red')
    plt.xlabel('Time')
    plt.ylabel('Power [W]')
    plt.title('Power over Time')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(df['Timestamp'], df['Resistance [Ohm]'], label='Resistance [Ohm]', color='purple')
    plt.xlabel('Time')
    plt.ylabel('Resistance [Ohm]')
    plt.title('Resistance over Time')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Print total energy discharged
    total_energy_wh = df['Cumulative_Energy_Wh'].iloc[-1]
    print(f"Total Energy Discharged: {total_energy_wh:.2f} Wh")

# Example usage
if __name__ == "__main__":
    dut_id = "250410A"
    analyze_battery_data(dut_id, data_dir='data', json_file='battery_data.json')
