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


def kbest_scaler(indep_X,dep_Y, k_no):
    test = SelectKBest(score_func=chi2, k=k_no)
    fit1= test.fit(indep_X,dep_Y)
    selectk_features = fit1.transform(indep_X)

    X_train, X_test, y_train, y_test = train_test_split(selectk_features, dep_Y, test_size = 0.25, random_state = 10)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)    
    return X_train, X_test, y_train, y_test

def cm_prediction(classifier, X_test, y_test):
    y_pred = classifier.predict(X_test)
    Accuracy=accuracy_score(y_test, y_pred )
    return  Accuracy

def logistic(X_train, y_train, X_test, y_test):       

    classifier = LogisticRegression(random_state = 0)
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy     
    
def svm_linear(X_train, y_train, X_test, y_test):
                
    classifier = SVC(kernel = 'linear', random_state = 0)
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy
    
def svm_NL(X_train, y_train, X_test, y_test):
                
    classifier = SVC(kernel = 'rbf', random_state = 0)
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy
   
def Navie(X_train, y_train, X_test, y_test):       

    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy         
    
def knn(X_train, y_train, X_test, y_test):
           
    classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy

def Decision(X_train, y_train, X_test, y_test):
        
    classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy      

def random(X_train, y_train, X_test, y_test):
        
    classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
    classifier.fit(X_train, y_train)
    Accuracy=cm_prediction(classifier, X_test, y_test)
    return  Accuracy

def selectk_class_result(k_no,acclog,accsvml,accsvmnl,accknn,accnav,accdes,accrf): 
    
    dataframe=pd.DataFrame(index=['ChiSquare'],columns=['K_No','Logistic','SVMl','SVMnl','KNN','Navie','Decision','Random'])
    for number,idex in enumerate(dataframe.index):      
        dataframe.loc[idex, 'K_No'] = k_no
        dataframe.loc[idex, 'Logistic'] = acclog[number]
        dataframe.loc[idex, 'SVMl'] = accsvml[number]
        dataframe.loc[idex, 'SVMnl'] = accsvmnl[number]
        dataframe.loc[idex, 'KNN'] = accknn[number]
        dataframe.loc[idex, 'Navie'] = accnav[number]
        dataframe.loc[idex, 'Decision'] = accdes[number]
        dataframe.loc[idex, 'Random'] = accrf[number]

    return dataframe


def selectk_Classification(indep_X,dep_Y, k_no):
    acclog=[]
    accsvml=[]
    accsvmnl=[]
    accknn=[]
    accnav=[]
    accdes=[]
    accrf=[]

    X_train, X_test, y_train, y_test=kbest_scaler(indep_X,dep_Y, k_no)   
        
    Accuracy=logistic(X_train, y_train, X_test, y_test)
    acclog.append(Accuracy)

    Accuracy=svm_linear(X_train, y_train, X_test, y_test)  
    accsvml.append(Accuracy)
        
    Accuracy=svm_NL(X_train, y_train, X_test, y_test)  
    accsvmnl.append(Accuracy)
        
    Accuracy=knn(X_train, y_train, X_test, y_test)  
    accknn.append(Accuracy)
        
    Accuracy=Navie(X_train, y_train, X_test, y_test)  
    accnav.append(Accuracy)
        
    Accuracy=Decision(X_train, y_train, X_test, y_test)  
    accdes.append(Accuracy)
        
    Accuracy=random(X_train, y_train, X_test, y_test)  
    accrf.append(Accuracy)
        
    result=selectk_class_result(k_no,acclog,accsvml,accsvmnl,accknn,accnav,accdes,accrf)

    return result