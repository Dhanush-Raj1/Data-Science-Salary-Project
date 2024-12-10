import os 
import sys 

from src.components.data_collection import DataCollection
from src.components.data_cleaning import DataCleaning
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


#data_collection = DataCollection()
#data_collection.initiate_data_collection()
 

#data_cleaning = DataCleaning()
#data_cleaning.initiate_data_cleaning()


data_transformation = DataTransformation()
X_train, X_test, y_train, y_test = data_transformation.initiate_data_transformation()
#train_arr, test_arr = data_transformation.initiate_data_transformation()


model_trainer = ModelTrainer()
model_trainer.initiate_model_trainer(X_train, X_test, y_train, y_test)
#model_trainer.initiate_model_trainer(train_arr , test_arr)