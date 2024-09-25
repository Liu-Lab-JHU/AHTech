#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This code is an example on how to generate the R2 plot of the model.
We assume that you have already saved your predicted data (y_pred) 
and the observed data (y_test) in the .csv file.

Please make sure Python3 as well as corresponding packages (Pandas, 
Numpy, matplotlib, and sklearn) were already installed before you
run the code.
"""


from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def make_plot(y_test, y_pred, rsme, r2_score, mae):
    fontsize = 12
    fig, ax = plt.subplots(figsize=(8, 8))
    r2_patch = mpatches.Patch(label="R$^2$ = {:.2f}".format(r2_score), color="#1f77b4")
    rmse_patch = mpatches.Patch(label="RMSE = {:.2f}".format(rmse), color="#1f77b4")
    mae_patch = mpatches.Patch(label="MAE = {:.2f}".format(mae), color="#1f77b4")
    plt.xlim(0, 4)
    plt.ylim(0, 4)
    plt.scatter(y_test, y_pred, alpha=0.8, color="#1f77b4")
    plt.plot(np.arange(4), np.arange(4), 'k--')
    plt.legend(handles=[r2_patch, rmse_patch, mae_patch], fontsize=12)
    plt.tick_params(axis='both',which='major',width=0.8, color='white',direction="in", labelsize =12)
    space = 0.7
    ax.xaxis.set_major_locator(ticker.MultipleLocator(space))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(space))
    ax.set_facecolor('#EBEFF2')
    ax.grid(True, which='both', linestyle='-', linewidth=1.2, color='white')
    ax.set_ylabel('Predicted', fontsize=fontsize,font='Avenir')
    ax.set_xlabel('Observed', fontsize=fontsize,font='Avenir')
    ax.set_title('Test set (label: LCE)', fontsize=18,font='Avenir')
    return fig


df = pd.read_csv('data_path')	# Your data path

y_test = df['y_test']
y_preds = df['y_pred']

r_squared = r2_score(y_test, y_preds)
rmse = mean_squared_error(y_test, y_preds) ** 0.5
mae = mean_absolute_error(y_test, y_preds)

fig = make_plot(y_test, y_preds, rmse, r_squared, mae)
