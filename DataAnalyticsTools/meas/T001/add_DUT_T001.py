import json
import os

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_dut(data):
    """Add a specific DUT to the data dictionary JSON."""
    battery_type = input("Please enter the Type of battery (example. '9V_EBlock_Alkaline'): ")

    # Check for Type
    if battery_type not in data:
        print(f"The battery type '{battery_type}' does not exists, please add general information about it.")
        return

    # Mandatory data of DUT
    dutID = input("ID for DUT: ")                                       # Used to reference a specific DUT in the results
    brand = input("Brand: ")                                            # Brand/Manufacturer of the Battery
    format = input("Format: ")                                          # Format of the battery casing
    model = input("Model: ")                                            # Model Number or any kind of marking
    test_date = input("Test date: ")                                    # Date of the testrun for this DUT
    exp_date = input("Exp Date: ")
    filepath_to_img = input("FilepathToIMG: ")

    # optional data of DUT
    merchant = input("Merchant (optional): ") or None                   # Merchant who sold the battery
    name = input("Name (optional): ") or None
    prod_date = input("Production_Date (optional): ") or None
    prod_marker = input("Production_Marker (optional): ") or None
    eur_price_per = input("Euro price per unit (optional): ")
    eur_price_per = float(eur_price_per) if eur_price_per else None

    # create new DUT
    new_dut = {
        "dutID": dutID,
        "Brand": brand,
        "Format": format,
        "Model": model,
        "test_date": test_date,
        "EXP_Date": exp_date,
        "FilepathToIMG": filepath_to_img
    }

    # add the wanted optional fields for DUT
    if merchant:
        new_dut["Merchant"] = merchant
    if name:
        new_dut["Name"] = name
    if prod_date:
        new_dut["PROD_Date"] = prod_date
    if prod_marker:
        new_dut["PROD_Marker"] = prod_marker
    if eur_price_per is not None:
        new_dut["EUR_PricePer"] = eur_price_per

    # add DUT to list
    data[battery_type]["SpecificDUT"].append(new_dut)
    print(f"The DUT was added to the battery type '{battery_type}'.")

def main():
    file_path = 'battery_data.json'
    data = load_json(file_path)

    while True:
        action = input("Do you want to add a new DUT? (y/n): ").strip().lower()
        if action == 'y':
            add_dut(data)
            save_json(data, file_path)
        elif action == 'n':
            break
        else:
            print("your choice is not supported")

if __name__ == "__main__":
    main()
