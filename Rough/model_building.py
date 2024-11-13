# we perform few feature engineering techniques
# select the best machine learning algorithm
# optimize it using cross_val_score & GridSearchCV
# predict the output

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data_eda.csv')

 
# choose relevent features
df.columns

# numerical columns at the front and categorical onces at the back
# we don't have to select min_salary & max_salary, avg_salary is enough
# avg_salary is our target feature
df_model =  df[['avg_salary', 'Rating', 'age', 'python', 'spark', 'aws', 'excel', 
              'LLMs', 'sql', 'Size', 'Industry', 'Sector', 'Ownership', 'Revenue',  
              'Job_simp', 'seniority']]





# encoding categorical features
df_dum = pd.get_dummies(df_model, dtype=int)





# train test split
#from sklearn.model_selection import train_test_split
#X = df_dum.drop('avg_salary', axis=1)
#y = df_dum.avg_salary.values

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)






# feature scaling
#from sklearn.preprocessing import StandardScaler
#ss = StandardScaler()

# fit and transform on X_train
#X_train_scaled = ss.fit_transform(X_train)

# only transform on X_test
#X_test_scaled = ss.transform(X_test)

#X_test_scaled = pd.DataFrame(X_test_scaled)




# multi-liner regression with cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
lin_reg = LinearRegression()

lin_reg.fit(X_train_scaled, y_train)
lin_mse = cross_val_score(lin_reg, X_train_scaled, y_train, scoring ='neg_mean_squared_error', cv=5)
mean_lin_mse = np.mean(lin_mse)
print(mean_lin_mse)






# ridge regression (L2) with cross_val_score
from sklearn.linear_model import Ridge
ridge = Ridge()

ridge.fit(X_train_scaled, y_train)
ridge_mse = cross_val_score(ridge, X_train_scaled, y_train, scoring='neg_mean_squared_error', cv=5)
mean_ridge_mse = np.mean(ridge_mse)
print(mean_ridge_mse) 



# ridge regression (L2) fine tunning with GridSearchCV
from sklearn.model_selection import GridSearchCV
ridge_grid = Ridge()

params = {'alpha' : [1e-15, 1e-10, 1e-8, 1e-5, 1e-3, 1e-2, 1, 5, 10, 20, 30, 35, 40, 45, 50, 55, 100]}
ridge_regressor = GridSearchCV(ridge_grid, params, scoring='neg_mean_squared_error', cv=5)
ridge_regressor.fit(X_train_scaled, y_train)

print(ridge_regressor.best_params_)
print(ridge_regressor.best_score_)






# lasso regression (L1) with cross_val_score
from sklearn.linear_model import Lasso
lasso = Lasso()

lasso.fit(X_train_scaled, y_train)
lasso_mse = cross_val_score(lasso, X_train_scaled, y_train, scoring='neg_mean_squared_error', cv=5)
mean_lasso_mse = np.mean(lasso_mse)
print(mean_lasso_mse)


# lasso regression (L1) with alpha and cross_val_score 
alpha = []
error = []
for i in range(1, 100):
    alpha.append(i/100)
    lasso_alpha = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lasso_alpha, X_train_scaled, y_train, scoring='neg_mean_squared_error', cv=5)))
    
plt.plot(alpha, error)    

# finding the lowest error
err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]



# lasso regression (L1) fine tunning with GridSearchCV
lasso_grid = Lasso()

params = {'alpha': [1e-15, 1e-10, 1e-8, 1e-5, 1e-3, 1e-2, 1, 5, 10, 20, 30, 35, 40, 45, 50, 55, 100]}
lasso_regressor = GridSearchCV(lasso_grid, params, scoring='neg_mean_squared_error', cv=5)
lasso_regressor.fit(X_train_scaled, y_train)

print(lasso_regressor.best_params_)
print(lasso_regressor.best_score_)






# random forest with cross_val_score
from sklearn.ensemble import RandomForestRegressor
ran_for = RandomForestRegressor()

ran_mse = cross_val_score(ran_for, X_train_scaled, y_train, scoring='neg_mean_squared_error', cv=5)
print(np.mean(ran_mse))


# random forest fine tunning with GridSearchCV
ran_for_grid = RandomForestRegressor()
params = {'n_estimators': [10, 100, 10],     # Number of trees in the forest
          'criterion': ('squared_error', 'absolute_error'),    # mse and mae
          'max_features': ['auto', 'sqrt', 'log2'],  # Number of features to consider at every split
          'max_depth': [None, 10, 20, 30],   # Maximum depth of the tree
          'min_samples_split': [2, 5, 10],   # Minimum number of samples required to split an internal node
          'min_samples_leaf': [1, 2, 4] }    # Minimum number of samples required to be at a leaf node
ran_regressor = GridSearchCV(ran_for_grid, params, scoring='neg_mean_squared_error', cv=5)
ran_regressor.fit(X_train_scaled, y_train)

# will give the best parameter
print(ran_regressor.best_params_)

# will give the best score/ lowest mse
print(ran_regressor.best_score_)

# it is the trained random forest regressor model with the best parameter found in the grid search process
print(ran_regressor.best_estimator_)






# test ensembles 
# Linear Regression
lin_reg_predictions = lin_reg.predict(X_test_scaled)

# Ridge Regression
ridge_predictions = ridge_regressor.predict(X_test_scaled)

# Lasso Regression
lasso_predictions = lasso_regressor.predict(X_test_scaled)

# Random Forest
ran_for_predictions = ran_for_regressor.predict(X_test_scaled)



# mae
from sklearn.metrics import mean_absolute_error

lin_reg_mae = mean_absolute_error(y_test, lin_reg_predictions)
ridge_mae = mean_absolute_error(y_test, ridge_predictions)
lasso_mae = mean_absolute_error(y_test, lasso_predictions)
ran_for_mae = mean_absolute_error(y_test, ran_for_predictions)

print("Mean absolute Error for Linear Regression:", lin_reg_mae)
print("Mean absolute Error for Ridge Regression:", ridge_mae)
print("Mean absolute Error for Lasso Regression:", lasso_mae)
print("Mean absolute Error for Random Forest:", ran_for_mae)



# mse
from sklearn.metrics import mean_squared_error

lin_reg_mse = mean_squared_error(y_test, lin_reg_predictions)
ridge_mse = mean_squared_error(y_test, ridge_predictions)
lasso_mse = mean_squared_error(y_test, lasso_predictions)
ran_for_mse = mean_squared_error(y_test, ran_for_predictions)

print("Mean Squared Error for Linear Regression:", lin_reg_mse)
print("Mean Squared Error for Ridge Regression:", ridge_mse)
print("Mean Squared Error for Lasso Regression:", lasso_mse)
print("Mean Squared Error for Random Forest:", ran_for_mse)

# mae and mse for average of linear regression predictions and random forest predictions
mean_absolute_error(y_test, (lin_reg_predictions+ran_for_predictions)/2)




# build model file (ran_regressor.best_estimator) using pickle
import pickle
pickl = {'model': ran_regressor.best_estimator_}
pickle.dump(pickl, open('model_file' + ".p", "wb"))

file_name = 'model_file.p'
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']
    
# model.predict(X_test_scaled.iloc[1, :].values.reshape(1, -1))

