# Importing the libraries

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

def run_all_classifiers(X, y, comp_no):
    X_train, X_test, y_train, y_test, explained_variance = pca_and_scale(X, y, comp_no)
    # Classifiers dictionary for easy iteration
    classifiers = {
        'Logistic': LogisticRegression(random_state=0),
        'SVMl': SVC(kernel='linear', random_state=0),
        'SVMnl': SVC(kernel='rbf', random_state=0),
        'KNN': KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2),
        'Navie': GaussianNB(),
        'Decision': DecisionTreeClassifier(criterion='entropy', random_state=0),
        'Random': RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    }
    # Evaluate each classifier and store accuracy
    results = {'No_Of_Components': comp_no}
    for name, clf in classifiers.items():
        # acc = train_and_score(clf, X_train, y_train, X_test, y_test)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc= accuracy_score(y_test, y_pred)
        results[name] = acc
    return results


def pca_and_scale(X, y, comp_no):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    pca = PCA(n_components = comp_no)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    explained_variance = pca.explained_variance_ratio_

    return X_train, X_test, y_train, y_test, explained_variance

def pca_classifiers(indep_X, dep_Y, comp_no):
    # Get classification results as one-row DataFrame
    row = run_all_classifiers(indep_X, dep_Y, comp_no)
    dataframe = pd.DataFrame([row])
    return dataframe
