# Load and Data Preprocessing

def load_and_preprocess_data(file_path, index_col):
    import pandas as pd

    df = pd.read_csv(file_path, index_col=index_col)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    # Data Preprocessing
    df.dropna(inplace=True)

    df['Description'] = df['Description'].astype(str)
    df['Cleaned_Desc'] = df['Description'].apply(clean_text)
    return df

# Basic text preprocessing

def clean_text(text):
    import re  # Regular expressions
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    stop_words = set(stopwords.words("english"))
   
    # Convert to lowercase
    text = text.lower()
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize
    tokens = word_tokenize(text)
    # Lemmatize and remove stop words
    lemmatizer = WordNetLemmatizer()
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words and len(word) > 2
    ]

    cleaned_text = " ".join(tokens)

    return cleaned_text

def coherence_score(model, vectorizer, texts, dictionary, topn=10):
    from gensim.models import CoherenceModel

    feature_names = vectorizer.get_feature_names_out()
    
    topics = []
    for topic in model.components_:
        top_words = [feature_names[i] for i in topic.argsort()[-topn:]]
        topics.append(top_words)

    cm = CoherenceModel(
        topics=topics,
        texts=texts,
        dictionary=dictionary,
        coherence='c_v'
    )
    return cm.get_coherence()

def get_model(model_name):
    from sklearn.linear_model import LogisticRegression, RidgeClassifier, Perceptron, SGDClassifier
    from sklearn.svm import LinearSVC
    from sklearn.neighbors import NearestCentroid
    from sklearn.naive_bayes import MultinomialNB, BernoulliNB

    models = {
        'LogisticRegression': LogisticRegression(),
        'LinearSVC': LinearSVC(),
        'RidgeClassifier': RidgeClassifier(),
        'Perceptron': Perceptron(),
        'NearestCentroid': NearestCentroid(),
        'SGDClassifier': SGDClassifier(),
        'MultinomialNB': MultinomialNB(),
        'BernoulliNB': BernoulliNB()
    }
    return models[model_name]

def run_classification_model(X_train_vec, y_train, X_test_vec, y_test, model_name, param_grid, grid_cv):
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.metrics import confusion_matrix, classification_report, f1_score, roc_auc_score
    from sklearn.preprocessing import label_binarize

    model = get_model(model_name)
    grid = GridSearchCV(model, param_grid, scoring='f1_weighted', cv=grid_cv, n_jobs=-1, refit=True, error_score='raise')
    grid.fit(X_train_vec, y_train)
    y_pred = grid.predict(X_test_vec)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)

    # ROC AUC
    if len(set(y_test)) > 2:
        if hasattr(grid.best_estimator_, "predict_proba"):
            roc_auc = roc_auc_score(y_test, grid.predict_proba(X_test_vec), multi_class='ovr')
        else:
            scores = grid.decision_function(X_test_vec)
            roc_auc = roc_auc_score(label_binarize(y_test, classes=np.unique(y_test)), scores, multi_class='ovr')
    else:
        if hasattr(grid.best_estimator_, "predict_proba"):
            roc_auc = roc_auc_score(y_test, grid.predict_proba(X_test_vec)[:,1])
        else:
            scores = grid.decision_function(X_test_vec)
            roc_auc = roc_auc_score(y_test, scores)
    
    # Output Results
    print('.' * 25)
    print(f"{model_name} \nBest Parameters: {grid.best_params_}")
    print(f"F1 Score (weighted):{f1:.4f} \nROC AUC Score:{roc_auc:.4f}")
    print("Confusion Matrix:\n", cm)
    print("Classification Report:\n", cr)


    return grid, f1, roc_auc

impact_words = [
    "fraud", "scam", "probe", "investigat", "embezzle",
    "default", "npas?", "loan", "bailout", "bankrupt", "insolv",
    "crash", "slump", "selloff", "volatility",
    "merger", "acquisit", "takeover",
    "layoff", "retrench", "shutdown", "closure",
    "penalty", "fine", "sanction", "audit",
    "ban", "restriction", "regulatory",
    "policy", "inflation", "rate", "budget"
]


def impact_label(text, topic):
    import re
    text = text.lower()

    hit = any(re.search(w, text) for w in impact_words)

    very_sensitive = ["policy", "rates"]
    sensitive = ["markets", "earnings"]

    if topic in very_sensitive:
        return "High Impact"

    if hit and topic in sensitive:
        return "High Impact"

    if hit:
        return "High Impact"

    return "Routine"
