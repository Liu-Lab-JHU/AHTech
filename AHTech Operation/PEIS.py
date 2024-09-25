#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import easy_biologic as ebl
import easy_biologic.base_programs as blp
import os


# IP of potentiostat
Biologic = ebl.BiologicDevice('Potentiostat IP')

# Potentiostat Channels
Channel = [0]

# Data Saving Directory
Path = '/data_path/'
def impedance(test):
    # Run OCP test
    save_path = Path + 'OCV.csv'

    params_ocv = {
        'time': 2,
        'time_interval': 1,
    }

    ocv = blp.OCV(
        Biologic,
        params_ocv,
        channels=Channel
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
    save_path = Path + 'PEIS.csv'

    params_peis = {
        'voltage': list(voc.values())[0],
        'final_frequency': 1000,       # frequency unit: Hertz
        'initial_frequency': 1000000,  # frequency unit: Hertz
        'amplitude_voltage': 0.1,      # voltage unit: Volt
        'frequency_number': 60,
        'duration': 0,                 # time unit: second
        'repeat': 10,
        'wait': 0.1
    }

    peis = blp.PEIS(
        Biologic,
        params_peis,
        channels=Channel
    )

    peis.run('data')
    peis.save_data(save_path)
    Impedance_data = peis.set_impedance(save_path)

    return Impedance_data

if __name__ == "__main__":
    Impedance_data = impedance()