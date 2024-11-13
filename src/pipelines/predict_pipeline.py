import os 
import sys 
from src.utils import load_object
from src.logger import logging
from src.exception_handling import Custom_Exception

import pandas as pd 
import numpy as np 


class NewData:
    """
    Returns the data as a Dataframe 
    """
    
    def __init__(self, 
                 Rating: int, 
                 Size: str, 
                 Industry: str, 
                 Sector: str, 
                 Ownership: str, 
                 Revenue: str, 
                 age: int, 
                 python: int, 
                 spark: int, 
                 aws: int, 
                 excel: int, 
                 LLMs: int, 
                 sql: int, 
                 Job_simp: str, 
                 seniority: str):
        
        self.Rating = Rating
        self.Size = Size
        self.Industry = Industry
        self.Sector = Sector
        self.Ownership = Ownership
        self.Revenue = Revenue 
        self.age = age
        self.python = python 
        self.spark = spark
        self.aws = aws
        self.excel = excel 
        self.LLMs = LLMs
        self.sql = sql
        self.Job_simp = Job_simp 
        self.seniority = seniority 
        
    
    def get_data_as_dataframe(self):
        try:
            new_data_input = {"Rating": [self.Rating], 
                              "Size": [self.Rating], 
                              "Industry": [self.Industry], 
                              "Sector": [self.Sector], 
                              "Ownership": [self.Ownership],
                              "Revenue": [self.Revenue],
                              "age": [self.age], 
                              "python": [self.python],
                              "spark": [self.spark],
                              "aws": [self.aws],
                              "excel": [self.excel],
                              "LLMs": [self.LLMs],
                              "sql": [self.sql],
                              "Job_simp": [self.Job_simp],
                              "seniorty": [self.seniority]  }
            
            logging.info("Converting the data as a DataFrame.")
            return pd.DataFrame(new_data_input)
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        

class Predict:
    """
    Make predictions(using saved model) and returns them
    """
    
    def __init__(self):
        pass 
    
    def predict_data(self, df):
        try:
            model_path = "artifacts/model.pkl"
            preprocessor_path = "artifacts/preprocessor.pkl"
            
            logging.info("Loading model and preprocessor object.")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            logging.info("Model and preprocessor has been loaded successfully.")
            
            logging.info(f"Data before preprocessing \n{df.head()}")
            df_preprocessed = preprocessor.transform(df)
            logging.info(f"Data after preprocessing \n{df_preprocessed}")
            
            logging.info("Predicting the salary for the given input data....")
            predicted = model.predict(df_preprocessed)
            logging.info("Prediction has been completed.")
            
            return predicted
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        
            
            
