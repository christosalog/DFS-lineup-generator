
# Hyperparameters
# Lasso hyperparameters
LASSO_HP = {
    'lasso__alpha': [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
}

# Ridge hyperparameters
RIDGE_HP = {
    'ridge__alpha': [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
}

# Elastic Net hyperparameters
ENET_HP = {
    'elasticnet__alpha': [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],
    'elasticnet__l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]
}

# Random forest hyperparameters
RF_HP = {
    'randomforestregressor__n_estimators': [100, 200],
    'randomforestregressor__max_features': ['auto', 'sqrt', 0.33],
}

# Boosted tree hyperparameters
GB_HP = {
    'gradientboostingregressor__n_estimators': [100, 200],
    'gradientboostingregressor__learning_rate': [0.05, 0.1, 0.2],
    'gradientboostingregressor__max_depth': [1, 3, 5]
}

# xgboost tree hyperparameters
XGB_HP = {
    'xgbregressor__n_estimators': [100, 200, 500],
    'xgbregressor__min_child_weight': [0, 3, 5],
    'xgbregressor__max_depth': [1, 5, 20, 30, 50],
    'xgbregressor__colsample_bytree': [0.7, 1.0],
    'xgbregressor__colsample_bylevel': [0.8, 1.0],
    'xgbregressor__subsample': [0.8, 1.0],
    'xgbregressor__learning_rate': [0.001, 0.5, 0.999],
    'xgbregressor__gamma': [0, 0.5, 1.0]
}

