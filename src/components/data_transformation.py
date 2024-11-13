import sys 
import os
from src.logger import logging 
from src.exception_handling import Custom_Exception
from src.utils import save_object

from dataclasses import dataclass

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
                                           ('encoder', OneHotEncoder()) ])
            
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
            
            df.drop(columns=['min_salary', 'max_salary'], axis=1)
            
            logging.info("Train, test split has been initated")
            train_set, test_set = train_test_split(df, test_size=0.1, random_state=42)
            
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

            logging.info("Preprocessing train and test set has been started.")
            
            X_train_pre = preprocessor.fit_transform(X_train) 
            X_test_pre = preprocessor.transform(X_test)
            logging.info("Preprocessing has been completed.")
            
            #logging.info(f"Shape of x_train_pre: {X_train_pre.shape}")
            #logging.info(f"Shape of y_train: {y_train.shape}")
            #logging.info(f"Shape of x_test_pre: {X_test_pre.shape}")
            #logging.info(f"Shape of y_test: {y_test.shape}")
            
            logging.info(f'Type of X_train_pre {type(X_train_pre)}')
            logging.info(f'Type of y_train: {type(y_train)}')
            
            logging.info('Converting the type of X_train_pre, X_test_pre(sparse matrix) into an array to match type of y_train, y_test.')
            X_train_pre = X_train_pre.toarray()
            X_test_pre = X_test_pre.toarray()
            
            train_arr = np.c_[X_train_pre, y_train]
            test_arr = np.c_[X_test_pre, y_test] 
            
            save_object(file_path = self.data_transformation_config.preprocessor_file_path, 
                        obj = preprocessor)
            
            logging.info("Preprocessing object has been saved.")
            logging.info("Data transformation process has been completed.")
            
            return(train_arr, 
                   test_arr)
            
            
        except Exception as e:
            raise Custom_Exception(e, sys)
            
    

#if __name__ == '__main__':
    #data_transformation = DataTransformation()
    #data_transformation.initiate_data_transformation()
    
     