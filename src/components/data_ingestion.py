#to read data from any kind of source and then store the spiltted data in artifacts

import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer 



##definig the path to store data
#just providing the input things that are req for data ingestion
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            #reading the dataset
            df=pd.read_csv(r"E:\Data science\Projects\mlproject\notebook\data\stud.csv")
            logging.info('Read the dataset as dataframe')
            
            #creating the artifact dir with the help of above mentioned paths  
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            #saving raw data into the raw data path after reading from local
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            #splitting the dataset
            logging.info("Train test split initiated")

            #saving the train and test data into the corresponding paths after reading from local
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed")

            return(
                #returning theses two data for data transformtion.data transformation will grab this info
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    #data ingestion
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    
    #data transformation
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    #model trainer
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))




