import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

class Univariate:

    def quanQual(data):
        qual = [col for col in data.columns if data[col].dtype == 'object']
        quan = [col for col in data.columns if data[col].dtype != 'object']
        return quan, qual    

    
    def descriptive(data, quan):
        descriptive = pd.DataFrame(columns=quan)

        for columnName in quan:
            # Central tendency
            descriptive.loc['Mean', columnName] = data[columnName].mean().round(2)
            mode_val = data[columnName].mode()
            descriptive.loc['Mode', columnName] = mode_val[0] if not mode_val.empty else np.nan

            descriptive.loc["Min", columnName] = data[columnName].min()
            descriptive.loc["Q1-25th%", columnName] = data[columnName].quantile(0.25)
            descriptive.loc['Median / Q2-50%', columnName] = data[columnName].median()
            descriptive.loc["Q3-75th%", columnName] = data[columnName].quantile(0.75)
            descriptive.loc["99th%", columnName] = np.percentile(data[columnName], 99).round(2)
            descriptive.loc["Max-100th%", columnName] = data[columnName].max()
            
            # IQR and outlier ranges
            descriptive.loc["IQR", columnName] = descriptive[columnName]["Q3-75th%"] - descriptive[columnName]["Q1-25th%"]
            descriptive.loc["1.5rule", columnName] = 1.5 * descriptive[columnName]["IQR"]
            descriptive.loc["LesserRange", columnName] = descriptive[columnName]["Q1-25th%"] - descriptive[columnName]["1.5rule"]
            descriptive.loc["GreaterRange", columnName] = descriptive[columnName]["Q3-75th%"] + descriptive[columnName]["1.5rule"]
            descriptive.loc["Skew", columnName] = descriptive[columnName].skew().round(2)
            descriptive.loc["Kurtosis", columnName] = descriptive[columnName].kurtosis().round(2)
            descriptive.loc["Var", columnName] = descriptive[columnName].var().round(2)
            descriptive.loc["Std", columnName] = descriptive[columnName].std().round()
        return descriptive
    
    
    def detect_outliers(descriptive, quan):
        lesser = []
        greater = []
        for columnName in quan:
            min_val = descriptive[columnName]["Min"]
            max_val = descriptive[columnName]["Max-100th%"]
            lesser_range = descriptive[columnName]["LesserRange"]
            greater_range = descriptive[columnName]["GreaterRange"]

            is_lesser_outlier = lesser_range > min_val
            is_greater_outlier = greater_range < max_val

            descriptive.loc["LesserOutlier", columnName] = is_lesser_outlier
            descriptive.loc["GreaterOutlier", columnName] = is_greater_outlier

            if is_lesser_outlier:
                lesser.append(columnName)
            if is_greater_outlier:
                greater.append(columnName)

        return descriptive, lesser, greater


    def remove_outliers(descriptive, data, lesser, greater):
        for columnName in lesser:
            data.loc[data[columnName] < descriptive[columnName]["LesserRange"], columnName] = descriptive[columnName]["LesserRange"]
        for columnName in greater:
            data.loc[data[columnName] > descriptive[columnName]["GreaterRange"], columnName] = descriptive[columnName]["GreaterRange"]
        return data
    
    def freqTable(data, columnName):
        
        total = len(data)
        
        freq_series = data[columnName].value_counts()  
        freqTable = pd.DataFrame({
            "UniqueValues": freq_series.index,
            "Frequency": freq_series.values
        })
        freqTable["RelativeFrequency%"]=(freqTable["Frequency"]/total*100).round(2)
        freqTable["Cumsum%"]=freqTable["RelativeFrequency%"].cumsum()
        return freqTable
    
    
class Preprocessing:

    def simple_missing(data, quan, qual):

        # Drop rows for ≤ 5% missing
        low_missing_cols = [col for col in data.columns if 0 < data[col].isna().mean() <= 0.05]
        if low_missing_cols:
            data = data.dropna(subset=low_missing_cols)

        # SimpleImputer for >5% & ≤25% missing
        mid_missing_num = [col for col in quan if 0.05 < data[col].isna().mean() <= 0.25]
        mid_missing_cat = [col for col in qual if 0.05 < data[col].isna().mean() <= 0.25]

        if mid_missing_num:
            mean_cols = [col for col in mid_missing_num if abs(data[col].skew()) < 1]
            median_cols = list(set(mid_missing_num) - set(mean_cols))

            if mean_cols: # mean for normal data
                data.loc[:, mean_cols] = SimpleImputer(strategy='mean').fit_transform(data[mean_cols])
            if median_cols: # median for skewed data
                data.loc[:, median_cols] = SimpleImputer(strategy='median').fit_transform(data[median_cols])

        if mid_missing_cat: # mode for categorical data
            data.loc[:, mid_missing_cat] = SimpleImputer(strategy='most_frequent').fit_transform(data[mid_missing_cat])

        return data



    def model_missing(data, quan):

        high_missing_cols = [col for col in data.columns if data[col].isna().mean() > 0.25]

        for col in high_missing_cols:
            known = data[data[col].notna()] # data without null rows
            unknown = data[data[col].isna()] # data with null rows
            if unknown.empty:
                continue

            X_known = pd.get_dummies(known.drop(columns=[col]), dummy_na=True)
            X_unknown = pd.get_dummies(unknown.drop(columns=[col]), dummy_na=True)
            X_unknown = X_unknown.reindex(columns=X_known.columns, fill_value=0) # align columns

            y_known = known[col]
            
            if col in quan:
                model = DecisionTreeRegressor(random_state=10)
            else:
                model = DecisionTreeClassifier(random_state=10)

            model.fit(X_known, y_known)
            prediction = model.predict(X_unknown)

            data.loc[data[col].isna(), col] = prediction

        return data

