# Device Tooling Overview
You can scan in your local network for online SCPI Devices with the [Scan Script](scanForSCPIDevices.py)

## Roadmap General Setup
| Timeslot | Doing                                   |
|----------|-----------------------------------------|
| Q2/2025  | Started working on Siglent SCPI over IP |

## Roadmap Testcases
| Timeslot   | Doing                     | Devices        | Testcase  |
|------------|---------------------------|----------------|-----------|
| 30-03-2025 | Battery endurance testing | SDL1020X-E     | T001      |

## SPD4323X
- See under Chapter 10.4 for SCPI Commands [UserManuel_EN01B.pdf](../src/docs/SPD4000X_UserManual_EN01B.pdf#page=59) ([online link](https://www.siglenteu.com/wp-content/uploads/dlm_uploads/2024/08/SPD4000X_UserManual_EN01B.pdf#page=59))

## SDL1020X-E
Siglent Electronic Load 200W [Scripts](SDL1020X-E)
Known Issues:
-   Current Problem: With LAN Interface no SCPI (opened Issue)

## SDG1032X
Siglent Function Generator [Scrips](SDG1032X)
Support
-   

## Setup
- USB HUB for all devices
- [Fritz!Repeater 1200 AX](https://www.amazon.de/dp/B09N4SJLWM?ref=ppx_yo2ov_dt_b_fed_asin_title) connects with a Network Switch to all devices
- <img src="../src/res/lan_setup.jpg" alt="Setup to automate" width="400"/>
- Install the Keysight Connetion Suite IO
- Add your Devices and if you like add ALIAS Names for them
- If you dont find your devices check the menus "utilitys" --> "interfaces" --> "LAN" --> "DHCP ON"
- Keysight Connection IO Suite Setup 
- <img src="../src/res/IOSuite_SetupLAN.png" alt="IOSuite" width="400"/>
