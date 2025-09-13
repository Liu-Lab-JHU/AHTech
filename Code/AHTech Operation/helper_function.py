#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
For documentation, see http://${ROBOT_IP}:31950/redoc.
"""

from __future__ import print_function
import requests
import json
import logging
import time
import os
import numpy as np
import easy_biologic as ebl
import easy_biologic.base_programs as blp


Headers = {"opentrons-version": "3"}

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


def load_labware(slot, labware, brand, url):

    """
    :param slot (dict): the slot number for placing the labware.
        e.g.: {"slotName": "1"}
    :param labware (string): the labware load name.
    :param brand (string): 'opentrons' or 'custom_beta'
    :param url: command url
    """

    try:
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

        r = requests.post(
            url=url,
            headers=Headers,
            params={"waitUntilComplete": True},
            data=command_payload
        )

        r_dict = json.loads(r.text)
        labware_id = r_dict["data"]["result"]["labwareId"]
        return labware_id
    except:
        print(f"Request status:\n{r}\n{r.text}")


def load_pipette(pipette, mount, url):

    """
    :param pipette (string): pipette load name.
    :param mount: mounting position, 'left' or 'right'.
    :param url: command url.
    """

    try:
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

        r = requests.post(
            url=url,
            headers=Headers,
            params={"waitUntilComplete": True},
            data=command_payload
        )

        r_dict = json.loads(r.text)
        pipette_id = r_dict["data"]["result"]["pipetteId"]
        return pipette_id
    except:
        print(f"Request status:\n{r}\n{r.text}")


def load_module(slot, module, url):

    """
    :param slot (dict): the slot number for placing the module.
        e.g.: {"slotName": "1"}
    :param module (string): the module load name.
    :param url: command url
    """

    try:
        command_dict = {
            "data": {
                "commandType": "loadModule",
                "params": {
                    "model": module,
                    "location": slot
                },
                "intent": "setup"
            }
        }

        command_payload = json.dumps(command_dict)

        r = requests.post(
            url=url,
            headers=Headers,
            params={"waitUntilComplete": True},
            data=command_payload
        )

        r_dict = json.loads(r.text)
        module_id = r_dict["data"]["result"]["moduleId"]
        return module_id
    except:
        print(f"Request status:\n{r}\n{r.text}")


def home_robot(url):
    command_dict = {"target": "robot"}
    command_payload = json.dumps(command_dict)

    r = requests.post(
        url=url,
        params={"waitUntilComplete": True},
        headers=Headers,
        data=command_payload
    )


def labware_definitions(labware_path, url):

    """
    :param labware_path: the directory of the labware definition json file.
    WARNING: if the 'displayVolumeUnits' is 'µL', it may cause an error if encoding is not utf-8.
    :param url: actions url.
    """

    try:
        with open(labware_path, 'r', encoding='utf-8') as f:
            command_dict = {"data": json.load(f)}
        command_payload = json.dumps(command_dict)
        r = requests.post(
            url=url,
            headers=Headers,
            data=command_payload
            )
    except:
        print(f"Request status:\n{r}\n{r.text}")
        

def pick_up_electrode(electrode_id, pipette, url):

    """
    :param electrode_id (string): the electrode ID.
           e.g.: {"slotName": "1"}
    :param pipette (string): the ID of the pipette that is used to pick up the electrode.
    :param url: command url
    """

    try:
        command_dict = {
            "data": {
                "commandType": "pickUpTip",
                "params": {
                    "labwareId": electrode_id,
                    "wellName": "A1",
                    "wellLocation": {
                        "origin": "top",
                        "offset": {"x": 0, "y": 0, "z": 0}
                    },
                    "pipetteId": pipette
                },
                "intent": "setup"
            }
        }

        command_payload = json.dumps(command_dict)

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def pick_up_tip(
        rack, 
        well, 
        pipette, 
        url,
        location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 0}
        }
):

    """
    :param rack (string): the labware ID of tip rack.
    :param well (string): the well to pick up the tip.
    :param pipette (string): the ID of the pipette that is used to pick up the tip.
    :param url: command url.
    :param location (dict): the location to pick up the tip.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def drop_tip(
        rack,
        well,
        pipette,
        url,
        location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 0}
        }
):

    """
    :param rack (string): the labware ID of tip rack or trash bin.
    :param well (string): the well to drop the tip.
    :param pipette (string): the ID of the pipette that is used to drop the tip.
    :param url: command url.
    :param location (dict): the location to drop the tip.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def aspirate(
        labware,
        well,
        volume,
        pipette,
        url,
        location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 0}
        },
        flowrate = 50
):

    """
    :param labware (string): the labwere for aspirating liquid.
    :param well (string): the well for aspirating liquid.
    :param volume (float): the volume for aspirating liquid.
    :param pipette (string): the ID of the pipette that is used to aspirate liquid.
    :param url: command url.
    :param location (dict): the location for aspirating liquid.
    :param flowrate (float): the flowrate for aspirating liquid. Default: 50.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def dispense(
        labware,
        well,
        volume,
        pipette,
        url,
        location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 0}
        },
        flowrate = 50
):

    """
    :param labware (string): the labwere for dispensing liquid.
    :param well (string): the well for dispensing liquid.
    :param volume (float): the volume for dispensing liquid.
    :param pipette (string): the ID of the pipette that is used to dispense liquid.
    :param url: command url.
    :param location (dict): the location for dispensing liquid.
    :param flowrate (float): the flowrate for dispensing liquid. Default: 50.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def blowout(
        labware,
        well,
        pipette,
        url,
        location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 0}
        },
        flowrate = 50,
):

    """
    :param labware (string): the labwere for blowing out liquid.
    :param well (string): the well for blowing out liquid.
    :param pipette (string): the ID of the pipette that is used to blow out liquid.
    :param url: command url.
    :param location (dict): the location for blowing out liquid.
    :param flowrate (float): the flowrate for blowing out liquid. Default: 50.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def drop_tip_to_trash(pipette, url):

    """
    :param pipette (string): the ID of the pipette that is to drop tip.
    :param url: command url.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )

    except:
        print(f"Request status:\n{r}\n{r.text}")


def drop_tip_to_rack(pipette, labware, well, url):

    """
    :param pipette (string): the ID of the pipette that is to drop tip.
    :param labware (string): the ID of the labware (tip rack) that is to put tip back.
    :param well (string): the well to put tip back.
    :param url: command url.
    """

    try:
        command_dict = {
            "data": {
                "commandType": "dropTip",
                "params": {
                    "pipetteId": pipette,
                    "labwareId": labware,
                    "wellName": well,
                    "offset": {"x": -0.6, "y": 0.6, "z": -10}
                },
                "intent": "setup"
            }
        }

        command_payload = json.dumps(command_dict)

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")
        

def move_to_well(
        labware,
        well,
        pipette,
        url,
        location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 0}
        }
):

    """
    :param labware (string): the ID of the destination labware.
    :param well (string): the destination well name.
    :param pipette (string): the ID of the pipette that is to move.
    :param url: command url.
    :param location (dict): the destination location.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def move_relative(
        axis,
        distance,
        pipette,
        url
):

    """
    :param axis (string): the axis to move. "x", "y", or "z".
    :param distance (float): the distance to move.
    :param pipette (string): the ID of the pipette that is to move.
    :param url: command url.
    """

    try:
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

        r = requests.post(
            url=url,
            params={"waitUntilComplete": True},
            headers=Headers,
            data=command_payload
        )
    except:
        print(f"Request status:\n{r}\n{r.text}")


def wash(
        reservoir, 
        pipette, 
        url,
        wash_location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": -35}
        },
        wash_leave_location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 50}
        },
        washtime = 5
):

    """
    This function is an example of washing the electrode. A four-column reservoir is used here.
    One can customize this function if necessary.
    :param reservoir (string): the ID of the washing reservoir.
    :param pipette (string): the ID of pipette that mounts the electrode.
    :param url: command url.
    :param wash_location (dict): the location to wash the electrode.
    :param wash_leave_location (dict): the location to leave the reservoir. This param is to
           make sure the electrode won't hit the reservoir.
    :param washtime (float): the washing (soaking) time. Default: 5.
    """

    # Washed by acid (First Column)
    move_to_well(labware=reservoir, well='E2', location=wash_leave_location,
                 pipette=pipette, url=url)
    move_to_well(labware=reservoir, well='E2', location=wash_location,
                 pipette=pipette, url=url)
    move_relative(axis="y", distance=10, pipette=pipette, url=url)
    move_relative(axis="y", distance=-20, pipette=pipette, url=url)
    move_relative(axis="y", distance=10, pipette=pipette, url=url)
    time.sleep(washtime)
    move_to_well(labware=reservoir, well='E2', location=wash_leave_location,
                 pipette=pipette, url=url)

    # Washed by DI_water (Second Column)
    move_to_well(labware=reservoir, well='E5', location=wash_leave_location,
                 pipette=pipette, url=url)
    move_to_well(labware=reservoir, well='E5', location=wash_location,
                 pipette=pipette, url=url)
    move_relative(axis="y", distance=10, pipette=pipette, url=url)
    move_relative(axis="y", distance=-20, pipette=pipette, url=url)
    move_relative(axis="y", distance=10, pipette=pipette, url=url)
    time.sleep(washtime)
    move_to_well(labware=reservoir, well='E5', location=wash_leave_location,
                 pipette=pipette, url=url)

    # Washed by Ethanol (Fourth Column)
    move_to_well(labware=reservoir, well='E11', location=wash_leave_location,
                 pipette=pipette, url=url)
    move_to_well(labware=reservoir, well='E11', location=wash_location,
                 pipette=pipette, url=url)
    move_relative(axis="y", distance=10, pipette=pipette, url=url)
    move_relative(axis="y", distance=-20, pipette=pipette, url=url)
    move_relative(axis="y", distance=10, pipette=pipette, url=url)
    time.sleep(washtime)
    move_to_well(labware=reservoir, well='E11', location=wash_leave_location,
                 pipette=pipette, url=url)


def dry_electrode(
        fan,  
        pipette, 
        url, 
        fan_location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": -40}
        },
        fan_leave_location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": 80}
        },
        drytime = 60
):

    """
    This function is an example of drying the electrode.
    One can customize this function if necessary.
    :param fan (string): the ID of the fan.
    :param pipette (string): the ID of pipette that mounts the electrode.
    :param url: command url.
    :param fan_location (dict): the location to dry the electrode.
    :param fan_leave_location (dict): the location to leave the fan. This param is to
           make sure the electrode won't hit the fan.
    :param drytime (float): the drying time. Default: 60.
    """

    move_to_well(labware=fan, well='G5', location=fan_leave_location, pipette=pipette,
                url=url)
    move_to_well(labware=fan, well='G5', location=fan_location, pipette=pipette,
                url=url)
    time.sleep(drytime)


def liquid_transfer(
        tipRackId, 
        pipette,
        tip_well,
        aspirate_plate,
        dispense_plate,
        aspirate_well,
        dispense_well,
        url, 
        aspirate_location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": -35}
        },
        dispense_location = {
            "origin": "top",
            "offset": {"x": 0, "y": 0, "z": -10}
        },
        aspirate_flowrate = 160,
        dispense_flowrate = 160,
        blowout_flowrate = 80,
        aspirate_volume = 200,
        dispense_volume = 200,
        blowOut = True,
        toTrash = True
):

    """
    :param tipRackId (string): the ID of the tip rack.
    :param pipette (string): the ID of the pipette that is to be used.
    :param tip_well (string): the well to pick up the tip.
    :param aspirate_plate (string): the labware to aspirate liquid.
    :param dispense_plate (string): the labware to dispense liquid.
    :param aspirate_well (string): the well to aspirate the liquid.
    :param dispense_well (string): the well to dispense the liquid.
    :param url: command url.
    :param aspirate_location (dict): the location to aspirate the liquid.
    :param dispense_location (dict): the location to dispense the liquid.
    :param aspirate_flowrate (float): the flow rate to aspirate the liquid. Default: 160.
    :param dispense_flowrate (float): the flow rate to dispense the liquid. Default: 160.
    :param blowout_flowrate (float): the flow rate to blow out the liquid. Default: 80.
    :param aspirate_volume (float): the volume to aspirate the liquid. Default: 200.
    :param dispense_volume (float): the volume to dipense the liquid. Default: 200.
    :param blowOut (bool): if True, blow out the liquid in the dispense plate after dispensing. Default: True.
    :param toTrash (bool): if True, drop tip to trash bin after liquid transfer. Default: True.
    """
    
    # Pick up tip
    pick_up_tip(rack=tipRackId, well=tip_well, 
                pipette=pipette, url=url)

    # Aspirate
    aspirate(labware=aspirate_plate, well=aspirate_well, location=aspirate_location,
             flowrate=aspirate_flowrate, volume=aspirate_volume, pipette=pipette, url=url)

    # Dispense
    dispense(labware=dispense_plate, well=dispense_well, volume=dispense_volume, pipette=pipette, url=url,
             location=dispense_location, flowrate=dispense_flowrate)

    # Blowout
    if blowOut:
        blowout(labware=dispense_plate, well=dispense_well, location=dispense_location,
            flowrate=blowout_flowrate, pipette=pipette, url=url)
    else:
        pass
    
    # Drop tip
    if toTrash:
        drop_tip_to_trash(pipette=pipette, url=url)

    else:
        drop_tip_to_rack(pipette, tipRackId, tip_well, url)


def CV(
        path,
        elbIp,
        channel,
        test,
        params = {
            'start': 0.5,
            'end': -1.5,
            'E2': 0.5,
            'Ef': 0.5,
            'rate': 0.05,
            'step': 0.001,
            'N_Cycles': 0,
            'average_over_dE': False,
            'begin_measuring_I': 0.5,
            'End_measuring_I': 1.0
        }

):

    """

    :param path (string): the directory to save the CV data.
    :param elbIp (string): the IP address of the Biologic device.
    :param channel (string): the channel that is to be used.
    :param test (string): experiment test name.
    :param params (dict): CV experiment parameters.
    """

    Biologic = ebl.BiologicDevice(elbIp)
    save_path = path+test+'_CV.csv'

    CV = blp.CV(
        Biologic,
        params,
        channels=channel
    )

    # run program
    CV.run('data')
    CV.save_data(save_path)


def impedance(path, elbIp, channel, test, frequency):
    Biologic = ebl.BiologicDevice(elbIp)

    # Run OCP test
    save_path = path+test+'_OCV.csv'

    params_ocv = {
        'time': 2,
        'time_interval': 1,
        # 'voltage_interval': 0.01
    }

    ocv = blp.OCV(
        Biologic,
        params_ocv,
        channels=channel
    )

    ocv.run('data')
    ocv.save_data(save_path)

    voc = {
        ch: [datum.voltage for datum in data]
        for ch, data in ocv.data.items()
    }

    voc = {
        ch: sum(ch_voc) / len(ch_voc)
        for ch, ch_voc in voc.items()
    }

    # Run PEIS test
    save_path = path+test+'_PEIS.csv'

    params_peis = {
        'voltage': list(voc.values())[0],
        'final_frequency': frequency,  # frequency unit: Hertz
        'initial_frequency': 100000,  # frequency unit: Hertz
        'amplitude_voltage': 0.1,  # voltage unit: Volt
        'frequency_number': np.log10(100000/frequency)*20,
        'duration': 0,  # time unit: second
        # 'vs_final': False,
        # 'time_interval': 1,  #time unit: second
        # 'current_interval': 0.001,
        # 'sweep': 'log',
        'repeat': 10,
        # 'correction': False
        'wait': 0.1
    }

    peis = blp.PEIS(
        Biologic,
        params_peis,
        channels=channel
    )

    peis.run('data')
    peis.save_data(save_path)

