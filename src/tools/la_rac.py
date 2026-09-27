from functools import lru_cache
from src.PipeLine.pipeline import RagPipeLine
from langchain_classic.tools.retriever import create_retriever_tool

@lru_cache(maxsize=1)
def _get_ras_retriever():
    rag = RagPipeLine(
        data_dir="./data/RAS",
        persist_dir="artifacts/vectorestore/db_RAS",
        force_rebuild=False
    )
    return rag.run()

ras_tool = create_retriever_tool(
    _get_ras_retriever(),
    "ras_maroc",
    """Moroccan accounting standards: RAS rules, 
    provisions, regularization entries. Use for: HOW to account for something, WHY an entry is made, 
    Keywords: RAS, retenu a la source , bilan, CPC, ESG, ETIC, taux de retenu ala source , 
    régularisation, clôture, stock CMUP FIFO, immobilisation, cession."""
)