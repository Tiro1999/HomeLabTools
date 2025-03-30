# T001 - Battery Endurance Test with Constant Load

For the edurance test we will apply a constant load to the battery.
To achieve a good comparison we will define basic rules and constants to each battery type.
These you can find under 'Battery Profiles' in this readme.
You can however set specified values for each model based on the datasheets. For my Meaurements I will 
provide a table overview of my used values for each battery type and most of the time they will be
very similar or identical per type for a better comparison. These are general purpose values.
If you add all the battery parameter to the [T001 - Script](../../../DeviceTools/SDL1020X-E/T001_BatteryEnduranceTest.py)
it will automatically define a unique CSV file name for your testrun with the following pattern 
'T001_testDate_Brandname_ModelNumber_imprintDate.csv'

## Battery Profiles 
If you adjust the "assumed dead Voltage" below the given Value for the battery type please keep
the constPower value identical for comparison reasons.

| Battery Type  | nominal_U [V] | nominal_I [mA] | dead_U [V] | constPower [W]  |
|---------------|---------------|----------------|------------|-----------------|
| 9V Block      | 9.00          | 0.100          | 6.00       | 0.60            |


## Testruns and Results
### ALDI - Topcraft Ultra Alkaline
<img src="../../../src/res/T001/Topcraft_6LR61_30-03-2025.jpg" alt="Topcraft Block" width="400"/>

You can find the [CSV Measurements](T001_30-03-2025_Topcraft_6LR61_01-2023.csv)
Battery Test Result Summary:
---------------------------------------------
Total Duration:       14798.0 s (246.63 min)
Samples Taken:        14798
Voltage avg:          7.106 V
Current avg:          85.13 mA
Power avg:            600.99 mW
Capacity (Q):         349.92 mAh
Energy (E):           2.470 Wh
Voltage drop:         9.105 V → 6.000 V = 3.105 V
Avg. Resistance:      84.58 Ohm
---------------------------------------------

