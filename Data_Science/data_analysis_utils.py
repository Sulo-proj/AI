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

        return descriptive
    
    
    def detect_outliers(descriptive, quan):
        lesser = []
        greater = []
        for columnName in quan:
            if descriptive[columnName]["LesserRange"] > descriptive[columnName]["Min"]:
                lesser.append(columnName)
                descriptive.loc["LesserOutlier", columnName] = True
            else:
                descriptive.loc["LesserOutlier", columnName] = False

            if descriptive[columnName]["GreaterRange"] < descriptive[columnName]["Max-100th%"]:
                greater.append(columnName)
                descriptive.loc["GreaterOutlier", columnName] = True
            else:
                descriptive.loc["GreaterOutlier", columnName] = False
                   
        return descriptive, lesser, greater

    def remove_outliers(descriptive, data, lesser, greater):
        for columnName in lesser:
            data.loc[data[columnName] < descriptive[columnName]["LesserRange"], columnName] = descriptive[columnName]["LesserRange"]
        for columnName in greater:
            data.loc[data[columnName] > descriptive[columnName]["GreaterRange"], columnName] = descriptive[columnName]["GreaterRange"]
        return data
