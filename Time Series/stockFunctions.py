def graph(Actual,predicted,Actlabel,predlabel,title,Xlabel,ylabel):
    from matplotlib import pyplot as plt
    plt.style.use('default')
    plt.figure(figsize=(10,5))
    plt.plot(Actual, color = 'blue', label=Actlabel)
    plt.plot(predicted, color = 'green', label =predlabel)
    plt.title(title)
    plt.xlabel(Xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
    
def rmsemape(y_test, y_pred):
    from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
    import numpy as np
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = mean_absolute_percentage_error(y_test, y_pred)
    return rmse, mape


















    