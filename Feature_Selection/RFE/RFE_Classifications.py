import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier   
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score 


# -------------------------------
# Feature Selection with RFE (returns DataFrame, not NumPy)
# -------------------------------
def rfeFeature(indep_X, dep_Y, n_features):
    rfelist = []
    features_list = []

    models = [
        LogisticRegression(solver='lbfgs', max_iter=500),
        SVC(kernel='linear', random_state=0),
        RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0),
        DecisionTreeClassifier(criterion='gini', max_features='sqrt', splitter='best', random_state=0)
    ]

    for model in models:
        print(f"Running RFE with: {model.__class__.__name__}")
        rfe = RFE(model, n_features_to_select=n_features)
        rfe_fit = rfe.fit(indep_X, dep_Y)
        selected_features = list(indep_X.columns[rfe_fit.get_support(True)])

        # Keep it as a DataFrame with column names
        transformed_df = indep_X[selected_features]

        rfelist.append(transformed_df)
        features_list.append(selected_features)

    return rfelist, features_list


# -------------------------------
# Train-Test Split
# -------------------------------
def split_scalar(indep_X, dep_Y):
    X_train, X_test, y_train, y_test = train_test_split(indep_X, dep_Y, test_size=0.25, random_state=10)
    return X_train, X_test, y_train, y_test


# -------------------------------
# Benchmark all classifiers
# -------------------------------
def all_classifiers(X_train, X_test, y_train, y_test):
    accuracy_scores = {}
    classifiers = {
        'Logistic': LogisticRegression(random_state=10, max_iter=500),
        'SVMl': SVC(kernel='linear', random_state=0),
        'SVMnl': SVC(kernel='rbf', random_state=0),
        'KNN': KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2),
        'Naive': GaussianNB(),
        'Decision': DecisionTreeClassifier(criterion='entropy', random_state=0),
        'Random': RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    }

    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy_scores[name] = accuracy_score(y_test, y_pred)

    return accuracy_scores


# -------------------------------
# Collect results into DataFrame
# -------------------------------
def rfe_classification(rfe_results, features_list, dep_Y):
    rfedataframe = pd.DataFrame(
        index=['LogisticRFE', 'SVCRFE', 'RandomForestRFE', 'DecisionTreeRFE'],
        columns=['Selected_Features', 'Logistic', 'SVMl', 'SVMnl', 'KNN', 'Naive', 'Decision', 'Random']
    )

    for number, rfe_df in enumerate(rfe_results):
        X_train, X_test, y_train, y_test = split_scalar(rfe_df, dep_Y)
        accuracies = all_classifiers(X_train, X_test, y_train, y_test)

        # Save feature names as a string
        rfedataframe.loc[rfedataframe.index[number], 'Selected_Features'] = ", ".join(features_list[number])

        # Save classifier accuracies
        for clf_name, acc in accuracies.items():
            rfedataframe.loc[rfedataframe.index[number], clf_name] = acc

    return rfedataframe





