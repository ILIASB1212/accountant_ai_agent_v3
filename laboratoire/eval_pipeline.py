"""
RAGAS evaluation of the Moroccan Accounting Agent, traced in LangSmith.

Drop-in replacement for eval_lab.ipynb cells 3/5/6. Same golden dataset
(data.json), same LangSmith dataset name, same RAGAS metric set — but:
  - each metric is scored independently (single_turn_ascore), so one
    metric failing no longer wipes out the other four for that example
    (this is why feedback.ragas_langsmith_evaluator was all-NaN before:
    ragas.evaluate() on a one-row Dataset raises on ANY metric error,
    which kills the whole feedback list for that run)
  - scores are read back from LangSmith's own ExperimentResults object,
    not from eval_results.to_pandas(), so what lands in the .md file is
    guaranteed to be what LangSmith actually recorded
  - one consistent RAGAS API (class-based) instead of two mixed styles

Run from the repo root:
    python laboratoire/eval_pipeline.py

Produces: laboratoire/evaluation/ragas_summary_report.md
"""

import asyncio
import json
import os
import sys
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ── Make `from src...` importable regardless of cwd ──
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langsmith import Client, evaluate
from langsmith.evaluation import run_evaluator

from ragas import SingleTurnSample
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    AnswerCorrectness,
    AnswerSimilarity,
    AnswerRelevancy,
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
)

from src.agentic_workflow.agent import graph

load_dotenv()

DATA_PATH = Path(__file__).resolve().parent / "data.json"
REPORT_DIR = Path(__file__).resolve().parent / "evaluation"
REPORT_PATH = REPORT_DIR / "ragas_summary_report.md"
DATASET_NAME = "Moroccan_Accounting_Golden_V2"
EXPERIMENT_PREFIX = "RAGAS-LangGraph-Run"

client = Client()

# ── RAGAS metrics: one shared judge LLM/embeddings, scored independently ──
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini", temperature=0))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

METRICS = {
    "faithfulness": Faithfulness(llm=evaluator_llm),
    "answer_correctness": AnswerCorrectness(
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
        answer_similarity=AnswerSimilarity(embeddings=evaluator_embeddings),
    ),
    "answer_relevancy": AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
    "context_precision": LLMContextPrecisionWithReference(llm=evaluator_llm),
    "context_recall": LLMContextRecall(llm=evaluator_llm),
}

_case_counter = 0


_LOOP = asyncio.new_event_loop()  # one persistent loop: avoids "Event loop is closed" with reused async clients
_LOOP_LOCK = threading.Lock()


def _run_async(coro):
    with _LOOP_LOCK:
        return _LOOP.run_until_complete(coro)


# ================================================================
# 1. Agent target function — invoked once per golden example
# ================================================================
def predict_agent_answer(inputs: dict) -> dict:
    global _case_counter
    _case_counter += 1

    user_input = inputs["user_input"]
    preview = user_input.replace("\n", " ")[:60]
    print(f"\n Running case {_case_counter}: {preview}...")

    config = {"configurable": {"thread_id": f"ragas_eval_{_case_counter}"}}
    final_state = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)

    retrieved_contexts, output_messages = [], []
    for msg in final_state["messages"]:
        if isinstance(msg, ToolMessage):
            retrieved_contexts.append(str(msg.content))
        elif msg.type == "ai" and msg.content and not msg.tool_calls:
            output_messages.append(msg.content)

    return {
        "response": output_messages[-1] if output_messages else "No response generated",
        "retrieved_contexts": retrieved_contexts if retrieved_contexts else ["No context retrieved"],
    }


# ================================================================
# 2. Scoring: each RAGAS metric scored independently and defensively
# ================================================================
def score_all_metrics(user_input: str, response: str, retrieved_contexts: list, reference: str) -> dict:
    sample = SingleTurnSample(
        user_input=user_input,
        response=response,
        retrieved_contexts=retrieved_contexts,
        reference=reference,
    )

    async def _score_one(name, metric):
        try:
            return name, await metric.single_turn_ascore(sample)
        except Exception as exc:  # a single metric failing must not blank the rest
            print(f"   ⚠️  {name} failed for this case: {exc}")
            return name, None

    async def _score_all():
        # all 5 metrics run concurrently -> roughly 5x faster per case
        return await asyncio.gather(*[_score_one(n, m) for n, m in METRICS.items()])

    return dict(_run_async(_score_all()))


# ================================================================
# 3. Native LangSmith evaluator — attaches each metric as its own feedback key
# ================================================================
@run_evaluator
def ragas_langsmith_evaluator(run, example):
    user_input = example.inputs.get("user_input", "")
    ground_truth = example.outputs.get("ground_truth", "")
    response = run.outputs.get("response", "")
    contexts = run.outputs.get("retrieved_contexts", ["No context retrieved"])

    scores = score_all_metrics(user_input, response, contexts, ground_truth)

    # LangSmith requires the {"results": [...]} wrapper for multiple feedback keys
    return {
        "results": [
            {"key": name, "score": score}
            for name, score in scores.items()
            if score is not None
        ]
    }


# ================================================================
# 4. Dataset setup (reuses the dataset if it already exists)
# ================================================================
def setup_langsmith_dataset(dataset_name: str, json_path: Path):
    if client.has_dataset(dataset_name=dataset_name):
        print(f"📌 Reusing existing LangSmith dataset: '{dataset_name}'")
        return client.read_dataset(dataset_name=dataset_name)

    print(f"🚀 Creating LangSmith dataset: '{dataset_name}'")
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Golden Dataset for Moroccan Accounting RAG Evaluation",
    )
    with open(json_path, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    inputs = [{"user_input": item["user_input"]} for item in golden_data]
    outputs = [{"ground_truth": item["expected_output"]} for item in golden_data]
    client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)
    return dataset


# ================================================================
# 5. Markdown report — built from what LangSmith actually recorded,
#    not from eval_results.to_pandas() (that's the part that was silently empty)
# ================================================================
def write_markdown_report(rows: list[dict], experiment_name: str):
    metric_names = list(METRICS.keys())
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    def avg(metric):
        vals = [r[metric] for r in rows if r.get(metric) is not None]
        return sum(vals) / len(vals) if vals else None

    lines = []
    lines.append("# RAGAS Evaluation Summary Report")
    lines.append("")
    lines.append(f"- **Dataset:** `{DATASET_NAME}`")
    lines.append(f"- **Experiment:** `{experiment_name}`")
    lines.append(f"- **Generated:** {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- **Cases evaluated:** {len(rows)}")
    lines.append("")
    lines.append("## Overall Metric Averages")
    lines.append("")
    lines.append("| Metric | Average Score | Scored / Total |")
    lines.append("| :--- | :--- | :--- |")
    for m in metric_names:
        scored = sum(1 for r in rows if r.get(m) is not None)
        a = avg(m)
        a_str = f"{a:.4f}" if a is not None else "N/A"
        lines.append(f"| **{m.replace('_', ' ').title()}** | {a_str} | {scored}/{len(rows)} |")
    lines.append("")
    lines.append("## Per-Question Breakdown")
    lines.append("")

    for i, r in enumerate(rows, start=1):
        lines.append(f"### Question {i}")
        lines.append("")
        lines.append(f"**User input:**\n> {r['user_input']}")
        lines.append("")
        lines.append(f"**Expected (ground truth):**\n```text\n{r['ground_truth']}\n```")
        lines.append("")
        lines.append(f"**Agent response:**\n```text\n{r['response']}\n```")
        lines.append("")
        lines.append("| Metric | Score |")
        lines.append("| :--- | :--- |")
        for m in metric_names:
            val = r.get(m)
            lines.append(f"| {m.replace('_', ' ').title()} | {f'{val:.4f}' if val is not None else 'N/A'} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✅ Report written to: {REPORT_PATH}")


# ================================================================
# 6. Main
# ================================================================
def main():
    global _case_counter
    _case_counter = 0

    setup_langsmith_dataset(DATASET_NAME, DATA_PATH)

    print("\n🔍 Running agent + RAGAS scoring through LangSmith...")
    eval_results = evaluate(
        predict_agent_answer,
        data=DATASET_NAME,
        evaluators=[ragas_langsmith_evaluator],
        experiment_prefix=EXPERIMENT_PREFIX,
        metadata={"version": "2.0.0"},
    )

    # Read back what LangSmith actually recorded per example — NOT
    # eval_results.to_pandas(), which silently dropped feedback last time.
    rows = []
    experiment_name = getattr(eval_results, "experiment_name", EXPERIMENT_PREFIX)
    for item in eval_results:
        run = item["run"]
        example = item["example"]
        result_list = item.get("evaluation_results", {}).get("results", [])

        row = {
            "user_input": example.inputs.get("user_input", ""),
            "ground_truth": example.outputs.get("ground_truth", ""),
            "response": run.outputs.get("response", "") if run.outputs else "",
        }
        for res in result_list:
            row[res.key] = res.score
        rows.append(row)

    write_markdown_report(rows, experiment_name)
    print("✅ Done. Every score in the .md file came straight from the LangSmith run results.")


if __name__ == "__main__":
    main()