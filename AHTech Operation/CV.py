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


def CV(test):
    save_path = Path + 'CV.csv'
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
    CV_data = CV.save_data(save_path)

    return CV_data

if __name__ == "__main__":
    CV_data = CV()