import os
dirpath = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(dirpath, 'data', 'season_data_2021.csv')

season_dates = {
    '2014-15': [20141028, 20150415],
    '2015-16': [20151027, 20160413],
    '2016-17': [20161025, 20170412],
    '2017-18': [20171017, 20180411],
    '2018-19': [20181016, 20190410],
    '2019-20': [20191022, 20200410],
    '2020-21': [20201222, 20210516]
}


load_params = {"start_date": season_dates['2020-21'][0],"end_date":season_dates['2020-21'][1]}


TARGET = 'FPTS'

PREDICTORS = ['Salary', 'Starter',
              'Home', 'Rest',
              'average_FPTS_last_5', 'average_FPTS_last_10', 'average_FPTS_last_15',
              'average_FPTS_last_20', 'average_FPTS_last_30', 'average_MP_last_1',
              'average_MP_last_3', 'average_MP_last_5', 'average_MP_last_10',
              'average_MP_last_30', 'season_le', 'average_FPTS_last_1',
              'average_FGA_last_1', 'average_FGA_last_5', 'average_FGA_last_10',
              'average_Value_last_1', 'average_Value_last_3', 'average_Value_last_5', 'average_Value_last_10',
              'average_Value_last_20', 'average_Value_last_30',
              'average_USG_perc_last_1', 'average_USG_perc_last_3', 'average_USG_perc_last_5',
              'average_USG_perc_last_10', 'average_USG_perc_last_20', 'average_USG_perc_last_30']

TRAIN_TEST_SPLIT = 0.2

RANDOM_STATE = 123

TRAINED_MODEL_DIR = os.path.join(dirpath, 'models', 'trained_models/')

TRAINED_MODEL = os.path.join(dirpath, 'prod_models', 'final_model_rf_2021-04-15.pickle')

TRAIN_LOG = os.path.join(dirpath, 'data', 'model_training_log.csv')