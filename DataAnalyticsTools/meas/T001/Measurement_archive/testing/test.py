import json

json_file_path = '../../battery_data.json'
dutID = '250405A'                           # What DUT are you looking for

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


            # print the results
            print(f"Test for {brand} {model} {name} started.")
            print(f"battery format: {format}")
            print(f"Nominal voltage: {nominal_voltage} V")
            print(f"End-of-Life voltage: {end_of_life_voltage} V")
            print(f"Test date: {test_date}")
            print(f"Expiration date: {exp_date}")
            print(f"Product date: {prod_date}")
            print(f"Product marker: {prod_marker}")
            print(f"Merchant: {merchant}")
            print(f"Euro price per unit: {eur_price}")
            print(f"File path to img: {filepath_to_img}")
            break
    else:
        continue
    break
else:
    print(f"No Data for DUT {dutID} found.")
