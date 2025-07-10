
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor



### Function to split the dataset into training and testing sets
def split_traintest(X, y, test_size=0.30):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = 10)

    return X_train, X_test, y_train, y_test

### Function to scale the data using StandardScaler
def scale_data(Xy_train, Xy_test=None):

    st_scaler = StandardScaler()
    Xy_train = st_scaler.fit_transform(Xy_train)
    if Xy_test is not None:
        Xy_test = st_scaler.transform(Xy_test)

    return Xy_train, Xy_test, st_scaler

### Used Linear Regression with Cross-Validation 
def lin_reg(X,y, n_folds=5, my_test_size=0.30, my_scoring='r2'):
    
    X_train,X_test,y_train,y_test=split_traintest(X, y, test_size=my_test_size)

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=10)

    # Linear regression model
    lin_regressor = LinearRegression()

    # Evaluate using cross_val_score
    scores = cross_val_score(lin_regressor, X, y, cv=kf, scoring=my_scoring)
    scores_df = pd.DataFrame(scores, columns=['R2_Score'])

    print("No. of folds:", kf.get_n_splits())
    print("R² Scores for each fold:", scores_df)
    print("Average R² Score:", np.mean(scores))

    lin_model = lin_regressor.fit(X_train, y_train)

    return lin_model, np.mean(scores)



### SVR, Decision Tree and Random Forest Regression with Grid Search CV
def regress(reg_model, X, y, param_grid, n_folds=10, scoring_method='r2'):
    print('Model Selected :',reg_model)

    print_msg = 'Model does not require scaling.'
    st_scaler = None
    if reg_model == 'DecisionTreeRegressor':
        model = DecisionTreeRegressor()
    elif reg_model == 'RandomForestRegressor':
        model = RandomForestRegressor()
    elif reg_model == 'SVR':
        print_msg = 'Scaling the data using StandardScaler...'
        X, _, st_scaler = scale_data(X)
        model = SVR()
    else:
        raise ValueError("Unsupported regression model type.")

    print(print_msg)

    arg_cv = KFold(n_splits=n_folds, shuffle=True, random_state=10)
    # print(X, arg_cv)

    model_grid = GridSearchCV(
        model,
        param_grid,
        scoring=scoring_method,
        refit=True,
        verbose=3,
        n_jobs=-1,
        cv=arg_cv,
        return_train_score=True
    )
    
    reg_model = model_grid.fit(X, y) 

    grid_result=model_grid.cv_results_
    grid_result_df=pd.DataFrame.from_dict(grid_result)

    list(param_grid.keys())
    param_list = []
    for param in list(param_grid.keys()):
        param_list.append(f"param_{param}")
    param_list = param_list + ['mean_test_score', 'std_test_score', 'rank_test_score']

    # print(param_list)
    display_result = grid_result_df[param_list].sort_values(by='rank_test_score', ascending=True, ignore_index=True)

    print(display_result)
    print("The best parameter {}:".format(model_grid.best_params_))
    print("The R_score value for best parameter {}:".format(model_grid.best_score_))

    return reg_model, st_scaler

