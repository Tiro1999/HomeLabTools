import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import os

# === Settings ===
csv_file = "T001_31-03-2025_ReweJA_6LR61_10E0A03_10-2028.csv"
interval_s = 1     # Measured interval in seconds
bat_dead_u = 6.0   # Discharge threshold

# === Load CSV ===
df = pd.read_csv(csv_file)

# Convert to float
df["Voltage [V]"] = df["Voltage [V]"].astype(float)
df["Current [A]"] = df["Current [A]"].astype(float)
df["Power [W]"] = df["Power [W]"].astype(float)
df["Resistance [Ohm]"] = df["Resistance [Ohm]"].astype(float)

# === Time axis ===
df["Time [s]"] = df["Index"] * interval_s
df["Time [min]"] = df["Time [s]"] / 60

# === Basic statistics ===
t_total = df["Time [s]"].iloc[-1]
n_samples = len(df)
U_avg = df["Voltage [V]"].mean()
I_avg = df["Current [A]"].mean()
P_avg = df["Power [W]"].mean()

# Capacity (mAh), Energy (Wh)
Q_total_mAh = (I_avg * t_total) / 3600 * 1000
E_total_Wh = (P_avg * t_total) / 3600

# Spannungseinbruch
V_start = df["Voltage [V]"].iloc[0]
V_end = df["Voltage [V]"].iloc[-1]
V_drop = V_start - V_end

# Mittelwert Innenwiderstand (effektiv gemessen)
R_avg = df["Resistance [Ohm]"].mean()

# === Plot ===
plt.figure()
plt.plot(df["Time [min]"], df["Voltage [V]"], label="Voltage [V]")
plt.plot(df["Time [min]"], df["Current [A]"], label="Current [A]")
plt.plot(df["Time [min]"], df["Power [W]"], label="Power [W]")
plt.xlabel("Time [min]")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.title("Battery Discharge Measurement")
plt.tight_layout()
plt.show()


# === Results Table ===
print("\nBattery Test Result Summary:")
#print("-" * 45)
#print(f"Total Duration:       {t_total:.1f} s ({t_total/60:.2f} min)")
#print(f"Samples Taken:        {n_samples}")
#print(f"Voltage avg:          {U_avg:.3f} V")
#print(f"Current avg:          {I_avg*1000:.2f} mA")
#print(f"Power avg:            {P_avg*1000:.2f} mW")
#print(f"Capacity (Q):         {Q_total_mAh:.2f} mAh")
#print(f"Energy (E):           {E_total_Wh:.3f} Wh")
#print(f"Voltage drop:         {V_start:.3f} V → {V_end:.3f} V = {V_drop:.3f} V")
#print(f"Avg. Resistance:      {R_avg:.2f} Ohm")
#print("-" * 45)

markdown_tabelle = f"""
| Parameter                 | Value                        |
|---------------------------|-----------------------------|
| Testduration              | {t_total:.1f} s ({t_total/60:.2f} min) |
| Sample count              | {n_samples}                 |
| Avarage voltage           | {U_avg:.3f} V               |
| Avarage current           | {I_avg*1000:.2f} mA         |
| Avarage power             | {P_avg*1000:.2f} mW         |
| Capacity (Q)              | {Q_total_mAh:.2f} mAh       |
| Energy (E)                | {E_total_Wh:.3f} Wh         |
| Voltage Drop              | {V_start:.3f} V → {V_end:.3f} V = {V_drop:.3f} V |
| Avarage resistance        | {R_avg:.2f} Ohm             |
| Price per DUT [EUR]       |                             |
| Imprinted Date            |
"""
print(markdown_tabelle)