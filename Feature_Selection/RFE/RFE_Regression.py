import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score 

def rfeFeature(indep_X, dep_Y, n_features):
    rfelist = []
    features_list = []

    models = [
        LinearRegression(),
        SVR(kernel='linear'),
        RandomForestRegressor(n_estimators=10, random_state=10),
        DecisionTreeRegressor(random_state=10)
    ]

    for model in models:
        rfe = RFE(model, n_features_to_select=n_features)
        rfe_fit = rfe.fit(indep_X, dep_Y)
        selected_features = list(indep_X.columns[rfe_fit.get_support(True)])

        transformed_df = indep_X[selected_features]

        rfelist.append(transformed_df)
        features_list.append(selected_features)

    return rfelist, features_list

def rfe_regression(rfe_results, features_list, dep_Y):
    rfe_models = ['LogisticRFE', 'SVCRFE', 'RandomForestRFE', 'DecisionTreeRFE']
    
    rows = []

    for number, rfe_df in enumerate(rfe_results):
        X_train, X_test, y_train, y_test = train_test_split(rfe_df, dep_Y, test_size=0.25, random_state=10)
        r2_scores = all_regressors(X_train, X_test, y_train, y_test)

        row_data = {
            'No_of_Features': len(features_list[number]),
            'RFE_Model': rfe_models[number],
            'Selected_Features': ", ".join(features_list[number])
        }
        row_data.update(r2_scores)  
        
        rows.append(row_data)

    rfedataframe = pd.DataFrame(rows, 
        columns=[ 'No_of_Features', 'RFE_Model', 'Selected_Features', 
                 'Logistic', 'SVMl', 'Decision', 'Random']
    )

    return rfedataframe



def all_regressors(X_train, X_test, y_train, y_test):
    r2_scores = {}
    regressors = {
        'Logistic': LinearRegression(),
        'SVMl': SVR(kernel='linear'),
        'Decision': DecisionTreeRegressor(),
        'Random': RandomForestRegressor(n_estimators=10)
    }

    for name, reg in regressors.items():
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        r2_scores[name] = r2_score(y_test, y_pred)

    return r2_scores

