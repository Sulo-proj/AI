from sklearn.linear_model import *
from sklearn.ensemble import *
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def scale_data(X_train, X_test=None):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
    else:
        X_test_scaled = None
    return X_train_scaled, X_test_scaled, scaler

def run_regression_model(model_name, X, y, param_grid=None, test_size=0.3, n_folds=5, scoring='r2', verbose=1):

    model_map = {
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(),
        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'QuantileRegressor': QuantileRegressor(),
        'SGDRegressor': SGDRegressor(),
        'DecisionTreeRegressor': DecisionTreeRegressor(),
        'RandomForestRegressor': RandomForestRegressor(),
        'GradientBoostingRegressor': GradientBoostingRegressor(),
        'SVR': SVR()
    }

    if model_name not in model_map:
        raise ValueError(f"Unsupported model '{model_name}'")

    model = model_map[model_name]

    # Scale if needed
    scalers = None
    if model_name in ['SVR', 'SGDRegressor', 'QuantileRegressor']:
        X, _, x_scaler = scale_data(X)
        if model_name == 'QuantileRegressor':
            y = y.reshape(-1, 1) if y.ndim == 1 else y
            y, _, y_scaler = scale_data(y)
            y = y.ravel()
            scalers = (x_scaler, y_scaler)
        else:
            scalers = x_scaler

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=10)

    if param_grid is None or model_name == 'LinearRegression':
        # Run cross_val_score
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=10)
        scores = cross_val_score(model, X_train, y_train, scoring=scoring, cv=kf)
        print(f"Cross-Validation {scoring.upper()} Scores: {scores}")
        print("Mean Score:", np.mean(scores))
        model.fit(X_train, y_train)
        return model, np.mean(scores), scalers
    else:
        # GridSearchCV
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=10)
        grid = GridSearchCV(model, param_grid, cv=kf, scoring=scoring, verbose=verbose, n_jobs=-1, return_train_score=True)
        grid.fit(X_train, y_train)

        result_df = pd.DataFrame(grid.cv_results_)
        param_cols = [f'param_{k}' for k in param_grid]
        final_cols = param_cols + ['mean_test_score', 'std_test_score', 'rank_test_score']
        print(result_df[final_cols].sort_values(by='rank_test_score').head())
        print("Best Parameters:", grid.best_params_)
        print("Best Score:", grid.best_score_)

        return grid.best_estimator_, grid.best_score_, scalers
