#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:40:23 2020

@author: admin
"""
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

'''Feature Engineering Functions'''
#create functions for double double and triple double
def dd(row):
    counting_cats=['PTS', 'TRB', 'AST', 'STL', 'BLK']
    count=0
    for i in counting_cats:
        if row[i]>=10:
            count+=1
    if count==2:
        return 1
    else:
        return 0

def td(row):
    counting_cats=['PTS', 'TRB', 'AST', 'STL', 'BLK']
    count=0
    for i in counting_cats:
        if row[i]>=10:
            count+=1
    if count==2:
        return 1
    else:
        return 0
    
    
def fpts_calc(df):
    #Fpts
    df['FPTS'] = df['PTS'] + 1.5*df['AST'] + 1.25*df['TRB'] + 0.5*df['3P'] + 2*df['STL'] + 2*df['BLK'] + (-1)*df['TOV'] + 1.5*df['DD']+3*df['TD']
    
    return df

def ts_calc(df):
    '''
    calculates true shooting percentage
    '''
    df['TS_perc'] = df['PTS'] / 2*(df['FGA'] + 0.44*df['FTA'])
    
    return df


def rest_days(df):
    rest_days = []
    for i in tqdm(range(df.shape[0])):
        #find the date and the name for that row
        date = df.loc[i, 'Date']
        name = df.loc[i, 'Name']
        season = df.loc[i, 'Season']
        
        #create a dataframe for that player only
        df_name = df[(df.Name == name)&(df.Season == season)].reset_index(drop=True)
        #find the index of the current row's date in df_name
        index = df_name.loc[df_name['Date']==date].index[0]
        
        if index > 0:
            #create df_past for all games before index
            df_past = df_name[index-1:index].reset_index(drop=True)
            
            #count number of days between current game and previous game
            current = datetime.strptime(str(df_name.loc[index, 'Date']), '%Y%m%d')
            previous = datetime.strptime(str(df_past.loc[df_past.shape[0]-1, 'Date']), '%Y%m%d')
            rest = current - previous
            
            rest_days.append(rest.days)
        else:
            rest_days.append(10)
            
    df['Rest'] = ' '
    df['Rest'] = list(rest_days)
    
    return df

# move to a utils script
def rename_players(df):
    df['Name'] = np.where(df['Name'] == 'Skal Labissière', 'Skal Labissiere', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Jusuf Nurkić', 'Jusuf Nurkic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Dennis Schröder', 'Dennis Schroder', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Džanan Musa', 'Dzanan Musa', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Nikola Vučević', 'Nikola Vucevic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Timothé Luwawu-Cabarrot', 'Timothe Luwawu-Cabarrot', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Vlatko Čančar', 'Vlatko Cancar', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Nikola Jokić', 'Nikola Jokic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Willy Hernangómez', 'Willy Hernangomez', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Ante Žižić', 'Ante Zizic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Bogdan Bogdanović', 'Bogdan Bogdanovic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Goran Dragić', 'Goran Dragic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Kristaps Porziņģis', 'Kristaps Porziņgis', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Ersan İlyasova', 'Ersan Ilyasova', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Bojan Bogdanović', 'Bojan Bogdanovic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Luka Šamanić', 'Luka Samanic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Luka Dončić', 'Luka Doncic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Dario Šarić', 'Dario Saric', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Jonas Valančiūnas', 'Jonas Valanciunas', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Alen Smailagić', 'Alen Smailagic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Anžejs Pasečņiks', 'Anzejs Pasecņiks', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Dāvis Bertāns', 'Davis Bertans', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Boban Marjanović', 'Boban Marjanovic', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Juan Hernangómez', 'Juan Hernangomez', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Cristiano Felício', 'Cristiano Felicio', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Tomáš Satoranský', 'Tomas Satoransky', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Nicolò Melli', 'Nicolo Melli', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Kristaps Porziņgis', 'Kristaps Porzingis', df['Name'])

    return df



def moving_average(df, metric, n_days):
    avg_metric_last_n = []
    for i in tqdm(range(df.shape[0])):
        #find the date and the name for that row
        date = df.loc[i, 'Date']
        name = df.loc[i, 'Name']
        season = df.loc[i, 'Season']

        #create a dataframe for that player only
        df_name = df[(df.Name == name)&(df.Season == season)].reset_index(drop=True)
        #find the index of the current row's date in df_name
        index = df_name.loc[df_name['Date']==date].index[0]

        if index > n_days-1:
            #create df_past for all games before index
            df_past = df_name[index-n_days:index].reset_index(drop=True)

            #count number of days between current game and previous game
            last_n_average = df_past[metric].mean()

            avg_metric_last_n.append(last_n_average)
        else:
            avg_metric_last_n.append(0)

    column_name = 'average_' + metric + '_last_' + str(n_days)
    df[column_name] = ' '
    df[column_name] = list(avg_metric_last_n)

    return df


def apply_feature_eng(df, season):
    '''
    applies feature engineering to raw data and prepares it for model input
    '''

    df['Team'] = df.Team_x
    df.drop(['Team_x', 'Team_y'], axis=1, inplace=True)

    df['Season'] = season

    df.reset_index(drop=True, inplace=True)
    df.sort_values(by='Date', inplace=True)

    # calculate Double-Double
    df['DD'] = df.apply(lambda x: dd(x), axis=1)

    # calculate Triple Double
    df['TD'] = df.apply(lambda x: td(x), axis=1)

    # calculate FPTS
    df['FPTS'] = df['PTS'] + 1.5 * df['AST'] + 1.25 * df['TRB'] + 0.5 * df[
        '3P'] + 2 * df['STL'] + 2 * df['BLK'] + (-1) * df['TOV'] + 1.5 * df['DD'] + 3 * \
                 df['TD']
    # calculate Value
    df['Value'] = df['FPTS'] / (df['Salary'] / 1000)

    # calculate TS%
    df['TS_perc'] = df['PTS'] / 2 * (df['FGA'] + 0.44 * df['FTA'])

    #calulate FPTS per min
    df['fptspermin'] = df['FPTS'] / df['MP']

    # calculate rest days
    df = rest_days(df)

    #calculate average fpts last 5, 10, 15, 20, 30
    df = moving_average(df, 'FPTS', 5)
    df = moving_average(df, 'FPTS', 10)
    df = moving_average(df, 'FPTS', 15)
    df = moving_average(df, 'FPTS', 20)
    df = moving_average(df, 'FPTS', 30)

    #calculate average min last 1, 3, 5, 10, 30
    df = moving_average(df, 'MP', 1)
    df = moving_average(df, 'MP', 3)
    df = moving_average(df, 'MP', 5)
    df = moving_average(df, 'MP', 10)
    df = moving_average(df, 'MP', 30)

    # find opponent
    df['opp'] = np.where(df['Team'] == df['W'], df['L'], df['W'])

    # calculate dvp
    # defence of the opponent team vs the position of the player in that row
    # defence means average fpts scored by all players of that position against that team
    dvp_df = df.groupby(['Season', 'opp', 'Pos']).FPTS.mean().reset_index()
    dvp_df['DVP'] = dvp_df['FPTS']
    dvp_df.drop('FPTS', axis=1, inplace=True)

    # merge w/ df
    df = pd.merge(df, dvp_df, how='left', on=['Season', 'opp', 'Pos'])

    # make W, L binary variables
    df['W'] = np.where(df['Team'] == df['W'], 1, 0)
    df['L'] = np.where(df['Team'] == df['L'], 1, 0)

    # fill na and ' '
    df.Starter.fillna(0, inplace=True)
    df.Starter = df.Starter.astype(int)
    df.Value.replace(' ', 0, inplace=True)

    '''Numerical and One-Hot Coding of Categorical variables'''
    le = LabelEncoder()
    # New variable for season
    df['season_le'] = le.fit_transform(df['Season'])

    #calculate Value
    df['Value'] = df['FPTS'] / (df['Salary'] / 1000)

    #calculate average value last 1, 3, 5, 10, 20, 30
    df = moving_average(df, 'Value', 1)
    df = moving_average(df, 'Value', 3)
    df = moving_average(df, 'Value', 5)
    df = moving_average(df, 'Value', 10)
    df = moving_average(df, 'Value', 20)
    df = moving_average(df, 'Value', 30)

    #calculate average min last 1, 3, 5, 10, 30
    df = moving_average(df, 'USG_perc', 1)
    df = moving_average(df, 'USG_perc', 3)
    df = moving_average(df, 'USG_perc', 5)
    df = moving_average(df, 'USG_perc', 10)
    df = moving_average(df, 'USG_perc', 20)
    df = moving_average(df, 'USG_perc', 30)

    #some more metrics
    df = moving_average(df, 'FGA', 10)
    df = moving_average(df, 'FGA', 1)
    df = moving_average(df, 'FGA', 5)
    df = moving_average(df, 'FPTS', 1)

    return df


def find_season(row):
    '''finds the season of each row using the date'''
    if row >= 20141028 and row <= 20150415:
        season = '2014-15'
    elif row >= 20151027 and row <= 20160413:
        season = '2015-16'
    elif row >= 20161025 and row <= 20170412:
        season = '2016-17'
    elif row >= 20171017 and row <= 20180411:
        season = '2017-18'
    elif row >= 20181016 and row <= 20190410:
        season = '2018-19'
    elif row >= 20191022 and row <= 20200410:
        season = '2019-20'
    elif row >= 20201222 and row <= 20210406:
        season = '2020-21'
    else:
        season = ''

    return season

# move to util
# rename players to their Draftkings names
def rename_to_dk(df):
    df['Name'] = np.where(df['Name'] == 'Michael Porter', 'Michael Porter Jr.', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Shaquille Harrison', 'Shaq Harrison', df['Name'])
    df['Name'] = np.where(df['Name'] == 'P.J. Washington', 'PJ Washington', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Vernon Carey', 'Vernon Carey Jr.', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Juan Hernangomez', 'Juancho Hernangomez', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Gary Trent', 'Gary Trent Jr.', df['Name'])
    df['Name'] = np.where(df['Name'] == "DeAndre' Bembry", 'DeAndre Bembry', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Dewayne Dedmon', 'Dewayne Dedmon', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Tim Hardaway', 'Tim Hardaway Jr.', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Xavier Tillman', 'Xavier Tillman Sr.', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Troy Brown', 'Troy Brown Jr.', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Anthony Tolliver', 'Anthony Tolliver', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Moritz Wagner', 'Moe Wagner', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Wendell Carter', 'Wendell Carter Jr.', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Mohamed Bamba', 'Mo Bamba', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Luguentz Dort', 'Lu Dort', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Sviatoslav Mykhailiuk', 'Svi Mykhailiuk', df['Name'])
    df['Name'] = np.where(df['Name'] == 'Marvin Bagley', 'Marvin Bagley III', df['Name'])

    return df
        
        
        