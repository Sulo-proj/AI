import pandas as pd
import numpy as np

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