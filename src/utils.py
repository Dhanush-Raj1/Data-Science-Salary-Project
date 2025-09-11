import os 
import sys 

from src.exception_handling import Custom_Exception
from src.logger import logging

import dill
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score



def save_object(file_path, obj):
    try:
        dir_name = os.path.dirname(file_path)
        
        os.makedirs(dir_name, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)    
            
    except Exception as e:
        raise Custom_Exception(e, sys)
    
    
    
    
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as obj:
            return dill.load(obj)
            
    except Exception as e:
        raise Custom_Exception(e, sys)
    
    
 

def evaluate_models(X_train, X_test, y_train , y_test, models, params):
    
    try:
        report = {}
        logging.info("Starting model evaluation process.")
        
        for model_name, model in models.items():
            param = params[model_name]
            
            gs = GridSearchCV(model, param, cv=3, scoring=r2_score)
            logging.info(f"Starting gridsearch for {model_name}")
            gs.fit(X_train, y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_set_score = r2_score(y_train, y_train_pred)       # r2 score is calculated on actual and predicted values
            test_set_score = r2_score(y_test, y_test_pred)
            
            logging.info(f"Train and test r2 score for {model_name}: {train_set_score, test_set_score}")
            logging.info(f"Completed gridsearch for {model_name}")
            
            report[model_name] = { 'train_accuracy': train_set_score, 
                                   'test_accuracy': test_set_score }
            
        logging.info("Model evalution process has been completed.")
        return report
    
    
    except Exception as e:
        raise Custom_Exception(e, sys) 
            
    