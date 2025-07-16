def classification_traditional(indep, dep, model_name, **params):

    from sklearn.model_selection import train_test_split

    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import MultinomialNB, GaussianNB, CategoricalNB, BernoulliNB, ComplementNB
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC

    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import classification_report

    # Split into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(indep, dep, test_size=0.30, random_state=10)

    # Create and train the classifier

    if model_name == "LogisticRegression":
        print("Using Logistic Regression")
        model=LogisticRegression(**params)
    elif model_name == 'KNeighborsClassifier':
        print("Using K-Neighbors Classifier")
        model = KNeighborsClassifier(**params)
    elif model_name == 'RandomForestClassifier':
        print("Using Random Forest Classifier")
        model = RandomForestClassifier(**params)
    elif model_name == 'DecisionTreeClassifier':
        print("Using Decision Tree Classifier")
        model = DecisionTreeClassifier(**params)
    elif model_name == 'SVC':
        print("Using Support Vector Classifier")
        model = SVC(**params)
    elif model_name == 'MultinomialNB':
        print("Using Multinomial Naive Bayes")
        model = MultinomialNB(**params)
    elif model_name == 'GaussianNB':
        print("Using Gaussian Naive Bayes")
        model = GaussianNB(**params)
    elif model_name == 'BernoulliNB':
        print("Using Bernoulli Naive Bayes")
        model = BernoulliNB(**params)
    elif model_name == 'CategoricalNB':
        print("Using Categorical Naive Bayes")
        model = CategoricalNB(**params)
    elif model_name == 'ComplementNB':
        print("Using Complement Naive Bayes")
        model = ComplementNB(**params)
    elif model_name == 'AdaBoostClassifier':
        print("Using AdaBoost Classifier")
        model = AdaBoostClassifier(**params)
    elif model_name == 'GradientBoostingClassifier':
        print("Using Gradient Boosting Classifier")
        model = GradientBoostingClassifier(**params)
    elif model_name == 'XGBClassifier':
        print("Using XGBoost Classifier")
        model = XGBClassifier(**params)
    elif model_name == 'LGBMClassifier':
        print("Using LightGBM Classifier")
        model = LGBMClassifier(**params)
        


    else:
        print(f"Unsupported model_name: {model_name}")
        raise ValueError(f"Unsupported model_name: {model_name}")


    classifier = model
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    conf_mat = confusion_matrix(y_test, y_pred)
    classific_report = classification_report(y_test, y_pred, zero_division=1)

    print("Confusion Matrix:")
    for i in conf_mat:
        print(i)

    print("Classification Report:\n", classific_report)
    return classifier