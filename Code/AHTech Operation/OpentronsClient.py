import requests
import json
import time
import os

# Keep Headers global or make it a class attribute
Headers = {"opentrons-version": "3"}

class OpentronsClient:
    """
    Client for interacting with an Opentrons robot via HTTP API.
    Manages run creation, command execution, and basic robot actions.
    """
    def __init__(self, robot_ip: str):
        """
        Initializes the client and creates a new run on the robot.

        Args:
            robot_ip: The IP address of the Opentrons robot.
        """
        self.robot_ip = robot_ip
        self.headers = {"opentrons-version": "3"} # Or use the global Headers
        self.run_id = None
        self.runs_url = f"http://{self.robot_ip}:31950/runs"
        self.commands_url = None
        self.actions_url = f"http://{self.robot_ip}:31950/actions"
        self.home_url = f"http://{self.robot_ip}:31950/robot/home"
        self.lights_url = f"http://{self.robot_ip}:31950/robot/lights"
        self.labware_defs_url = f"http://{self.robot_ip}:31950/labware_definitions"

        self._create_run()

    def _create_run(self):
        """Creates a new run on the robot and stores the run ID."""
        print(f"Creating run on {self.robot_ip}...")
        try:
            r = requests.post(
                url=self.runs_url,
                params={"waitUntilComplete": True},
                headers=self.headers
            )
            r.raise_for_status() # Raise an exception for bad status codes
            r_dict = r.json()
            self.run_id = r_dict["data"]["id"]
            self.commands_url = f"{self.runs_url}/{self.run_id}/commands"
            print(f"Run created successfully. Run ID: {self.run_id}")
            print(f"Commands URL: {self.commands_url}")
        except requests.exceptions.RequestException as e:
            print(f"Error creating run: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            self.run_id = None # Ensure run_id is None if creation failed
            # Consider raising the exception or handling it more robustly
            raise # Re-raise the exception after printing info

    def _send_command(self, command_dict: dict, wait: bool = True):
        """Helper method to send commands to the robot's run."""
        if not self.run_id or not self.commands_url:
            print("Error: Run not created or commands URL not set. Cannot send command.")
            return None # Or raise an exception

        command_payload = json.dumps(command_dict)
        params = {"waitUntilComplete": wait} if wait else {}
        try:
            r = requests.post(
                url=self.commands_url,
                headers=self.headers,
                params=params,
                data=command_payload
            )
            r.raise_for_status()
            return r.json() # Return the parsed JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error sending command: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            # Optionally return None or re-raise
            return None

    def set_lights(self, on: bool):
        """Turns the robot's rail lights on or off."""
        print(f"Setting lights {'ON' if on else 'OFF'}...")
        data = json.dumps({"on": on})
        try:
            r = requests.post(
                url=self.lights_url,
                headers=self.headers,
                data=data
            )
            r.raise_for_status()
            print("Lights set successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error setting lights: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")

    def home(self):
        """Homes the robot."""
        print("Homing robot...")
        command_dict = {"target": "robot"}
        command_payload = json.dumps(command_dict)
        try:
            r = requests.post(
                url=self.home_url,
                params={"waitUntilComplete": True},
                headers=self.headers,
                data=command_payload
            )
            r.raise_for_status()
            print("Robot homed successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error homing robot: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")


    def define_labware(self, labware_def_path: str):
        """Adds a custom labware definition to the robot."""
        print(f"Adding labware definition from: {labware_def_path}")
        try:
            with open(labware_def_path, 'r', encoding='utf-8') as f:
                labware_data = json.load(f)
            # The API expects the definition directly, not nested under "data"
            command_payload = json.dumps(labware_data)
            r = requests.post(
                url=self.labware_defs_url, # Use the correct endpoint
                headers=self.headers,
                data=command_payload
            )
            r.raise_for_status()
            print("Labware definition added successfully.")
            # Note: The response for adding definitions might not follow the standard command structure.
            # Adjust parsing if needed based on actual API response.
            # Example: definition_uri = r.json().get("data", {}).get("uri")
            # return definition_uri
            return r.json() # Return the full response for now
        except FileNotFoundError:
            print(f"Error: Labware definition file not found at {labware_def_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {labware_def_path}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error adding labware definition: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            return None


    def load_labware(self, slot: str, load_name: str, namespace: str = 'opentrons', version: int = 1):
        """Loads labware onto the deck."""
        print(f"Loading labware '{load_name}' (ns: {namespace}, v: {version}) into slot {slot}...")
        command_dict = {
            "data": {
                "commandType": "loadLabware",
                "params": {
                    "location": {"slotName": slot},
                    "loadName": load_name,
                    "namespace": namespace,
                    "version": version
                },
                "intent": "setup"
            }
        }
        response = self._send_command(command_dict)
        if response and response.get("data", {}).get("result"):
            labware_id = response["data"]["result"]["labwareId"]
            print(f"Labware loaded successfully. ID: {labware_id}")
            return labware_id
        else:
            print("Failed to load labware.")
            return None

    def load_pipette(self, pipette_name: str, mount: str):
        """Loads a pipette onto the specified mount."""
        print(f"Loading pipette '{pipette_name}' onto {mount} mount...")
        command_dict = {
            "data": {
                "commandType": "loadPipette",
                "params": {
                    "pipetteName": pipette_name,
                    "mount": mount
                },
                "intent": "setup"
            }
        }
        response = self._send_command(command_dict)
        if response and response.get("data", {}).get("result"):
            pipette_id = response["data"]["result"]["pipetteId"]
            print(f"Pipette loaded successfully. ID: {pipette_id}")
            return pipette_id
        else:
            print("Failed to load pipette.")
            return None

    def load_module(self, slot: str, module_model: str):
        """Loads a module onto the deck."""
        print(f"Loading module '{module_model}' into slot {slot}...")
        command_dict = {
            "data": {
                "commandType": "loadModule",
                "params": {
                    "model": module_model,
                    "location": {"slotName": slot}
                },
                "intent": "setup"
            }
        }
        response = self._send_command(command_dict)
        if response and response.get("data", {}).get("result"):
            module_id = response["data"]["result"]["moduleId"]
            print(f"Module loaded successfully. ID: {module_id}")
            return module_id
        else:
            print("Failed to load module.")
            return None

    # --- Pipetting Actions ---

    def pick_up_tip(self, pipette_id: str, labware_id: str, well_name: str,
                    offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Picks up a tip from the specified rack and well."""
        print(f"Pipette {pipette_id} picking up tip from {labware_id} well {well_name}...")
        command_dict = {
            "data": {
                "commandType": "pickUpTip",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {"origin": origin, "offset": offset}
                },
                "intent": "setup" # Or "protocol" if during run
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Pick up tip command sent.")
        else:
            print("Failed to send pick up tip command.")
        # Add return value if needed, e.g., command ID or status

    def drop_tip(self, pipette_id: str, labware_id: str, well_name: str,
                 offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Drops the current tip into the specified rack/trash and well."""
        print(f"Pipette {pipette_id} dropping tip into {labware_id} well {well_name}...")
        command_dict = {
            "data": {
                "commandType": "dropTip",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {"origin": origin, "offset": offset}
                },
                "intent": "setup" # Or "protocol"
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Drop tip command sent.")
        else:
            print("Failed to send drop tip command.")

    def drop_tip_in_trash(self, pipette_id: str, offset: dict = {"x": 0, "y": 0, "z": 10}):
        """Moves to trash and drops the current tip."""
        print(f"Pipette {pipette_id} dropping tip in trash...")
        # Note: API v6 uses moveToAddressableAreaForDropTip
        command_dict = {
            "data": {
                "commandType": "moveToAddressableAreaForDropTip",
                "params": {
                    "pipetteId": pipette_id,
                    "addressableAreaName": "fixedTrash",
                    "offset": offset
                },
                "intent": "setup" # Or "protocol"
            }
        }
        # This command moves *then* drops implicitly. Check API docs if separate drop needed.
        response = self._send_command(command_dict)
        if response:
            print("Drop tip in trash command sent.")
        else:
            print("Failed to send drop tip in trash command.")


    def aspirate(self, pipette_id: str, labware_id: str, well_name: str, volume: float,
                 flow_rate: float = 50, offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Aspirates liquid."""
        print(f"Pipette {pipette_id} aspirating {volume} uL from {labware_id} well {well_name}...")
        command_dict = {
            "data": {
                "commandType": "aspirate",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {"origin": origin, "offset": offset},
                    "volume": volume,
                    "flowRate": flow_rate
                },
                "intent": "setup" # Or "protocol"
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Aspirate command sent.")
        else:
            print("Failed to send aspirate command.")

    def dispense(self, pipette_id: str, labware_id: str, well_name: str, volume: float,
                 flow_rate: float = 50, offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Dispenses liquid."""
        print(f"Pipette {pipette_id} dispensing {volume} uL into {labware_id} well {well_name}...")
        command_dict = {
            "data": {
                "commandType": "dispense",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {"origin": origin, "offset": offset},
                    "volume": volume,
                    "flowRate": flow_rate
                },
                "intent": "setup" # Or "protocol"
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Dispense command sent.")
        else:
            print("Failed to send dispense command.")

    def blowout(self, pipette_id: str, labware_id: str, well_name: str,
                flow_rate: float = 50, offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Blows out remaining liquid."""
        print(f"Pipette {pipette_id} blowing out into {labware_id} well {well_name}...")
        command_dict = {
            "data": {
                "commandType": "blowout",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {"origin": origin, "offset": offset},
                    "flowRate": flow_rate
                },
                "intent": "setup" # Or "protocol"
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Blowout command sent.")
        else:
            print("Failed to send blowout command.")

    # --- Movement Actions ---

    def move_to_well(self, pipette_id: str, labware_id: str, well_name: str,
                     offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Moves the pipette to the specified well."""
        print(f"Pipette {pipette_id} moving to {labware_id} well {well_name}...")
        command_dict = {
            "data": {
                "commandType": "moveToWell",
                "params": {
                    "pipetteId": pipette_id,
                    "labwareId": labware_id,
                    "wellName": well_name,
                    "wellLocation": {"origin": origin, "offset": offset}
                },
                "intent": "setup" # Or "protocol"
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Move to well command sent.")
        else:
            print("Failed to send move to well command.")

    def move_relative(self, pipette_id: str, axis: str, distance: float):
        """Moves the pipette relative to its current position."""
        print(f"Pipette {pipette_id} moving {distance} mm along {axis} axis...")
        command_dict = {
            "data": {
                "commandType": "moveRelative",
                "params": {
                    "pipetteId": pipette_id,
                    "axis": axis,
                    "distance": distance
                },
                "intent": "setup" # Or "protocol"
            }
        }
        response = self._send_command(command_dict)
        if response:
            print("Move relative command sent.")
        else:
            print("Failed to send move relative command.")

    # --- Electrode Specific (Could be separate or integrated) ---
    # Note: The original pick_up_electrode seems identical to pick_up_tip.
    # If electrodes use special racks/handling, adjust parameters.
    def pick_up_electrode(self, pipette_id: str, electrode_rack_id: str, well_name: str = "A1",
                          offset: dict = {"x": 0, "y": 0, "z": 0}, origin: str = "top"):
        """Picks up an electrode (uses pick_up_tip command)."""
        print(f"Pipette {pipette_id} picking up electrode from {electrode_rack_id} well {well_name}...")
        self.pick_up_tip(pipette_id, electrode_rack_id, well_name, offset, origin)

    def drop_electrode(self, pipette_id: str, electrode_rack_id: str, well_name: str = "A1",
                       offset: dict = {"x": -0.6, "y": 0.6, "z": -10}, origin: str = "top"):
        """Drops an electrode back into its rack (uses drop_tip command)."""
        # Adjust offset/origin as needed for electrode placement
        print(f"Pipette {pipette_id} dropping electrode into {electrode_rack_id} well {well_name}...")
        self.drop_tip(pipette_id, electrode_rack_id, well_name, offset, origin)


# --- End of OpentronsClient Class ---

# ---------------------------------------------------------------------------

# 2. BiologicController Class
import easy_biologic as ebl
import easy_biologic.base_programs as blp
import numpy as np
import logging # Optional: for better logging from easy_biologic

class BiologicController:
    """
    Controller for interacting with a Biologic potentiostat using easy_biologic.
    """
    def __init__(self, biologic_ip: str, default_save_dir: str = './biologic_data'):
        """
        Initializes the controller and connects to the Biologic device.

        Args:
            biologic_ip: The IP address of the Biologic potentiostat.
            default_save_dir: The default directory to save experiment data.
        """
        self.biologic_ip = biologic_ip
        self.default_save_dir = default_save_dir
        self.device = None
        self._connect()
        # Create save directory if it doesn't exist
        os.makedirs(self.default_save_dir, exist_ok=True)

    def _connect(self):
        """Connects to the Biologic device."""
        print(f"Connecting to Biologic device at {self.biologic_ip}...")
        try:
            # Optional: Configure logging for easy_biologic
            # logging.basicConfig(level=logging.INFO)
            self.device = ebl.BiologicDevice(self.biologic_ip)
            # You might want to test the connection here, e.g., get device info
            print("Connected to Biologic device successfully.")
        except Exception as e: # Catch specific exceptions if known
            print(f"Error connecting to Biologic device: {e}")
            self.device = None
            raise # Re-raise after printing

    def run_cv(self, channel: int, test_name: str, save_dir: str = None, params: dict = None):
        """
        Runs a Cyclic Voltammetry (CV) experiment.

        Args:
            channel: The channel number to use.
            test_name: A base name for the output file (e.g., 'sample1_run2').
            save_dir: Directory to save the data. Uses default if None.
            params: Dictionary of CV parameters (see easy_biologic docs).
                    Uses default values if None.
        """
        if not self.device:
            print("Error: Not connected to Biologic device.")
            return None

        if params is None:
            # Define default CV parameters here if desired
            params = {
                'start': 0.5, 'end': -1.5, 'E2': 0.5, 'Ef': 0.5,
                'rate': 0.05, 'step': 0.001, 'N_Cycles': 0,
                'average_over_dE': False,
                'begin_measuring_I': 0.5, 'End_measuring_I': 1.0
            }
            print("Using default CV parameters.")

        current_save_dir = save_dir if save_dir else self.default_save_dir
        os.makedirs(current_save_dir, exist_ok=True) # Ensure dir exists
        save_path = os.path.join(current_save_dir, f"{test_name}_CV.csv")

        print(f"Running CV on channel {channel}, saving to {save_path}...")
        print(f"CV Parameters: {params}")

        try:
            cv_program = blp.CV(self.device, params, channels=channel)
            cv_program.run('data') # Assuming 'data' is the desired data level
            cv_program.save_data(save_path)
            print("CV experiment completed and data saved.")
            return cv_program.data # Return the collected data object
        except Exception as e:
            print(f"Error during CV experiment: {e}")
            return None

    def run_impedance(self, channel: int, test_name: str, frequency: float, save_dir: str = None,
                      ocv_time: float = 2.0, ocv_interval: float = 1.0,
                      peis_params: dict = None):
        """
        Runs an Open Circuit Voltage (OCV) measurement followed by
        Potentio Electrochemical Impedance Spectroscopy (PEIS).

        Args:
            channel: The channel number to use.
            test_name: A base name for the output files (e.g., 'sample1_run2').
            frequency: The final (lowest) frequency for PEIS in Hz.
            save_dir: Directory to save the data. Uses default if None.
            ocv_time: Duration of the OCV measurement in seconds.
            ocv_interval: Time interval for OCV measurements in seconds.
            peis_params: Optional dictionary to override default PEIS parameters.
                         'voltage' will be automatically set from OCV.
        """
        if not self.device:
            print("Error: Not connected to Biologic device.")
            return None, None

        current_save_dir = save_dir if save_dir else self.default_save_dir
        os.makedirs(current_save_dir, exist_ok=True) # Ensure dir exists
        ocv_save_path = os.path.join(current_save_dir, f"{test_name}_OCV.csv")
        peis_save_path = os.path.join(current_save_dir, f"{test_name}_PEIS.csv")

        # --- Run OCV ---
        print(f"Running OCV on channel {channel} for {ocv_time}s, saving to {ocv_save_path}...")
        params_ocv = {
            'time': ocv_time,
            'time_interval': ocv_interval,
            # 'voltage_interval': 0.01 # Optional
        }
        try:
            ocv_program = blp.OCV(self.device, params_ocv, channels=channel)
            ocv_program.run('data')
            ocv_program.save_data(ocv_save_path)
            print("OCV measurement completed.")

            # Calculate average OCV
            voc_data = ocv_program.data.get(channel)
            if not voc_data:
                print("Error: No OCV data found for the specified channel.")
                return None, None
            voltages = [datum.voltage for datum in voc_data]
            if not voltages:
                 print("Error: No voltage readings in OCV data.")
                 return None, None
            avg_voc = sum(voltages) / len(voltages)
            print(f"Average OCV: {avg_voc:.4f} V")

        except Exception as e:
            print(f"Error during OCV measurement: {e}")
            return None, None

        # --- Run PEIS ---
        print(f"Running PEIS on channel {channel} around {avg_voc:.4f} V, saving to {peis_save_path}...")

        # Default PEIS params (voltage set dynamically)
        default_peis_params = {
            'final_frequency': frequency,
            'initial_frequency': 100000,
            'amplitude_voltage': 0.1,
            'frequency_number': np.log10(100000 / frequency) * 20, # Points per decade
            'duration': 0,
            'repeat': 10, # Average N measurements per freq
            'wait': 0.1 # Wait time before measurement
        }

        # Override defaults with user-provided params
        current_peis_params = default_peis_params.copy()
        if peis_params:
            current_peis_params.update(peis_params)

        # Set the measured OCV as the PEIS voltage
        current_peis_params['voltage'] = avg_voc

        print(f"PEIS Parameters: {current_peis_params}")

        try:
            peis_program = blp.PEIS(self.device, current_peis_params, channels=channel)
            peis_program.run('data')
            peis_program.save_data(peis_save_path)
            print("PEIS experiment completed and data saved.")
            return ocv_program.data, peis_program.data # Return both data objects
        except Exception as e:
            print(f"Error during PEIS experiment: {e}")
            return ocv_program.data, None # Return OCV data even if PEIS failed

# --- End of BiologicController Class ---

# ---------------------------------------------------------------------------

# 3. Workflow Functions (Keep separate or add to a WorkflowManager class)
# These functions now take an OpentronsClient instance as an argument.

def wash_electrode(
    client: OpentronsClient, # Pass the client instance
    pipette_id: str,
    reservoir_id: str,
    wash_wells: list = ['E2', 'E5', 'E11'], # Acid, Water, Ethanol wells
    wash_location: dict = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -35}},
    wash_leave_location: dict = {"origin": "top", "offset": {"x": 0, "y": 0, "z": 50}},
    dip_distance_y: float = 10.0,
    wash_time: float = 5.0
):
    """
    Washes an electrode mounted on a pipette using a specified reservoir.

    Args:
        client: An initialized OpentronsClient instance.
        pipette_id: The ID of the pipette holding the electrode.
        reservoir_id: The labware ID of the washing reservoir.
        wash_wells: List of well names in the reservoir for washing steps.
        wash_location: Dictionary defining the Z-offset for dipping.
        wash_leave_location: Dictionary defining the Z-offset for moving above wells.
        dip_distance_y: Distance to move in Y during dipping (mm).
        wash_time: Time to soak in each wash well (seconds).
    """
    print(f"Starting wash sequence for pipette {pipette_id} in reservoir {reservoir_id}...")
    for well in wash_wells:
        print(f"Washing in well {well}...")
        # Move above well
        client.move_to_well(pipette_id, reservoir_id, well, location=wash_leave_location)
        # Dip into well
        client.move_to_well(pipette_id, reservoir_id, well, location=wash_location)
        # Agitate (optional dipping motion)
        client.move_relative(pipette_id, "y", dip_distance_y)
        client.move_relative(pipette_id, "y", -2 * dip_distance_y)
        client.move_relative(pipette_id, "y", dip_distance_y)
        # Wait
        print(f"Soaking for {wash_time} seconds...")
        time.sleep(wash_time)
        # Move out of well
        client.move_to_well(pipette_id, reservoir_id, well, location=wash_leave_location)
    print("Wash sequence completed.")


def dry_electrode(
    client: OpentronsClient, # Pass the client instance
    pipette_id: str,
    fan_labware_id: str, # Assuming fan is treated as labware
    fan_well: str = 'G5', # Example well near the fan
    fan_location: dict = {"origin": "top", "offset": {"x": 0, "y": 0, "z": -40}},
    fan_leave_location: dict = {"origin": "top", "offset": {"x": 0, "y": 0, "z": 80}},
    dry_time: float = 60.0
):
    """
    Moves the electrode to a drying position (e.g., near a fan) and waits.

    Args:
        client: An initialized OpentronsClient instance.
        pipette_id: The ID of the pipette holding the electrode.
        fan_labware_id: The labware ID representing the fan area.
        fan_well: The well name representing the drying position.
        fan_location: Dictionary defining the Z-offset for drying.
        fan_leave_location: Dictionary defining the Z-offset for moving above the fan area.
        dry_time: Time to wait for drying (seconds).
    """
    print(f"Starting drying sequence for pipette {pipette_id} at {fan_labware_id} well {fan_well}...")
    # Move above drying spot
    client.move_to_well(pipette_id, fan_labware_id, fan_well, location=fan_leave_location)
    # Move to drying spot
    client.move_to_well(pipette_id, fan_labware_id, fan_well, location=fan_location)
    # Wait
    print(f"Drying for {dry_time} seconds...")
    time.sleep(dry_time)
    # Optional: Move away after drying
    client.move_to_well(pipette_id, fan_labware_id, fan_well, location=fan_leave_location)
    print("Drying sequence completed.")


def liquid_transfer(
    client: OpentronsClient, # Pass the client instance
    pipette_id: str,
    tip_rack_id: str,
    tip_well: str,
    source_labware_id: str,
    dest_labware_id: str,
    source_well: str,
    dest_well: str,
    volume: float,
    aspirate_offset: dict = {"x": 0, "y": 0, "z": -35}, # Deeper aspirate default
    dispense_offset: dict = {"x": 0, "y": 0, "z": -10}, # Higher dispense default
    aspirate_flow_rate: float = 160,
    dispense_flow_rate: float = 160,
    blowout_flow_rate: float = 80,
    perform_blowout: bool = True,
    drop_tip_in_trash: bool = True
):
    """
    Performs a standard liquid transfer operation.

    Args:
        client: An initialized OpentronsClient instance.
        pipette_id: The ID of the pipette to use.
        tip_rack_id: The labware ID of the tip rack.
        tip_well: The well name to pick up the tip from.
        source_labware_id: The labware ID to aspirate from.
        dest_labware_id: The labware ID to dispense into.
        source_well: The well name to aspirate from.
        dest_well: The well name to dispense into.
        volume: The volume to transfer (in uL).
        aspirate_offset: Dictionary defining the Z-offset for aspiration.
        dispense_offset: Dictionary defining the Z-offset for dispensing.
        aspirate_flow_rate: Flow rate for aspiration (uL/s).
        dispense_flow_rate: Flow rate for dispensing (uL/s).
        blowout_flow_rate: Flow rate for blowout (uL/s).
        perform_blowout: Whether to perform a blowout after dispensing.
        drop_tip_in_trash: Whether to drop the tip in the trash afterwards.
                           If False, drops back into the original tip well.
    """
    print(f"Starting liquid transfer: {volume}uL from {source_labware_id}/{source_well} to {dest_labware_id}/{dest_well} using pipette {pipette_id}...")

    # Pick up tip
    client.pick_up_tip(pipette_id, tip_rack_id, tip_well)

    # Aspirate
    client.aspirate(pipette_id, source_labware_id, source_well, volume,
                    flow_rate=aspirate_flow_rate, offset=aspirate_offset)

    # Dispense
    client.dispense(pipette_id, dest_labware_id, dest_well, volume,
                    flow_rate=dispense_flow_rate, offset=dispense_offset)

    # Blowout
    if perform_blowout:
        client.blowout(pipette_id, dest_labware_id, dest_well,
                       flow_rate=blowout_flow_rate, offset=dispense_offset) # Blowout at dispense height

    # Drop tip
    if drop_tip_in_trash:
        client.drop_tip_in_trash(pipette_id)
    else:
        # Drop back in the rack (adjust offset if needed)
        client.drop_tip(pipette_id, tip_rack_id, tip_well, offset={"x": 0, "y": 0, "z": 0})

    print("Liquid transfer completed.")

# ---------------------------------------------------------------------------

# Example Usage (Illustrative)
if __name__ == "__main__":
    # --- Opentrons Example ---
    try:
        print("\n--- Opentrons Example ---")
        robot_ip = "169.254.166.11" # Replace with your robot's IP
        ot_client = OpentronsClient(robot_ip)

        if ot_client.run_id: # Proceed only if run creation was successful
            ot_client.set_lights(True)
            ot_client.home()

            # Load labware definition (replace with your actual path)
            # try:
            #     ot_client.add_labware_definition("/path/to/your/custom_labware.json")
            # except Exception as e:
            #     print(f"Could not load custom labware: {e}")

            # Load items
            tip_rack = ot_client.load_labware(slot="1", load_name="opentrons_96_tiprack_300ul")
            reservoir = ot_client.load_labware(slot="2", load_name="nest_12_reservoir_15ml")
            plate = ot_client.load_labware(slot="3", load_name="nest_96_wellplate_200ul_flat")
            pipette = ot_client.load_pipette(pipette_name="p300_single_gen2", mount="left")

            if all([tip_rack, reservoir, plate, pipette]):
                # Perform a transfer
                liquid_transfer(
                    client=ot_client,
                    pipette_id=pipette,
                    tip_rack_id=tip_rack,
                    tip_well="A1",
                    source_labware_id=reservoir,
                    source_well="A1",
                    dest_labware_id=plate,
                    dest_well="B2",
                    volume=150,
                    drop_tip_in_trash=True
                )
            else:
                print("Failed to load necessary items for transfer.")

            ot_client.set_lights(False)
        else:
            print("Could not establish connection or create run with Opentrons.")

    except Exception as e:
        print(f"An error occurred during Opentrons example: {e}")

    # --- Biologic Example ---
    try:
        print("\n--- Biologic Example ---")
        biologic_ip = "192.168.1.100" # Replace with your Biologic's IP
        save_directory = "./experiment_data"
        bio_controller = BiologicController(biologic_ip, default_save_dir=save_directory)

        if bio_controller.device:
            # Run CV
            cv_data = bio_controller.run_cv(channel=0, test_name="sampleA_CV1")
            if cv_data:
                print("CV Data Keys:", cv_data.keys())

            # Run Impedance
            ocv_data, peis_data = bio_controller.run_impedance(channel=0, test_name="sampleA_PEIS1", frequency=0.1)
            if ocv_data:
                print("OCV Data Keys:", ocv_data.keys())
            if peis_data:
                print("PEIS Data Keys:", peis_data.keys())
        else:
            print("Could not connect to Biologic device.")

    except Exception as e:
        print(f"An error occurred during Biologic example: {e}")