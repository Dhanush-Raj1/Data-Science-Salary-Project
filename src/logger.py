import logging
import os 
from datetime import datetime



# log file name
logs_file_name = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + ".log" 

# log folder name 
logs_folder_name = datetime.now().strftime('%d_%m_%Y')


# logs folder path 
logs_path = os.path.join(os.getcwd(), "logs", logs_folder_name)


# create logs folder path 
os.makedirs(logs_path, exist_ok=True)


# path for storing logs files
logs_file_path = os.path.join(logs_path, logs_file_name)


# configure logging
logging.basicConfig(filename=logs_file_path,
                    
                    # format of logging message
                    format="[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
                    
                    # level info and above 
                    level=logging.INFO)


# testing code 
if __name__=="__main__":
    logging.info('Logging has started')