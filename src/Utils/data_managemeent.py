import pandas as pd


#think about how to incorporate VERSION
def load_dataset(file, params):
    data = pd.read_csv(file)
    train_data = data[(data.Date >= params['start_date'])|(data.Date >= params['end_date'])]

    return train_data
