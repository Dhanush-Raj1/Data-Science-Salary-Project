# import sys
# import os 
# from src.exception_handling import Custom_Exception
# from src.logger import logging 
# from src.utils import save_object

# import pandas as pd
# from sklearn.pipeline import Pipeline 
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import StandardScaler, OneHotEncoder, MultiLabelBinarizer
# from sklearn.base import BaseEstimator, TransformerMixin 
# from sklearn.impute import SimpleImputer
# from sklearn.model_selection import train_test_split


# class DataTransformationConfig:
#     preprocessor_file_path = os.path.join('artifacts', 'preprocessor.pkl')
#     train_data_path = os.path.join('artifacts', 'train.csv')
#     test_data_path = os.path.join('artifacts', 'test.csv')
    


# class MultiLabelEncoder(BaseEstimator, TransformerMixin):
#     def __init__(self):
#         self.mlb = MultiLabelBinarizer()
    
#     def fit(self, X, y=None):
#         self.mlb.fit(X)
#         return self
    
#     def transform(self, X):
#         return self.mlb.transform(X)
    
#     def get_feature_names_out(self, input_features=None):
#         return [f"skill_{cls}" for cls in self.mlb.classes_]

     

# class DataTransformation:
#     def __init__(self):
#         self.data_transformation_config = DataTransformationConfig()

#     def get_data_transformer_object(self):
#         """
#         Builds preprocessor object and returns it
#         """
#         try:
#             num_cols = ['Company_Rating']
#             cat_cols = ['Seniority', 'Job_type', 'Salary_Source', 'Location']
#             multi_cat_cols = ['Skills']
            
#             num_pipeline = Pipeline(steps = [#('imputer', SimpleImputer(strategy='median')),
#                                              ('scaler', StandardScaler())])
            
#             cat_pipeline = Pipeline(steps = [#('imputer', SimpleImputer(strategy='most_frequent')),
#                                              ('encoder', OneHotEncoder())])
            
#             multi_cat_pipeline = Pipeline(steps = [('multi_encoder', MultiLabelEncoder())])

#             preprocessor = ColumnTransformer([
#                 ('num_pipeline', num_pipeline, num_cols), 
#                 ('cat_pipeline', cat_pipeline, cat_cols),
#                 ('multi_cat_pipeline', multi_cat_pipeline, multi_cat_cols)
#             ])

#             return preprocessor
        
#         except Exception as e:
#             raise Custom_Exception(e, sys)



import sys
import os 
from src.exception_handling import Custom_Exception
from src.logger import logging 
from src.utils import save_object

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer, MultiLabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin 
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import ast


class DataTransformationConfig:
    preprocessor_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    train_data_path = os.path.join('artifacts', 'train.csv')
    test_data_path = os.path.join('artifacts', 'test.csv')


class SkillPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.mlb = MultiLabelBinarizer()
        self.feature_names_ = None

    
    def fit(self, X, y=None):
        # converts numpy to series (columntransformer passes dataframe as numpy arrays )
        # converts dataframes to series (during prediction on new input data which is in dataframe format)
        skills_series = X.iloc[:, 0] if hasattr(X, 'iloc') else pd.Series(X)
        
        # Convert string representations to lists if needed
        if isinstance(skills_series.iloc[0], str):
            skills_series = skills_series.apply(ast.literal_eval)
        
        self.mlb.fit(skills_series)
        self.feature_names_ = [f"skill_{cls}" for cls in self.mlb.classes_]
        return self
    
    def transform(self, X):
        skills_series = X.iloc[:, 0] if hasattr(X, 'iloc') else pd.Series(X)
        
        if isinstance(skills_series.iloc[0], str):
            skills_series = skills_series.apply(ast.literal_eval)
        
        return self.mlb.transform(skills_series)
    
    def get_feature_names_out(self, input_features=None):
        return self.feature_names_


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Builds preprocessor object and returns it
        """
        try:
            num_cols = ['Company_Rating']
            cat_cols = ['Seniority', 'Job_type', 'Salary_Source', 'Location']
            multi_cat_cols = ['Skills']
            
            num_pipeline = Pipeline(steps = [
                ('scaler', StandardScaler())
            ])
            
            cat_pipeline = Pipeline(steps = [
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])
            
            multi_cat_pipeline = Pipeline(steps = [
                ('skill_processor', SkillPreprocessor())
            ])

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, num_cols), 
                ('cat_pipeline', cat_pipeline, cat_cols),
                ('multi_cat_pipeline', multi_cat_pipeline, multi_cat_cols)
            ])

            return preprocessor
        
        except Exception as e:
            raise Custom_Exception(e, sys)


    def initiate_data_transformation(self):
        try:
            logging.info("Starting data transformation")
            logging.info("Reading cleaned data from 'Data/data_cleaned.csv'")
            df = pd.read_csv('data/data_cleaned.csv')   # The file is executed from the root directory as 'data' folder is in root dir 
            
            logging.info(f"Shape of data: {df.shape}") 
            logging.info(f"Columns in the dataset before transformation: {list(df.columns)}")

            logging.info("Obtaining preprocessor object")
            preprocessor = self.get_data_transformer_object()

            logging.info("Performing train and test split")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
            target_col = 'Salary'   
            X_train = train_set.drop(columns=target_col, axis=1)
            y_train = train_set[target_col]
            logging.info(f"Training set shape: {X_train.shape}, {y_train.shape}")
            X_test = test_set.drop(columns=[target_col], axis=1)
            y_test = test_set[target_col]
            logging.info(f"Testing set shape: {X_test.shape}, {y_test.shape}")

            logging.info("Preprocessing train and test sets")
            X_train_pre = preprocessor.fit_transform(X_train)
            X_test_pre = preprocessor.transform(X_test)

            logging.info(f"Shape and dtype of X_train_pre: {X_train_pre.shape}, {type(X_train_pre)}")
            logging.info(f"Shape and dtype of X_test_pre: {X_test_pre.shape}, {type(X_test_pre)}")
            logging.info(f"Shape and dtype of y_train: {y_train.shape}, {type(y_train)}")
            logging.info(f"Shape and dtype of y_test: {y_test.shape}, {type(y_train)}")

            logging.info("Converting the numpy arrays(outputs of fit_transform) to dataframes to save as csv files")
            feature_names = preprocessor.get_feature_names_out()
            # Remove pipeline prefixes in column names(everything before "__")
            clean_feature_names = [name.split("__")[-1] for name in feature_names]      
            logging.info(f"Feature names after transformation: {clean_feature_names}")

            X_train_df = pd.DataFrame(X_train_pre, columns=clean_feature_names)
            x_test_df = pd.DataFrame(X_test_pre, columns=clean_feature_names)
            logging.info(f"Shape of X_train_df: {X_train_df.shape}")
            logging.info(f"Shape of X_test_df: {x_test_df.shape}")

            train_final = pd.concat([X_train_df, y_train.reset_index(drop=True)], axis=1)
            test_final = pd.concat([x_test_df, y_test.reset_index(drop=True)], axis=1)
            logging.info(f"Shape of train_final: {train_final.shape}")
            logging.info(f"Shape of test_final: {test_final.shape}")

            logging.info("Saving train and test sets")
            train_final.to_csv(self.data_transformation_config.train_data_path, index=False)
            test_final.to_csv(self.data_transformation_config.test_data_path, index=False)

            logging.info("Saving preprocessor object")
            save_object(file_path=self.data_transformation_config.preprocessor_file_path, obj=preprocessor)

            logging.info("Data transformation completed successfully.")
            return (X_train_pre,        # array 
                    X_test_pre,         # array
                    y_train,            # series
                    y_test)             # series
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        

# if __name__ == "__main__":
#     data_transformation = DataTransformation()
#     data_transformation.initiate_data_transformation()