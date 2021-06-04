import os
dirpath = os.path.dirname(os.path.abspath(__file__))
print(dirpath)
TRAIN_PATH = os.path.join(dirpath, 'data', 'season_data_2021.csv')

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

TRAINED_MODEL = os.path.join(dirpath, 'prod_models', 'final_model_rf_2021-04-15.pickle')
