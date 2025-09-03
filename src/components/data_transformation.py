import sys
import os 
from src.exception_handling import Custom_Exception
from src.logger import logging 
from src.utils import save_object

from dataclasses import dataclass 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class DataTransformationConfig:
    preprocessor_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    train_data_path = os.path.join('artifacts', 'train.csv')
    test_data_path = os.path.join('artifacts', 'test.csv')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self):
        try:
            logging.info("Reading cleaned data")
            data = pd.read_csv('data/data_cleaned.csv')   # The file is executed from the root directory as 'data' folder is in root dir 
            data.size 

            logging.info(f"Renaming target column to 'Salary'")
            data.rename(columns={'Median_Salary_Standardized': 'Salary'}, inplace=True)

            logging.info(f"Final columns in the dataset: {data.columns}")

            logging.info("Performing train/test split")
            train_set, test_set = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)
            target_col = 'Salary' 
            X_train = train_set.drop(columns=target_col, axis=1)
            y_train = train_set[target_col]

            X_test = test_set.drop(columns=[target_col], axis=1)
            y_test = test_set[target_col]

            logging.info("Scaling the dataset")
            preprocessor = StandardScaler()
            X_train[['Company_Rating']]= preprocessor.fit_transform(X_train[['Company_Rating']])
            X_test[['Company_Rating']] = preprocessor.transform(X_test[['Company_Rating']])

            # Recombine X and y before saving it as csv files 
            train_set = pd.concat([X_train, y_train], axis=1)
            test_set = pd.concat([X_test, y_test], axis=1)

            logging.info("Saving train and test sets")
            train_set.to_csv(self.data_transformation_config.train_data_path, index=False)
            test_set.to_csv(self.data_transformation_config.test_data_path, index=False)

            logging.info("Saving preprocessor object")
            save_object(file_path=self.data_transformation_config.preprocessor_file_path, obj=preprocessor)

            logging.info("Data transformation process completed successfully.")
            return (X_train, 
                    X_test, 
                    y_train, 
                    y_test)
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        

# if __name__ == "__main__":
#     data_transformation = DataTransformation()
#     data_transformation.initiate_data_transformation()