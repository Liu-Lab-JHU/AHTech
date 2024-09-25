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


# IP of OT-2 Robot
Robot_IP = "Robot IP"
Headers = {"opentrons-version": "3"}

# IP of potentiostat
Biologic = ebl.BiologicDevice('Potentiostat IP')

On = json.dumps({"on": True, "waitUntilComplete": True})
Off = json.dumps({"on": False, "waitUntilComplete": True})

# Potentiostat Channels
Channel = [0]

# Data Saving Directory
Path = '/data_path/'

# Labware Variables
Electrode = "opentrons_96_tiprack_300ul"
Tip_Rack = "opentrons_96_tiprack_300ul"
Test_Plate = "nest_96_wellplate_200ul_flat"
Acid_Bath = 'nest_1_reservoir_195ml'
DI_Water = 'nest_1_reservoir_195ml'
Ethanol = 'nest_1_reservoir_195ml'
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


def create_run(robot_ip):
    runs_url = f"http://{robot_ip}:31950/runs"
    print(f"Command:\n{runs_url}")

    r = requests.post(
        url=runs_url,
        params={"waitUntilComplete": True},
        headers=Headers
    )

    r_dict = json.loads(r.text)
    run_id = r_dict["data"]["id"]
    print(f"Run ID:\n{run_id}")
    return runs_url, run_id


def light(status, url):
    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=status)  # ON or OFF

    print(f"Request status:\n{r}\n{r.text}")


def load_labware(slot, labware, brand, url):
    command_dict = {
        "data": {
            "commandType": "loadLabware",
            "params": {
                "location": slot,
                "loadName": labware,
                "namespace": brand,
                "version": 1
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}")

    r = requests.post(
        url=url,
        headers=Headers,
        params={"waitUntilComplete": True},
        data=command_payload
    )

    r_dict = json.loads(r.text)
    labware_id = r_dict["data"]["result"]["labwareId"]
    return labware_id


def load_pipette(pipette, mount, url):
    command_dict = {
        "data": {
            "commandType": "loadPipette",
            "params": {
                "pipetteName": pipette,
                "mount": mount
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}")

    r = requests.post(
        url=url,
        headers=Headers,
        params={"waitUntilComplete": True},
        data=command_payload
    )

    r_dict = json.loads(r.text)
    pipette_id = r_dict["data"]["result"]["pipetteId"]
    return pipette_id


def home_robot(url):
    command_dict = {"target": "robot"}
    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")

def pick_up_electrode(electrode_id, pipette, url):
    command_dict = {
        "data": {
            "commandType": "pickUpTip",
            "params": {
                "labwareId": electrode_id,
                "wellName": "A1",
                "wellLocation": {
                    "origin": "top", "offset": {"x": 0, "y": 0, "z": 0}
                },
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def pick_up_tip(rack, well, location, pipette, url):
    command_dict = {
        "data": {
            "commandType": "pickUpTip",
            "params": {
                "labwareId": rack,
                "wellName": well,
                "wellLocation": location,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def drop_tip(rack, well, location, pipette, url):
    command_dict = {
        "data": {
            "commandType": "dropTip",
            "params": {
                "labwareId": rack,
                "wellName": well,
                "wellLocation": location,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def aspirate(labware, well, location, flowrate, volume, pipette, url):
    command_dict = {
        "data": {
            "commandType": "aspirate",
            "params": {
                "labwareId": labware,
                "wellName": well,
                "wellLocation": location,
                "flowRate": flowrate,
                "volume": volume,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")

def dispense(labware, well, location, flowrate, volume, pipette, url):
    command_dict = {
        "data": {
            "commandType": "dispense",
            "params": {
                "labwareId": labware,
                "wellName": well,
                "wellLocation": location,
                "flowRate": flowrate,
                "volume": volume,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def blowout(labware, well, location, flowrate, pipette, url):
    command_dict = {
        "data": {
            "commandType": "blowout",
            "params": {
                "labwareId": labware,
                "wellName": well,
                "wellLocation": location,
                "flowRate": flowrate,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def drop_tip_to_trash(pipette, url):
    command_dict = {
        "data": {
            "commandType": "moveToAddressableAreaForDropTip",
            "params": {
                "pipetteId": pipette,
                "addressableAreaName": "fixedTrash",
                "offset": {"x": 0, "y": 0, "z": 10}
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")

    command_dict = {
        "data": {
            "commandType": "dropTipInPlace",
            "params": {
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def move_to_well(labware, well, location, pipette, url):
    command_dict = {
        "data": {
            "commandType": "moveToWell",
            "params": {
                "labwareId": labware,
                "wellName": well,
                "wellLocation": location,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def move_relative(axis, distance, pipette, url):
    command_dict = {
        "data": {
            "commandType": "moveRelative",
            "params": {
                "axis": axis,
                "distance": distance,
                "pipetteId": pipette
            },
            "intent": "setup"
        }
    }

    command_payload = json.dumps(command_dict)
    print(f"Command:\n{command_payload}\n")

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )

    print(f"Response:\n{r}\n{r.text}\n")


def CV(test):
    save_path = Path+test+'.csv'
    params = {
        'start': 0.5,
        'end': -0.25,
        'E2': 0.5,
        'Ef': 0.5,
        'rate': 0.05,
        'step': 0.001,
        'N_Cycles': 0,
        'average_over_dE': False,
        'begin_measuring_I': 0.5,
        'End_measuring_I': 1.0
    }

    CV = blp.CV(
        Biologic,
        params,
        channels=Channel  
    )

    # run program
    CV.run('data')
    CV.save_data(save_path)


def wash(reservoir, location, pipette, url, washtime):
    move_to_well(labware=reservoir, location=location,well="A1",
                 pipette=pipette, url=url)
    move_relative(axis="x", distance=12, pipette=pipette, url=url)
    move_relative(axis="x", distance=-24, pipette=pipette, url=url)
    move_relative(axis="x", distance=12, pipette=pipette, url=url)
    time.sleep(washtime)

def dry_electrode(reservoir, location, pipette, url, drytime):
    move_to_well(labware=reservoir, location=location, well="A1", pipette=pipette, url=url)
    time.sleep(drytime)

def liquid_transfer(pipette, well, electrolytes, test_plate, url):

    # Pick up tip
    pick_up_tip(rack=Tip_Rack_ID, well=well, location=Pick_Up_Tip_Location,
                pipette=pipette, url=url)

    # Aspirate
    aspirate(labware=electrolytes, well=well, location=Aspirate_Location,
             flowrate=160, volume=200, pipette=pipette, url=url)

    # Dispense
    dispense(labware=test_plate, well=well, location=Dispense_Location,
             flowrate=160, volume=200, pipette=pipette, url=url)

    # Blowout
    blowout(labware=test_plate, well=well, location=Dispense_Location,
            flowrate=80, pipette=pipette, url=url)

    # Drop tip
    drop_tip_to_trash(pipette=pipette, url=url)


"""
Initialization
"""
runs_url, run_id = create_run(robot_ip=Robot_IP)

commands_url = f"{runs_url}/{run_id}/commands"

lights_url = f"http://{Robot_IP}:31950/robot/lights"

light(status=On, url=lights_url)        # Turn on Light

# Load electrode (Electrode)
Electrode_ID = load_labware(
    slot=Electrode_Slot,
    labware=Electrode,
    brand="opentrons",
    url=commands_url
)

# Load Labware 1 (Tip_Rack)
Labware_1_ID = load_labware(
    slot=Tip_Rack_Slot,
    labware=Tip_Rack,
    brand="opentrons",
    url=commands_url
)
Tip_Rack_ID = Labware_1_ID

# Load Labware 2 (Test_Plate)
Labware_2_ID = load_labware(
    slot=Test_Plate_Slot,
    labware=Test_Plate,
    brand="opentrons",
    url=commands_url
)
Test_Plate_ID = Labware_2_ID

# Load Labware 3 (Acid Bath)
Labware_3_ID = load_labware(
    slot=Acid_Bath_Slot,
    labware=Acid_Bath,
    brand="opentrons",
    url=commands_url
)
Acid_Bath_ID = Labware_3_ID

# Load Labware 4 (DI_Water)
Labware_4_ID = load_labware(
    slot=DI_Water_Slot,
    labware=DI_Water,
    brand="opentrons",
    url=commands_url
)
DI_Water_ID = Labware_4_ID

# Load Labware 5 (DI_Water)
Labware_5_ID = load_labware(
    slot=Ethanol_Slot,
    labware=Ethanol,
    brand="opentrons",
    url=commands_url
)
Ethanol_ID = Labware_5_ID

# Load Labware 6 (Fan)
Labware_6_ID = load_labware(
    slot=Fan_Slot,
    labware=Fan,
    brand="opentrons",
    url=commands_url
)
Fan_ID = Labware_6_ID

# Load Labware 7 (Electrolytes)
Labware_7_ID = load_labware(
    slot=Electrolytes_Slot,
    labware=Electrolytes,
    brand="opentrons",
    url=commands_url
)
Electrolytes_ID = Labware_7_ID

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
            liquid_transfer(pipette=Pipette_Left_ID, well=well_name,
                            electrolytes=Electrolytes_ID, test_plate=Test_Plate_ID, url=commands_url)
        else:
            pass
        move_to_well(labware=Test_Plate_ID, well=well_name, location=Test_Location,
                     pipette=Pipette_Right_ID, url=commands_url)
        time.sleep(5)
        CV(well_name)
        wash(reservoir=Acid_Bath_ID, location=Wash_Location, pipette=Pipette_Right_ID, url=commands_url, washtime=8)
        wash(reservoir=DI_Water_ID, location=Wash_Location, pipette=Pipette_Right_ID, url=commands_url, washtime=8)
        wash(reservoir=Ethanol_ID, location=Wash_Location, pipette=Pipette_Right_ID, url=commands_url, washtime=8)
        dry_electrode(reservoir=Fan_ID, location=Fan_Location, pipette=Pipette_Right_ID, url=commands_url, drytime=60)

"""
Finalization
"""
home_url = f"http://{Robot_IP}:31950/robot/home"
home_robot(url=home_url)

lights_url = f"http://{Robot_IP}:31950/robot/lights"

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

print(f"Request status:\n{r}\n{r.text}")

print('run complete!')
