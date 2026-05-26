from functools import lru_cache
from src.PipeLine.pipeline import RagPipeLine
from langchain_classic.tools.retriever import create_retriever_tool

@lru_cache(maxsize=1)
def _get_cgnc_retriever():
    rag = RagPipeLine(
        data_dir="./data/CGNC",
        persist_dir="artifacts/vectorestore/db_CGNC",
        force_rebuild=False
    )
    return rag.run()

cgnc_tool = create_retriever_tool(
    _get_cgnc_retriever(),
    "cgnc_maroc",
    """Moroccan accounting standards: CGNC rules, financial statements (bilan, CPC, ESG, ETIC), 
    accounting principles (prudence, permanence), asset depreciation, stock valuation, 
    provisions, regularization entries. Use for: HOW to account for something, WHY an entry is made, 
    financial statement preparation rules. NOT for account numbers — use plan_comptable tool for that.
    Keywords: CGNC, principe comptable, bilan, CPC, ESG, ETIC, amortissement, provision, 
    régularisation, clôture, stock CMUP FIFO, immobilisation, cession."""
)