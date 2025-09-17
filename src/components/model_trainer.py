import os 
import sys
from src.logger import logging
from src.exception_handling import Custom_Exception
from src.utils import save_object, evaluate_models
from src.mlflow.mlflow_tracking import MLFlowLogger 

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
        self.mlflow_logger = MLFlowLogger()
        
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
            
            
            model_report, trained_models, best_params = evaluate_models(X_train, X_test, y_train, y_test, models, params)
            
            best_model_name = max(model_report, key=lambda x: model_report[x]['r2_score'])
            best_model_score = model_report[best_model_name]['r2_score']
            best_model = trained_models[best_model_name]
            
            save_object(file_path=self.model_trainer_config.model_path, 
                        obj=best_model)
                     
            best_r2_score = model_report[best_model_name]['r2_score']
            best_mae = model_report[best_model_name]['mean_absolute_error']
            best_mse = model_report[best_model_name]['mean_squared_error']

            print(f"Best model: {best_model_name}")
            print(f"Best model's metrics: [r2_score:{best_r2_score}, \
                                           mean_absolute_error: {best_mae}, \
                                           mean_squared_error: {best_mse}]")
            
            logging.info(f"Best model: {best_model_name}")
            logging.info(f"Best model's metrics: [r2_score:{best_r2_score}, \
                                           mean_absolute_error: {best_mae}, \
                                           mean_squared_error: {best_mse}]")

            for model_name, model in trained_models.items():
                self.mlflow_logger.log_model(
                    model_name = model_name,
                    params = best_params[model_name],
                    metrics = model_report[model_name],
                    model = model,
                    X_train = X_train
                )
            
            # register the best model (should be outside the above loop)
            self.mlflow_logger.register_best_model(
                    metrics = model_report,
                    models = trained_models,
                    X_train = X_train
                )                               
            
            return model_report[best_model_name]
        
        except Exception as e:
            raise Custom_Exception(e, sys)           
             