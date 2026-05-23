from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException

logging=log

# Try a multilingual model
model_name="intfloat/multilingual-e5-large"

from  dotenv import  load_dotenv

load_dotenv()
import os

os.environ["HUGGINGFACE_API"] = os.getenv("HUGGINGFACE_API")  


class Embeddings:

    def __init__(self,
        model_name:str="intfloat/multilingual-e5-large",
        device: str = "cuda",
        normalize_embeddings: bool = True,
        batch_size: int = 32):

        self.model_name = model_name
        self.device = device
        self.normalize_embeddings = normalize_embeddings
        self.batch_size = batch_size
        self._embeddings = None
        logging.info("embedding get initialized")


    def initializing_embedding(self):
        if self._embeddings is None:
            try:
                self.embeddings = HuggingFaceEmbeddings(
                        model_name=self.model_name,
                        model_kwargs={'device': self.device},
                        encode_kwargs={
                            'normalize_embeddings': self.normalize_embeddings,
                            'batch_size': self.batch_size
                        }
                    )
                log.info(f"initialiased embeding model {HuggingFaceEmbeddings.__class__.__name__} with model name : {self.model_name}")
            except Exception as e:
                    logging.error(f"error during initilizing embedings : {e}")
                    raise CustomException(
                        message=f"Failed to initialize embeddings with model {self.model_name} or their is an error in embeding models",
                        error_detail=e
                    )
        return self.embeddings