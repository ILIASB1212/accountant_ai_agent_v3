from src.PipeLine.pipeline import  RagPipeLine

pipeline=RagPipeLine(data_dir="data/PLAN_COMPTABLE",persist_dir="artifacts/vectorestore/plan_comptable",force_rebuild=True)
pip=pipeline.run()


if __name__=="__main__":
    pip.invoke("tva recuperable")