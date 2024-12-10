import sys 
import os
from src.logger import logging 
from src.exception_handling import Custom_Exception
from src.utils import save_object

from dataclasses import dataclass

import dill
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split



@dataclass
class DataTransformationConfig:
    
    # path for saving preprocessor
    preprocessor_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
        
    def get_data_transformer_obj(self):
        try:
            num_cols = ['Rating', 'age', 'python', 'spark', 'aws', 'excel', 'LLMs', 'sql']
            
            cat_cols = ['Size', 'Industry', 'Sector', 'Ownership', 'Revenue', 'Job_simp', 'seniority']
            
            logging.info(f"Numerical columns {num_cols}")
            logging.info(f"Categorical columns {cat_cols}")
            
            num_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')) ])
            
            cat_pipeline = Pipeline(steps=[('imputer', SimpleImputer(strategy='most_frequent')),
                                           ('encoder', OneHotEncoder(sparse_output=False)) ])
            
            preprocessor = ColumnTransformer([('num_pipeline', num_pipeline, num_cols), 
                                              ('cat_pipeline', cat_pipeline, cat_cols)])
            
            return preprocessor
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        
    
    
    def initiate_data_transformation(self):
        try:
            logging.info("Data transformation process has been started.")
            
            df = pd.read_csv('artifacts/data_eda.csv')
            logging.info("Data has been imported successfully.")
            
            df = df.drop(columns=['min_salary', 'max_salary'], axis=1)
            logging.info(f"Shape of df: {df.shape}")

            logging.info("Train, test split has been initated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            logging.info("Saving the train, test sets.")
            train_set.to_csv(self.data_transformation_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.data_transformation_config.test_data_path, index=False, header=True)
            
            logging.info("Calling the preprocessing object.")
            preprocessor = self.get_data_transformer_obj()
            
            target_col = 'avg_salary'

            X_train = train_set.drop(columns = target_col, axis=1)
            y_train = train_set[target_col]
            
            X_test = test_set.drop(columns = target_col, axis=1)
            y_test = test_set[target_col]

            logging.info(f"X_train: {X_train.shape}, y_train: {y_train.shape}, X_test: {X_test.shape}, y_test: {y_test.shape}")
            logging.info(f"X_train, X_test columns: {X_train.columns}, {X_test.columns}")
            logging.info(f"y_train, y_test columns: {y_train.name}, {y_test.name}")
            logging.info(f"Type train sets: {type(X_train)} {type(y_train)}")
            logging.info(f"Type test sets: {type(X_test)} {type(y_test)}")


            logging.info("Preprocessing train and test set has been started.")
            X_train_pre = preprocessor.fit_transform(X_train) 
            X_test_pre = preprocessor.transform(X_test)
            logging.info("Preprocessing has been completed.")
            
            logging.info(f'Type of X_train_pre {type(X_train_pre)}')
            logging.info(f'Type of X_test_pre {type(X_test_pre)}')
            
            #train_arr = np.c_[X_train_arr, y_train]
            #test_arr = np.c_[X_test_arr, y_test] 

            #logging.info(f"train_arr, test_arr type {type(train_arr)} {type(test_arr)}")
            #logging.info(f"Shape of train_arr, test_arr {train_arr.shape} {test_arr.shape}")
            
            save_object(file_path = self.data_transformation_config.preprocessor_file_path, 
                        obj = preprocessor)
            
            logging.info("Preprocessing object has been saved.")
            logging.info("Data transformation process has been completed.")
            
            return(X_train_pre, 
                   X_test_pre,
                   y_train, 
                   y_test)
            
            
        except Exception as e:
            raise Custom_Exception(e, sys)
            
    

if __name__ == '__main__':
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation()
    
     