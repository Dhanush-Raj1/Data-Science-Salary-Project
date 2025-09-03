import os 
import sys
from src.logger import logging
from src.exception_handling import Custom_Exception
from src.utils import save_object, evaluate_models

import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR
from catboost import CatBoostRegressor



@dataclass 
class ModelTrainerConfig:
    model_path = os.path.join('artifacts', 'model.pkl')
    
    
class ModelTrainer:
     
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    #def initiate_model_trainer(self, train_array, test_array):
    def initiate_model_trainer(self, X_train, X_test, y_train, y_test):
        try:
            logging.info("Model training has been started.")
            
            #X_train, X_test, y_train, y_test = (train_array[:, :-1], test_array[:, :-1],
                                                #train_array[:, -1], test_array[:, -1])

            #logging.info("Train, test split has been completed.")
            
            models = { "Linear regression": LinearRegression(), 
                       "Knn regressor": KNeighborsRegressor(), 
                       "Decision tree regressor": DecisionTreeRegressor(), 
                       "Random Forest regressor": RandomForestRegressor(), 
                       "Adaboost regressor": AdaBoostRegressor(), 
                       "Gradientboost regressor": GradientBoostingRegressor(), 
                       "Xgboost regressor": XGBRegressor(), 
                       "Support vector regressor": SVR(),
                       "Catboost regressor": CatBoostRegressor()   }

            params = { "Linear regression": {}, 
                
                       "Knn regressor": {'n_neighbors': [3, 5, 8, 11, 15], 
                                         'weights': ['uniform', 'distance'], 
                                         'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']},
                        
                       "Decision tree regressor": {'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                                                   'splitter': ['best', 'random'], 
                                                   'max_depth': [3, 5, 10, 15, 20, 25, 30, 40, 50],
                                                   'max_features': [None, 'sqrt', 'log2']}, 
                        
                       "Random Forest regressor": {'n_estimators': [50, 100, 150, 200, 250, 300], 
                                                   'criterion': ['squared_error', 'absolute_error', 'friedman_mse', 'poisson'], 
                                                   'max_depth': [3, 5, 10, 15, 20, 25, 30, 40, 50],
                                                   'max_features': ['sqrt', 'log2', None]}, 
                        
                       "Adaboost regressor": {'estimator': [None, LinearRegression(), KNeighborsRegressor()],
                                              'n_estimators': [10, 50, 100, 200, 300], 
                                              'learning_rate': [0.01, 0.1, 0.5, 1.0, 1.5, 2.0],
                                              'loss': ['linear', 'square', 'exponential'] }, 
                        
                       "Gradientboost regressor": {'loss': ['squared_error', 'absolute_error', 'huber', 'quantile'], 
                                                   'learning_rate': [0.01, 0.5, 0.1, 1.0, 1.5], 
                                                   'n_estimators': [10, 50, 100, 200, 300, 400], 
                                                   'criterion': ['friedman_mse', 'squared_error'], 
                                                   'max_features': ['sqrt', 'log2', None]}, 
                        
                       "Xgboost regressor": {'boost': ['gbtree', 'gblinear', 'dart'], 
                                             'max_depth': [3, 5, 10, 15, 20, 25, 30, 40]}, 
                        
                       "Support vector regressor": {}, 
                        
                       "Catboost regressor": {}     }
            
            
            model_report = evaluate_models(X_train, X_test, y_train, y_test, models, params)
            
            best_model_name = max(model_report, key=lambda x: model_report[x]['test_accuracy'])
            best_model_score = model_report[best_model_name]['test_accuracy']
            best_model = models[best_model_name]
            
            
            save_object(file_path=self.model_trainer_config.model_path, 
                        obj=best_model)
            
            predicted = best_model.predict(X_test)
            
            r_2_score = r2_score(y_test, predicted)
            
            print(f"Best model: {best_model_name}")
            print(f"Final score: {r_2_score}")
            
            logging.info(f"Best model: {best_model_name}")
            logging.info(f"Final accuracy: {r_2_score}")
            
            return r_2_score
        
        
        except Exception as e:
            raise Custom_Exception(e, sys)           
            