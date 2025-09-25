import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def kbest_and_scale(X, y, k_no):
    # SelectKBest feature selection
    selector = SelectKBest(score_func=chi2, k=k_no)
    X_new = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support(indices=True)]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.25, random_state=10)
    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test, selected_features

def train_and_score(classifier, X_train, y_train, X_test, y_test):
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    return accuracy_score(y_test, y_pred)

def run_all_classifiers(X, y, k_no):
    X_train, X_test, y_train, y_test, selected_features = kbest_and_scale(X, y, k_no)
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
    results = {'K_No': k_no}
    for name, clf in classifiers.items():
        acc = train_and_score(clf, X_train, y_train, X_test, y_test)
        results[name] = acc
    return results, selected_features

def selectk_Classification(indep_X, dep_Y, k_no):
    # Get classification results as one-row DataFrame
    row, selected_features = run_all_classifiers(indep_X, dep_Y, k_no)
    row['Selected_Features'] = ', '.join(selected_features)
    dataframe = pd.DataFrame([row], index=['ChiSquare'])
    return dataframe

