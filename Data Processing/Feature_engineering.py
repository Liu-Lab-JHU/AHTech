#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This code is an example on how to convert a list of chemicals' CAS numbers into their SMILES
and use these SMILES strings to generate RDKit descriptors.

Please make sure Python3 and corresponding packages (Pandas, cirpy and rdkit) were 
installed before running the code.
"""


import cirpy
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors

"""
Covert CAS numbers to their SMILES.
It should be noted that sometimes the conversion is not accurate. We recommend 
to double check the converted SMILES strings before use them to generate the
RDKit descriptors.
"""

# Load the CSV file containing CAS numbers
data = pd.read_csv("CAS_file_path", header=[0])	# The chemical list file

CASes = []
identifiers = data["CAS"].values	# Assume that the column name of the CAS number is "CAS"

for CAS in identifiers:
    try:
        CASes += [CAS, cirpy.resolve(CAS, "smiles")]
    except:
        CASes += [CAS, "did not work"]

SMILES = np.array(CASes).reshape(-1,3)

print(SMILES)

# Output data
SMILES_df = pd.DataFrame(SMILES)
SMILES_df.to_csv("SMILES_save_data_path")	# Path to save the data.


"""
Generate RDKit descriptors from the chemicals' SMILES strings.
"""

# Load the CSV file containing SMILES strings
df = pd.read_csv("SMILES_file_path", header=[0])
smiles_list = df['SMILES'].tolist()	# Assume that the columnn name is "SMILES"

# Function to convert SMILES to RDKit molecule
def smiles_to_mol(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    else:
        return mol

# Function to calculate descriptors for a molecule
def calculate_descriptors(mol):
    if mol is None:
        return {desc: None for desc, func in Descriptors._descList}
    else:
        return {desc: func(mol) for desc, func in Descriptors._descList}

# Convert SMILES to molecules
molecules = [smiles_to_mol(smi) for smi in smiles_list]

# Calculate descriptors for each molecule
descriptors_list = [calculate_descriptors(mol) for mol in molecules]

# Convert list of dictionaries to DataFrame
descriptors_df = pd.DataFrame(descriptors_list)

# Optional: Combine the original SMILES with their descriptors
result_df = pd.concat([df, descriptors_df], axis=1)

# Save the results to a new CSV file
SMILES_df.to_csv("Descriptors_save_data_path", index=False)	# Path to save the data.
