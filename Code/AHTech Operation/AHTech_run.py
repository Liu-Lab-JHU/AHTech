#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import json
import logging
import easy_biologic as ebl
import easy_biologic.base_programs as blp
import time
import os
from helper_function import *

# IP of OT-2 Robot
Robot_IP = "OT2 Robot IP"

# IP of potentiostat
EC_Lab_IP = "Potentiostat IP"

# Potentiostat Channels
Channel = [0]

On = json.dumps({"on": True, "waitUntilComplete": True})
Off = json.dumps({"on": False, "waitUntilComplete": True})

# Data Saving Directory
data_path = 'data_path'

# Labware Variables
Electrode = "opentrons_96_tiprack_300ul"
Tip_Rack = "opentrons_96_tiprack_300ul"
Test_Plate = "nest_96_wellplate_200ul_flat"
Acid_Bath = 'nest_12_reservoir_15ml'
DI_Water = 'nest_12_reservoir_15ml'
Ethanol = 'nest_12_reservoir_15ml'
Fan = "nest_1_reservoir_195ml"
Electrolytes = 'nest_96_wellplate_2ml_deep'
Pipette_Left = "p300_multi_gen2"
Pipette_Right = "p300_single_gen2"

# Labware Location
Test_Plate_Slot = {"slotName": "1"}
Electrode_Slot = {"slotName": "2"}
Acid_Bath_Slot = {"slotName": "4"}
DI_Water_Slot = {"slotName": "5"}
Ethanol_Slot = {"slotName": "6"}
Electrolytes_Slot = {"slotName": "8"}
Tip_Rack_Slot = {"slotName": "9"}
Fan_Slot = {"slotName": "11"}

# Moving location
Pick_Up_Tip_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}}
Drop_Tip_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -10}}
Aspirate_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -30}}
Dispense_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -10}}
Test_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -20}}
Wash_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -27}}
Fan_Location = {"origin": "top", "offset": {"x": 0, "y": 0, "z": 0}}

# 96-well plate as an example. Adjust if necessary.
Col = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
Row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

"""
Initialization
"""
runs_url, run_id = create_run(robot_ip=Robot_IP)

commands_url = f"{runs_url}/{run_id}/commands"
actions_url = f"{runs_url}/{run_id}/labware_definitions"
lights_url = f"http://{Robot_IP}:31950/robot/lights"
home_url = f"http://{Robot_IP}:31950/robot/home"

light(status=On, url=lights_url)        # Turn on Light

# Load electrode (Electrode)
Electrode_ID = load_labware(
    slot=Electrode_Slot,
    labware=Electrode,
    brand="opentrons",
    url=commands_url
)

# Load Tip_Rack
Tip_Rack_ID = load_labware(
    slot=Tip_Rack_Slot,
    labware=Tip_Rack,
    brand="opentrons",
    url=commands_url
)

# Load Test_Plate
Test_Plate_ID = load_labware(
    slot=Test_Plate_Slot,
    labware=Test_Plate,
    brand="opentrons",
    url=commands_url
)

# Load Acid Bath
Acid_Bath_ID = load_labware(
    slot=Acid_Bath_Slot,
    labware=Acid_Bath,
    brand="opentrons",
    url=commands_url
)

# Load DI_Water
DI_Water_ID = load_labware(
    slot=DI_Water_Slot,
    labware=DI_Water,
    brand="opentrons",
    url=commands_url
)

# Load DI_Water
Ethanol_ID = load_labware(
    slot=Ethanol_Slot,
    labware=Ethanol,
    brand="opentrons",
    url=commands_url
)

# Load Fan
Fan_ID = load_labware(
    slot=Fan_Slot,
    labware=Fan,
    brand="opentrons",
    url=commands_url
)

# Load Electrolytes
Electrolytes_ID = load_labware(
    slot=Electrolytes_Slot,
    labware=Electrolytes,
    brand="opentrons",
    url=commands_url
)

# Load Pipette_Right
Pipette_Right_ID = load_pipette(
    pipette=Pipette_Right,
    mount="right",
    url=commands_url)

# Load Pipette_Left
Pipette_Left_ID = load_pipette(
    pipette=Pipette_Left,
    mount="left",
    url=commands_url)

# Home the Robot
home_url = f"http://{Robot_IP}:31950/robot/home"
home_robot(url=home_url)

# Pick up electrode and get ready to run
pick_up_electrode(
    electrode_id=Electrode_ID,
    pipette=Pipette_Right_ID,
    url=commands_url
)

print(input("Press Enter if everything is ready to run."))

"""
Main workflow
"""
for col in Col:
    for row in Row:
        well_name = row+col
        if row == "A":
            liquid_transfer(tipRackId=Tip_Rack_ID, pipette=Pipette_Left_ID,
                            tip_well="A1", aspirate_well="A1", 
                            dispense_well=well_name, aspirate_plate=Electrolytes_ID,
                            dispense_plate=Test_Plate_ID, url=commands_url,
                            aspirate_volume=250, dispense_volume=250)
        else:
            pass
        move_to_well(labware=Test_Plate_ID, well=well_name, location=Test_Location,
                     pipette=Pipette_Right_ID, url=commands_url)
        print(f"moving to {well_name}")
        time.sleep(5)

        # impedance(data_path, EC_Lab_IP, Channel, well_name, 1000)
        CV(data_path, EC_Lab_IP, Channel, well_name)
        wash(reservoir=Acid_Bath_ID, pipette=Pipette_Right_ID, url=commands_url, washtime=8)
        wash(reservoir=DI_Water_ID, pipette=Pipette_Right_ID, url=commands_url, washtime=8)
        wash(reservoir=Ethanol_ID, pipette=Pipette_Right_ID, url=commands_url, washtime=8)
        dry_electrode(Fan_ID, pipette=Pipette_Right_ID, url=commands_url, drytime=90)

"""
Finalization
"""
home_robot(url=home_url)

# Turn off Light
light(status=Off, url=lights_url)

# Stop run
actions_url = f"{runs_url}/{run_id}/actions"
action_payload = json.dumps(
    {"data": {"actionType": "stop"}}
)

r = requests.post(
    url=actions_url,
    headers=Headers,
    data=action_payload
)

print('run completed!')
