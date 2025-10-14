import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, classification_report, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from imblearn.over_sampling import SMOTE
import pandas as pd

def get_model(model_name):
    models = {
        'LogisticRegression': LogisticRegression(class_weight='balanced'),
        'SVC': SVC(probability=True, class_weight='balanced'),
        'RandomForestClassifier': RandomForestClassifier(class_weight='balanced'),
        'DecisionTreeClassifier': DecisionTreeClassifier(class_weight='balanced'),
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
    model = get_model(model_name)
    # Use stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=10, stratify=y
    )
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # Balance classes in training data using SMOTE
    smote = SMOTE(random_state=10)
    X_train, y_train = smote.fit_resample(X_train, y_train)
    print(f"Running {model_name} with Grid Search...")
    grid = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring='f1_weighted',
        n_jobs=-1,
        cv=5,
        refit=True
    )
    grid.fit(X_train, y_train)
    y_pred = grid.predict(X_test)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)
    if hasattr(grid, "predict_proba"):
        if len(set(y_test)) > 2:
            roc_auc = roc_auc_score(y_test, grid.predict_proba(X_test), multi_class='ovr')
        else:
            roc_auc = roc_auc_score(y_test, grid.predict_proba(X_test)[:, 1])
    else:
        roc_auc = None
    print(f"\nBest Parameters: {grid.best_params_}")
    print(f"F1 Score (weighted): {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    print("Classification Report:\n", cr)
    if roc_auc is not None:
        print(f"ROC AUC Score: {roc_auc:.4f}")
    print('-' * 65)
    return grid, f1, roc_auc

