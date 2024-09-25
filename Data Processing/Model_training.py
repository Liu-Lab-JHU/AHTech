#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Here is the example about how to train the ML model with different algorithms.

Please make sure Python3 was already installed as well as the corresponding packages 
(Pandas, Numpy, sklearn, and xgboost) before running the code.

For further hyperparameter-tuning, please refer to scikit-learning (https://scikit-learn.org/),
XGBoost (https://xgboost.readthedocs.io/), and AutoGluon (https://auto.gluon.ai/).
'''

# Import corresponding packages
from autogluon.tabular import TabularDataset, TabularPredictor
import numpy as np
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVM
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
import xgboost as xgb


# Define training algorithms
def LinearRegression_Model (X_train, y_train, X_test, y_test):

	linear_model = LinearRegression()

	linear_model.fit(X_train, y_train)

	y_pred = linear_model.predict(X_test)

	r2  = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def kNN_Model (X_train, y_train, X_test, y_test):
	
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)

	knn_model = KNeighborsRegressor(n_neighbors=5)	# The number of neighbors, adjust as necessary

	knn_model.fit(X_train_scaled, y_train)

	y_pred = knn_model.predict(X_test_scaled)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def SVM_Model (X_train, y_train, X_test, y_test):
	
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)

	svm_model = SVM(
		kernel="rbf", 
		C=1.0, 
		gamma=0.5, 
		epsilon=0
	)

	svm_model.fit(X_train_scaled, y_train)

	y_pred = svm_model.predict(X_test_scaled)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def NN_Model (X_train, y_train, X_test, y_test):
	
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)

	nn_model =  MLPRegressor(
		hidden_layer_sizes=(100,),  # Single hidden layer with 100 neurons
        activation="relu",          # Activation function for the hidden layer
        solver="adam",              # The solver for weight optimization.
        max_iter=500,               # Maximum number of iterations before stopping
        random_state=42
    )  

	nn_model.fit(X_train, y_train)

	y_pred = nn_model.predict(X_test)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
    "r2": r2,
    "mae": mae,
    "mse": mse,
    "rmse": rmse
    }
	return scores


def GaussianProcess_Model (X_train, y_train, X_test, y_test):
	
	gp_model = GaussianProcessRegressor(
		kernel=None, 
		n_restarts_optimizer=10, 
		alpha=1e-2, 
		normalize_y=True
	)

	gp_model.fit(X_train, y_train)

	y_pred = gp_model.predict(X_test)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def RandomForest_Model (X_train, y_train, X_test, y_test):
	
	rf_model = RandomForestRegressor(random_state=42)

	rf_model.fit(X_train, y_train)

	y_pred = rf_model.predict(X_test)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def GBT_Model (X_train, y_train, X_test, y_test):
	
	gbt_model = GradientBoostingRegressor(random_state=42)

	gbt_model.fit(X_train, y_train)

	y_pred = gbt_model.predict(X_test)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def XGB_Model (X_train, y_train, X_test, y_test):
	
	xbg_model = xgb.XGBRregressor()

	xgb_model.fit(X_train, y_train)

	y_pred = xgb_model.predict(X_test)

	r2 = r2_score(y_test, y_pred)
	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)

	scores = {
	"r2": r2,
	"mae": mae,
	"mse": mse,
	"rmse": rmse
	}

	return scores


def AG_Model (dataset, label):

	train_data, test_data = train_test_split(dataset, test_size=0.2, random_state=42)

	predictor = TabularPredictor(
		label=label, 
		problem_type="regression", 
		eval_metric = "r2").fit(
		train_data, 
		presets="best_quality", 
		num_bag_folds=5, 
		num_bag_sets=1, 
		auto_stack=True
	)

	scores = predictor.evaluate(test_data)

	return scores

if __name__ == "__main__":
	# Load dataset
	df = pd.read_csv("data_path")	# Your data path

	label = "LCE"					# Replace the label to your target

	X = df.drop(colunms=label, axis=1)
	y = df[label]

	# Split data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


	linear_scores = LinearRegression_Model(X_train, X_test, y_train, y_test)
	knn_scores = kNN_Model(X_train, X_test, y_train, y_test)
	svm_scores = SVM_Model(X_train, X_test, y_train, y_test)
	nn_scores = NN_Model(X_train, X_test, y_train, y_test)
	gp_scores = GaussianProcesss_Model(X_train, X_test, y_train, y_test)
	rf_scores = Randomforest_Model(X_train, X_test, y_train, y_test)
	gbt_scores = GBT_Model(X_train, X_test, y_train, y_test)
	xgb_scores = XGB_Model(X_train, X_test, y_train, y_test)
	ag_scores = AG_Model(df, label)

	# Print the models scores
	print("Scores of Linear Regression model is {linear_scores}")
	print("Scores of k-Nearest Neighbor model (kNN) is {knn_scores}")
	print("Scores of Support Vector Machine (SVM) model is {svm_scores}")
	print("Scores of Neural Network (NN) model is {nn_scores}")
	print("Scores of Gaussian Process (GP) model is {gp_scores}")
	print("Scores of Random Forest (RF) model is {rf_scores}")
	print("Scores of Gradient Boosting (GBT) model is {gbt_scores}")
	print("Scores of eXtreme Gradient Boosting (XGB) model is {xgb_scores}")
	print("Scores of AutoGluon (AG) model is {ag_scores}")


