import os 
import sys
from src.utils import load_object
from src.logger import logging 
from src.exception_handling import Custom_Exception 
from flask import request
import pandas as pd 


class NewData:
    """
    Returns the data as a Dataframe 
    """

    def __init__(self, 
                 Company_Rating: float,
                 Skills: str,
                 Seniority: str,
                 Job_type: str,
                 Salary_Source: str,
                 Location: str,
                 ):

            self.Company_Rating = Company_Rating
            self.Skills = Skills
            self.Seniority = Seniority
            self.Job_type = Job_type
            self.Salary_Source = Salary_Source 
            self.Location = Location

    def get_data_as_dataframe(self):
        try:
            # convert skills string to list format that preprocessor expects 
            skills_list = request.form.getlist('Skills')
            #skills_list = self.Skills.split(',') if self.Skills else []
            skills_formated = str([skill.strip() for skill in skills_list])

            new_data_input = {
                 "Company_Rating": [float(self.Company_Rating)],
                 "Skills": [skills_formated],
                 "Seniority": [self.Seniority],
                 "Job_type": [self.Job_type],
                 "Salary_Source": [self.Salary_Source],
                 "Location": [self.Location]
            } 

            logging.info("Converting input as a DataFrame.")
            df = pd.DataFrame(new_data_input)
            logging.info("DataFrame created: \n{df}")
            return df
          
        except Exception as e:
            raise Custom_Exception(e, sys)


class PredictData:
     """
     Make Predictions and returns them 
     """

     def __init__(self):
          pass 

     def predict_data(self, df): 
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'

            logging.info("Loading preprocessor and model objects.")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            logging.info("Preprocessor and model objects loaded successfully.")

            logging.info("Input data before transformation: {df}")
            logging.info(f"Input data types: \n{df.dtypes}")

            data_transformed = preprocessor.transform(df)
            logging.info(f"Input data after transformation: {data_transformed}")
            logging.info(f"Input data shape after transformation: {data_transformed.shape}")

            logging.info("Making predictions...")
            prediction = model.predict(data_transformed)
            logging.info(f"Prediction completed: {prediction}")

            return prediction

        except Exception as e: 
             raise Custom_Exception(e, sys)
     
    
        