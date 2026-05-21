

from src.data_ingestion.documents_loader import DocumentLoader
from src.data_ingestion.embedding import  Embeddings
from src.data_ingestion.text_spliter import TextSpliter
from src.data_ingestion.vectorestore import VectorStore
from pathlib import Path
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException
import sys

logging=log

class RagPipeLine:
    def __init__(self,data_dir,persist_dir,force_rebuild):
        self.data_dir=data_dir
        self.persist_dir=persist_dir
        self.force_rebuild=force_rebuild
        self.vectorstore = None  # Initialize as None
        self.retriever = None

        persist_path = Path(self.persist_dir)
        self.vectorstore_exists = (persist_path.exists() and 
                            any(persist_path.glob("*.sqlite3")))  # Chroma files

        print(f"\n{'='*50}")
        print(f"🚀 RAG Pipeline initialized")
        print(f"📂 Data: {self.data_dir}")
        print(f"💾 Persist: {self.persist_dir}")
        print(f"🔍 Vectorstore exists: {self.vectorstore_exists}")
        print(f"{'='*50}\n")
    def run(self):
        embeding_model=Embeddings()
        embeding=embeding_model.initializing_embedding()
        self.vectorstore =VectorStore(embeddings=embeding,
                                persist_directory=self.persist_dir)
        
        if self.vectorstore_exists and not self.force_rebuild:
            print("🔄 Loading existing vectorstore...")
            print(f"✅ Loaded existing vectorstore from {self.persist_dir}")
            self.retriever=self.vectorstore.load_existing() 
            return self.retriever

        else:
            try:
                log.info(f"initialised rag pipeline for {self.data_dir}")
                document_loader=DocumentLoader(directory=self.data_dir)
                documents=document_loader.document_loader()

                self.text_spliter=TextSpliter(embeding)
                print(f"📄 Loaded {len(documents)} documents from cgnc folder")
                if not documents:
                    logging.error("❌ No documents to process. Please add PDF files to data/CGNC/")
                    print("❌ No documents to process. Please add PDF files to data/CGNC/")
                    raise ValueError(f"❌ No documents found in {self.data_dir}")
                print("🔤 Embeddings ready")
                chunks =self.text_spliter.split_documents(documents)
                if not chunks:
                    print("❌ No chunks created. Check your PDF files.")
                    raise ValueError("❌ No chunks created. Check your PDF files.")
                self.vectorstore.create_from_documents(chunks)
                
                print(f"💾 Vectorstore created with {len(chunks)} documents from cgnc ")
                self.retriever=self.vectorstore.get_retriever()
                print(f"✅ retriver for {self.persist_dir} is ready to use ")
                return self.retriever
            except Exception as e:
                log.error(f"error in rag pipeline {e}")
                raise CustomException(f"error in rag pipeline {e}",sys)


                
                



