import config
from src.Utils.data_managemeent import load_dataset

import pandas as pd
import numpy as np
from datetime import date
import pickle
import os

from src.Configs import config, hp_config

from sklearn.linear_model import ElasticNet, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def run_training(df):

    # get today's date
    today = date.today()

    # fill nulls
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    # sort values by date, name
    df = df.sort_values(by=['Date', 'Name']).reset_index(drop=True)


    target = config.TARGET
    predictors = config.PREDICTORS

    # Independent, dependent var
    y = df[target]

    X = df.drop(target, axis=1)

    # split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.TRAIN_TEST_SPLIT, random_state=config.RANDOM_STATE)

    # make pipielines
    pipelines = {
        'lasso': make_pipeline(StandardScaler(), Lasso(random_state=config.RANDOM_STATE)),
        'ridge': make_pipeline(StandardScaler(), Ridge(random_state=config.RANDOM_STATE)),
        'enet': make_pipeline(StandardScaler(), ElasticNet(random_state=config.RANDOM_STATE)),
        'rf': make_pipeline(StandardScaler(), RandomForestRegressor(random_state=config.RANDOM_STATE)),
        'gb': make_pipeline(StandardScaler(), GradientBoostingRegressor(random_state=config.RANDOM_STATE))  # ,
        # 'xgb' : make_pipeline(StandardScaler(), xgb.XGBRegressor(random_state=123))
    }

    # Create hyperparameters dictionary
    hyperparameters = {
        'rf': hp_config.RF_HP,
        'gb': hp_config.GB_HP,
        'lasso': hp_config.LASSO_HP,
        'ridge': hp_config.RIDGE_HP,
        'enet': hp_config.ENET_HP  # ,
        # 'xgb' : xgb_hyperparameters
    }

    # Create empty dictionary called fitted_models
    fitted_models = {}

    # Loop through model pipelines, tuning each one and saving it to fitted_models
    for name, pipeline in pipelines.items():
        if not os.path.exists(r'/Users/admin/Documents/Data Science/Project Answer/Models/' + str(today)):
            os.makedirs(r'/Users/admin/Documents/Data Science/Project Answer/Models/' + (today))
        # Create cross-validation object from pipeline and hyperparameters
        model = GridSearchCV(pipeline, hyperparameters[name], cv=10, n_jobs=-1)

        # Fit model on X_train, y_train
        model.fit(X_train[predictors], y_train)

        # Store model in fitted_models[name]
        fitted_models[name] = model
        with open(r'/Users/admin/Documents/Data Science/Project Answer/Models/' + today + '/final_model_' + name + '_' + str(
                model.best_score_) + '.pickle', 'wb') as f:
            pickle.dump(fitted_models[name].best_estimator_, f)

        # Print '{name} has been fitted'
        print(name, 'has been fitted.')


if __name__ == "__main__":
    run_training()
