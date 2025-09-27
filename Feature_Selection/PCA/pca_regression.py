# Importing the libraries

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA

def run_all_regressors(X, y, comp_no):
    X_train, X_test, y_train, y_test, explained_variance = pca_and_scale(X, y, comp_no)
    # Classifiers dictionary for easy iteration
    regressors = {
        'Linear': LinearRegression(),
        'Ridge': Ridge(random_state=0),
        'SVMl': SVR(kernel='linear'),
        'SVMnl': SVR(kernel='rbf'),
        'KNN': KNeighborsRegressor(n_neighbors=5),
        'DecisionTree': DecisionTreeRegressor(random_state=10),
        'RandomForest': RandomForestRegressor(n_estimators=10, random_state=0)
    }
    # Evaluate each classifier and store accuracy
    results = {'No_Of_Components': comp_no}
    for name, reg in regressors.items():
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        r2_scores= r2_score(y_test, y_pred)
        results[name] = r2_scores
    return results


def pca_and_scale(X, y, comp_no):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)
    pca = PCA(n_components = comp_no)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    explained_variance = pca.explained_variance_ratio_

    return X_train, X_test, y_train, y_test, explained_variance

def pca_regressors(indep_X, dep_Y, comp_no):
    row = run_all_regressors(indep_X, dep_Y, comp_no)
    dataframe = pd.DataFrame([row])
    return dataframe
