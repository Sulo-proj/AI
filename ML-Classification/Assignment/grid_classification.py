import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (confusion_matrix, classification_report, 
                             f1_score, roc_auc_score)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.svm import SVC

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


def get_model(model_name):
    """Return the classifier instance based on the given model name."""
    models = {
        'LogisticRegression': LogisticRegression(),
        'SVC': SVC(probability=True),
        'RandomForestClassifier': RandomForestClassifier(),
        'DecisionTreeClassifier': DecisionTreeClassifier(),
        'KNeighborsClassifier': KNeighborsClassifier(),
        'XGBClassifier': XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        'LGBMClassifier': LGBMClassifier(),
        'CatBoostClassifier': CatBoostClassifier(),
        'AdaBoostClassifier': AdaBoostClassifier(),
        'GaussianNB': GaussianNB(),
        'MultinomialNB': MultinomialNB(),
        'BernoulliNB': BernoulliNB()
    }
    
    if model_name not in models:
        raise ValueError(f"Model '{model_name}' is not supported.")
    
    return models[model_name]


def run_classification_model(X, y, model_name, param_grid):
    """Train, evaluate and return the best classifier using GridSearchCV."""
    
    model = get_model(model_name)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=10
    )

    # Standardize features (skip for count-based Naive Bayes)
    if model_name not in ['MultinomialNB', 'ComplementNB', 'CategoricalNB']:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    print(f"Running {model_name} with Grid Search...")

    # Grid Search
    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='f1_weighted',
        n_jobs=-1,
        cv=5,
        refit=True
    )
    grid.fit(X_train, y_train)

    # Predict
    y_pred = grid.predict(X_test)

    # Evaluation
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)

    roc_auc = roc_auc_score(y_test, grid.predict_proba(X_test)[:, 1])


    # Output Results
    print(f"\nBest Parameters: {grid.best_params_}")
    print(f"F1 Score (weighted): {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    print("Classification Report:\n", cr)
    print(f"ROC AUC Score: {roc_auc:.4f}")
    
    print('-' * 65)
    
    return grid, f1, roc_auc
