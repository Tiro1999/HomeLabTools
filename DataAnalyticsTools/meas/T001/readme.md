# T001 - Battery Endurance Test with Constant Load

For the edurance test we will apply a constant load to the battery.
To achieve a good comparison we will define basic rules and constants to each battery type.
These you can find under 'Battery Profiles' in this readme.
You can however set specified values for each model based on the datasheets and add those with
the [Add DUT Script](add_DUT_T001.py) and add all parameters you can find.
With that all data for your newly created DUT will be stored in the [Battery Data JSON](battery_data.json).
If you like you can always validate this data file with the [JSON Validator](Measurement_archive/testing/JSONvalidator.py).

In the current state there is the [Measurement Script T001 with JSON Support](../../../DeviceTools/SDL1020X-E/T001_BatteryEnduranceTestJSON.py)
you can use if you added the wanted DUT with you chose dutID to the JSON file.
You can include the dutID in the script and can vary the constant load you want to use.
I am currently working on the result creating scripts that are also supporting the JSON data and in the future I will
try to refactor the already done measurement result CSVs for this purpose.

## Current State - In Progress
There are a few things I really want to change before further updating any results.

## Battery Profiles 
If you adjust the "assumed dead Voltage" below the given Value for the battery type please keep
the constPower value identical for comparison reasons.

| Battery Type  | nominal_U [V] | nominal_I [mA] | dead_U [V] | constPowerMax [W] |
|---------------|---------------|----------------|------------|-------------------|
| 9V Block      | 9.00          | 0.100          | 6.00       | 0.60              |
| AA Alkaline   | 1.5           | 0.100          | 0.9        | 0.02              |



