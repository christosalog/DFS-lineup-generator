# get today's lineups
import pandas as pd
import numpy as np
from datetime import datetime
import pickle

from src.FeatureEngineering.feature_eng_functions import find_season, rename_to_dk
from src.Input.daily_lineups import get_daily_lineups
import config

def make_daily_predictions(daily_lineups):

    # load trained model
    model = pickle.load(open(config.TRAINED_MODEL, 'rb'))

    # get latest row for each player from the full dataset (currently in csv but will need to structure it somehow or even add it in a database
    df = pd.read_csv(config.TRAIN_PATH)
    df = rename_to_dk(df)
    #fix season_le
    df['Season'] = df.Date.apply(lambda x: find_season(x))
    df_season = df[df.Season == '2020-21']
    df_latest = df_season.loc[df_season.groupby('Name').Date.idxmax()]

    # join lineups with full df
    df_jn = pd.merge(daily_lineups, df_latest, on='Name', how='inner')
    # calculate Rest
    df_jn['Date_x'] = df_jn.Date_x.apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
    df_jn['Date_y'] = df_jn.Date_y.apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
    df_jn['Rest'] = df_jn['Date_x'] - df_jn['Date_y']
    df_jn['Rest'] = df_jn['Rest'].apply(lambda x: x.days)

    # drop unnecessary columns
    df_jn.drop(['Pos_y', 'Salary_y', 'Starter_y', 'Home_y', 'Date_y'], axis=1, inplace=True)

    # replace/recalc salary, rest, starter, home
    df_jn.rename(columns = {'Pos_x': 'Pos', 'Salary_x': 'Salary', 'Starter_x': 'Starter', 'Home_x': 'Home', 'Date_x': 'Date'}, inplace=True)
    # df_jn = df_jn[config.PREDICTORS]

    # fill nulls
    df_jn.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_jn.fillna(0, inplace=True)

    # predict FPTS using latest trained model
    df_jn['FPTS'] = model.predict(df_jn[config.PREDICTORS])

    return df_jn

if __name__ == "__main__":
    daily_lineups = get_daily_lineups()
    daily_predictions = make_daily_predictions(daily_lineups)

