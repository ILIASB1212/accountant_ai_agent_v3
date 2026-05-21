from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException

logging=log


class Embeddings:

    def __init__(self,
        model_name:str="sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cpu",
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