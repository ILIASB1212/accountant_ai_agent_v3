from langchain_community.document_loaders import PyPDFDirectoryLoader
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException
import sys
logging=log



class DocumentLoader:
    def __init__(self,directory:str,):
        self.directory=directory
        logging.info("initialized docuemnt loader")

    def document_loader(self):
        rew_documents=PyPDFDirectoryLoader(self.directory)
        self.docs=rew_documents.load()
        if self.docs:
            try:
                # extract metada and LOG TROUGHT EASH DOCUMENT LOADED AND EXTRACT THE SOURCE:PDF NAME 
                pdf_files = set()
                for doc in self.docs:
                    source = doc.metadata.get('source', 'unknown')
                    pdf_files.add(source)
                # Log each PDF file
                logging.info(f"✅ Successfully loaded {len(self.docs)} from directory {self.directory} documents lent is  {len(pdf_files)} PDF files:")
                for pdf in pdf_files:
                    logging.info(f" 📄 {pdf}")
                
                
            except Exception as e:
                    logging.error(f"error in loading documents : {e}")
                    raise CustomException(f"Failed to load documents {e}",sys
                        
                    )
        elif not self.docs:
            logging.error(f" No documents found in {self.directory}")
            print(f"⚠️ No documents found in {self.directory}")
         
        return self.docs
    



