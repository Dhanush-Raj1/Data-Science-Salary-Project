import os
import sys
from dataclasses import dataclass

from src.components import scraper as scraper
from src.logger import logging
from src.exception_handling import Custom_Exception


@dataclass()
class DataCollectionConfig:
    data_path: str = os.path.join('data', 'data_new.csv')
    

class DataCollection:
    def __init__(self):
        self.data_collection_config = DataCollectionConfig()
        
    def initiate_data_collection(self):
        try: 
            logging.info("Data collection process has been started.")
            
            collect_data = scraper.find_jobs("Data Scientist")

            os.makedirs(os.path.dirname(self.data_collection_config.data_path), exist_ok=True)
            
            # saving the dataframe to csv file
            collect_data.to_csv(self.data_collection_config.data_path, index=False)
            
            logging.info("Data collection process has been completed.")
            logging.info("Data has been successfully saved.")
        
        except Exception as e:
            raise Custom_Exception(e, sys)
        

if __name__ == "__main__":
    data_collection = DataCollection()
    data_collection.initiate_data_collection()