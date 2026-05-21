from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker   # ← FIXED
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException
import sys

logging=log



class TextSpliter:
    def __init__(self,embeding_model,persist_directory:str="vectorestore_VDB"):
        self.embeding=embeding_model
        self.persist_directory=persist_directory
        


    
    def split_documents(self,documents):
        # Split
        try:
            text_splitter = SemanticChunker(
                            embeddings=self.embeding,
                            breakpoint_threshold_type="percentile"
                        )

           
            chunks = text_splitter.split_documents(documents)
            logging.info(f"✅ Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logging.error(f"❌ Error splitting documents: {e}")
            raise CustomException(f"Failed to chunk  {e}",sys)




