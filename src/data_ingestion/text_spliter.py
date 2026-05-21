from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SemanticChunker

from langchain_community.document_loaders import PyPDFDirectoryLoader
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException

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

           
            chunks = text_splitter.create_document(documents)
            logging.info(f"✅ Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logging.error(f"❌ Error splitting documents: {e}")
            raise CustomException("Failed to split documents", e)





