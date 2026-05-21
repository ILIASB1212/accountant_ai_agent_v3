import os
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException
import sys
import yaml


def create_directoris(path:str):
    directory_name=os.path.dirname(path)
    os.makedirs(directory_name,exist_ok=True)
    log.info(f"created directory with name : {directory_name}")




def read_yaml(path:str):
    try:
        with open(path,"r") as file:
            data=yaml.safe_load(file)
            return data
    except Exception as e:
        log.error(f"error during loading yaml file {e}")
        raise CustomException(f"error in loading yaml file {e}",sys)
