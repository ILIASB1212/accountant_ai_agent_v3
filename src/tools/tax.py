from functools import lru_cache
from src.PipeLine.pipeline import RagPipeLine
from langchain_classic.tools.retriever import create_retriever_tool

@lru_cache(maxsize=1)
def _get_cgi_retriever():
    rag = RagPipeLine(
        data_dir="./data/CGI",
        persist_dir="artifacts/vectorestore/db_CGI",
        force_rebuild=False
    )
    return rag.run()

CGI_tool = create_retriever_tool(
    _get_cgi_retriever(),
    "cgi_maroc",
    """Moroccan Tax Code (CGI): permanent tax law. IS corporate tax, IR income tax, 
    TVA VAT (7/10/14/20%), TIC, registration duties, withholding tax, tax deductions, 
    amortissement fiscal, déficit reportable, exonérations, contrôle fiscal, pénalités.
    Use for: tax RATES, tax DEDUCTION rules, tax ARTICLES, permanent fiscal law.
    NOT for: annual budget changes (use loi_finances), accounting entries (use plan_comptable).
    Keywords: impôt, taxe, IS, IR, TVA, CGI, retenue, exonération, déduction fiscale, 
    base imposable, taux, article fiscal, droits d'enregistrement."""
)