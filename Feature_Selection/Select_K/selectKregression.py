import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def prepare_data(indep_X, dep_Y, k_no, test_size=0.25, random_state=10):
    selector = SelectKBest(score_func=f_regression, k=k_no)
    X_selected = selector.fit_transform(indep_X, dep_Y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, dep_Y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return r2

def run_regressors(indep_X, dep_Y, k_no):
    X_train, X_test, y_train, y_test = prepare_data(indep_X, dep_Y, k_no)

    regressors = {
        'Linear': LinearRegression(),
        'Ridge': Ridge(random_state=0),
        'SVMl': SVR(kernel='linear'),
        'SVMnl': SVR(kernel='rbf'),
        'KNN': KNeighborsRegressor(n_neighbors=5),
        'DecisionTree': DecisionTreeRegressor(random_state=10),
        'RandomForest': RandomForestRegressor(n_estimators=10, random_state=0)
    }

    results = {'K_No': k_no}
    for name, model in regressors.items():
        r2 = evaluate_model(model, X_train, y_train, X_test, y_test)
        results[f'{name}_R2'] = r2

    return pd.DataFrame([results], index=['F_regression'])

# Example usage:
# df_results = run_regressors(indep_X, dep_Y, k_no=5)


# # kbest=selectkbest(indep_X,dep_Y,5)      
# def selectk_regression(indep_X,dep_Y, k_no):
#     acclin=[]
#     accsvml=[]
#     accsvmnl=[]
#     accdes=[]
#     accrf=[]

#     X_train, X_test, y_train, y_test=kbest_scaler(indep_X,dep_Y, k_no)  
#     # for i in kbest:   
#     r2_lin=Linear(X_train,y_train,X_test, y_test)
#     acclin.append(r2_lin)
    
#     r2_sl=svm_linear(X_train,y_train,X_test, y_test)    
#     accsvml.append(r2_sl)
    
#     r2_NL=svm_NL(X_train,y_train,X_test, y_test)
#     accsvmnl.append(r2_NL)
    
#     r2_d=Decision(X_train,y_train,X_test, y_test)
#     accdes.append(r2_d)
    
#     r2_r=random(X_train,y_train,X_test, y_test)
#     accrf.append(r2_r)

    
#     result=selectk_regression(k_no,acclin,accsvml,accsvmnl,accdes,accrf)



#     return result