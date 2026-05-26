from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException

logging=log

# Try a multilingual model
model_name="intfloat/multilingual-e5-large"

from  dotenv import  load_dotenv

load_dotenv()
import os
from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  


class Embeddings:

    def __init__(self,model_name:str="text-embedding-3-large"):

        self.model_name = model_name
        self._embeddings = None
        logging.info("embedding get initialized")


    def initializing_embedding(self):
        if self._embeddings is None:
            try:
                self.embeddings = OpenAIEmbeddings(model=self.model_name)
                log.info(f"initialiased embeding model {self.embeddings.__class__.__name__} with model name : {self.model_name}")
            except Exception as e:
                    logging.error(f"error during initilizing embedings : {e}")
                    raise CustomException(
                        message=f"Failed to initialize embeddings with model {self.model_name} or their is an error in embeding models",
                        error_detail=e
                    )
        return self.embeddings
    