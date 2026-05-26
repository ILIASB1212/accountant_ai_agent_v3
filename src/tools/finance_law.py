from functools import lru_cache
from src.PipeLine.pipeline import RagPipeLine
from langchain_classic.tools.retriever import create_retriever_tool

@lru_cache(maxsize=1)
def _get_lf_retriever():
    rag = RagPipeLine(
        data_dir="./data/LOIS_DE_FINANCE",
        persist_dir="artifacts/vectorestore/LOIS_DE_FINANCE",
        force_rebuild=False
    )
    return rag.run()

finance_law_tool = create_retriever_tool(
    _get_lf_retriever(),
    "loi_finances_maroc",
    """Annual Moroccan budget law (Loi de Finances): temporary fiscal measures, 
    rate changes, new exemptions, budget amendments for a SPECIFIC year. 
    Use ONLY when the user mentions a YEAR (e.g., 2024, 2025, 2026) or asks about 
    RECENT changes, NEW measures, or annual updates to tax rules.
    NOT for: permanent tax code (use cgi_maroc), accounting rules (use cgnc_maroc).
    Keywords: loi de finances 2024, loi de finances 2025, LF, mesure nouvelle, 
    réforme fiscale récente, amendement annuel, budget État."""
)