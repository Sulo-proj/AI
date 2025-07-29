import pandas as pd

class Univariate():

    def quanQual(data):
        qual = []
        quan = []
        for columnNames in data.columns:
            # print(columnNames)
            if data[columnNames].dtype == 'object':
                qual.append(columnNames)
            else:
                quan.append(columnNames)
        return quan, qual    
    
    def descriptive(data, quan):

        descriptive = pd.DataFrame(index = ['Mean', 'Median', 'Mode'], columns = quan)
        descriptive

        for columnName in quan:
            descriptive.loc['Mean', columnName] = data[columnName].mean().round(2)
            descriptive.loc['Median', columnName] = data[columnName].median()
            descriptive.loc['Mode', columnName] = data[columnName].mode()[0]
        descriptive

        return descriptive