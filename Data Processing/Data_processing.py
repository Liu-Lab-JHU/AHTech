#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Here is the example code about how to process the CV data collected from AHTech plarform. 
Determination of capacity, Coulombic efficiency (CE) and onset potential were shown.

Note that the default file name of data from AHTech platform is "row+col" (for example,A1). 
Please replace the corresponding code if you save your data with different naming convention.

Please make sure Python3 and corresponding packages (Pandas, Numpy, Matplotlib, and Scipy)
were already installed before running the code.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Load data
data_path="data_path"	# Your data path
save_path="save_path"	# Path to save data

# 96-well plate as an example. Adjust if using other well plates.
Row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
Col = ['1', '2', '3', '4', '5', '6', '7', '8',  '9', '10', '11','12']

Area = 3.14*(0.005*0.005)	# Area of disc WE. 100 𝜇m disc WE as an example. Adjust if necessary.

cycle_num = 0 	# Process the first cycle of CV. Adjust if necessary.

E_onset, scan_number, Capacity, Coulombic_efficiency = list(), list(), list(), list()


def data_process (CV_filename, threshold=0.1):	# Adjust the threshold if necessary.

    #determine onset potential
    df = pd.read_csv(CV_filename, header = [0], sep = ',')
    df=df.iloc[1:,:]
    df=df[df['Cycle']==cycle_num]
    df = df[(df['Voltage'] < 0.6) & (df['Voltage']>=-0.25)]
    df['Current'] = df['Current']*1000	# Convert current from A to mA.

    potential = df[df['Voltage']<-0.05].reset_index()
    current_derivative = np.gradient(potential['Current'], potential['Voltage'])

    # Find the onset potential by locating the index where the derivative surpasses the threshold
    onset_index = np.argmax(np.abs(current_derivative) > threshold)
    onset_potential = potential['Voltage'][onset_index]

    #plot onset potential
    plt.plot(df['Voltage'], df['Current'], label='CV curve')
    plt.axvline(onset_potential, color='r', linestyle='--', label=f'Onset potential: {onset_potential:.3f} V')
    plt.xlabel('Potential (V)')
    plt.ylabel('Current (mA)')
    plt.title('Cyclic Voltammetry with Onset Potential of ' + row+col)
    plt.legend()
    plt.grid(True)
    plt.show()

    #Separate charging and discharging data
    ad_potential = df[(df['Voltage']>0.1)&(df['Time']>max_row['Time'])&(df['Current']<0.01)].reset_index()
    ad_current_derivative = np.gradient(ad_potential['Current'], ad_potential['Voltage'])
    cutoff_index = np.argmax(np.abs(ad_current_derivative) < 0.1)
    cutoff_voltage = ad_potential['Voltage'][cutoff_index]

    cd = df[df['Voltage'] < 0]
    ad = df[(df['Voltage'] < cutoff_voltage) & (df['Voltage']>onset_potential)]

    cathodic_data = cd[df['Current'] < 0]
    anodic_data = ad[df['Current'] > 0 ]

    # Calculate the charge delivered during charging and discharging
    cathodic_charge = np.trapz(cathodic_data['Current'], cathodic_data['Time'])
    anodic_charge = np.trapz(anodic_data['Current'], anodic_data['Time'])

    # Calculate Coulombic efficiency and capacity. Diameter set as 100 micron
    CE = abs(anodic_charge / (cathodic_charge)) * 100
    capacity = abs(cathodic_charge/3600/Area)

    return onset_potential, CE, capacity


# Data processing
for col in Col:
    for row in Row:

        if __name__ == "__main__":

            CV_filename = data_path + row+col + '.csv'
            try:
                onset_potential, CE, capacity = data_process (CV_filename)
            except:
                onset_potential = "N/A"
                CE = "N/A"
                capacity = "N/A"

            E_onset.append(onset_potential)
            scan_number.append(row+col)
            Capacity.append(capacity)
            Coulombic_efficiency.append(CE)

            try:
                print(f"Onset potential: {onset_potential:.3f} V")
                print(f'Coulombic efficiency: {CE:.2f}%')
                print(f'Capacity: {capacity:.2f} mAh/cm2')
            except:
                print("Unable to process the data. Please check the source data.")

Result = {
    'onset potential': E_onset,
    'Capacity': Capacity,
    'Coulombic Efficiency': Coulombic_efficiency,
}

# Save processed data
df = pd.DataFrame(Result,index=scan_number)
df.to_csv(save_path+"summary_result_cycle_"+str(cycle_num)+".csv")


