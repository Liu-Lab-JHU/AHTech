## Read me

This folder includes corresponding example codes for the operation of AHTech platform.

In this project, we used HTTP API to integrate the OT-2 with the EC-Biologic potentiostat. The codes showing here are 
examples to demonstrate how to operate the AHTech platform. Please adjust the corresponding parameters before usage. 
For more details of the electrochemical measure parameters tuning, please refer to 
[`easy-biologic`](https://github.com/bicarlsen/easy-biologic).

If you are seeking other ways to integrate your equipments with the OT-2 robot, please see 
[here](https://github.com/Opentrons/opentrons-integration-tools/tree/main) for details.

### Disclaimer 
**Note that the HTTP API for OT-2 operation is still in its beta version. Some features may be changed or deprecated 
by the Opentrons team at any point. One should keep in mind to check the 
[updated documentation](http://sandbox.docs.opentrons.com/edge/http/api_reference.html) regularly if they want to use 
the HTTP API in case any errors occur**

### File description

#### `Full_operation.py` 
This is an example code showing the full operation of the AHTech platform with the following workflow:

![Workflow.png]([Code/AHTech Operation/img.png](https://github.com/Liu-Lab-JHU/AHTech/blob/main/Code/AHTech%20Operation/img.png))

*For detailed description of the workflow, please refer to our paper.*

#### `helper_function.py`
We wrapped up the operation features that were used in this project to this helper function. 

#### `AHTech_run.py`
This is an example code showing the full operation of the AHTech platform with importing the helper function.

#### `CV.py`
This is an example code showing how to run the CV experiment through the EC-Biologic potentiostat.

#### `PEIS.py`
This is an example code showing how to tun the PEIS experiment through the EC-Biologic potentiostat.
