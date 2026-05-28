import pickle
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever


  # type: ignore
from src.loging.logger import log
from src.exceptions.custom_exceptions import CustomException

logging = log


class VectorStore:
    def __init__(self, embeddings, persist_directory):
        self.embeddings = embeddings
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.hybrid_retriever = None
        # create a file for BM25 if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        logging.info(f"✅ VectorStore initialized with persist_dir: {persist_directory}")

    # ── Helper: BM25 file path ── create sub file for BM25 
    @property
    def _bm25_path(self) -> Path:
        return Path(self.persist_directory) / "bm25_index.pkl"

    # ── CREATE (build hybrid + persist BM25 to disk) ──
    def create_from_documents(self, documents):
        try:
            # 1. Dense (Chroma persists automatically)
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            logging.info(f"✅ Created Chroma vectorstore with {len(documents)} documents")

            # 2. Dense retriever
            dense_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})

            # 3. Sparse BM25 (build from docs)
            sparse_retriever = BM25Retriever.from_documents(documents)
            sparse_retriever.k = 3

            # 4. Save BM25 to disk (pickle)
            with open(self._bm25_path, "wb") as f:
                pickle.dump(sparse_retriever, f)
            logging.info(f"💾 BM25 index saved to {self._bm25_path}")

            # 5. Hybrid ensemble
            self.hybrid_retriever = EnsembleRetriever(
                retrievers=[dense_retriever, sparse_retriever],
                weights=[0.7, 0.3]
            )

            return self.vectorstore

        except Exception as e:
            logging.error(f"❌ Error creating vectorstore: {e}")
            raise CustomException("Failed to create vectorstore", e)

    # ── LOAD EXISTING (restore both dense + BM25) ──
    def load_existing(self, k: int = 4):
        try:
            # 1. Load dense Chroma
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            logging.info(f"✅ Loaded Chroma from {self.persist_directory}")
            dense_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})

            # 2. Load BM25 from disk
            if self._bm25_path.exists():
                with open(self._bm25_path, "rb") as f:
                    sparse_retriever = pickle.load(f)
                sparse_retriever.k = 3
                logging.info(f"✅ Loaded BM25 index from {self._bm25_path}")

                # 3. Rebuild hybrid
                self.hybrid_retriever = EnsembleRetriever(
                    retrievers=[dense_retriever, sparse_retriever],
                    weights=[0.7, 0.3]
                )
                logging.info("✅ Hybrid retriever restored")
            else:
                logging.warning("⚠️ No BM25 pickle found — falling back to dense only")
                self.hybrid_retriever = None

            # ← FIX: return the retriever, not the vectorstore
            return self.get_retriever()

        except Exception as e:
            logging.error(f"❌ Error loading vectorstore: {e}")
            raise CustomException("Failed to load vectorstore", e)

    # ── GET RETRIEVER ──
    def get_retriever(self, k: int = 4):
        if self.vectorstore is None:
            raise CustomException("Vectorstore not created yet.")

        if self.hybrid_retriever is not None:
            return self.hybrid_retriever

        return self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": 20, "lambda_mult": 0.5}
        )