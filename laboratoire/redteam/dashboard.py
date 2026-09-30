"""
Red-team results dashboard. Reads both JSON files produced by run_pair_attack.py
and run_crescendo_attack.py and shows a side-by-side comparison -- this is the
single-turn-style (PAIR) vs multi-turn-escalation (Crescendo) comparison
that actually matters: if Crescendo's success rate is much higher, that's
the concrete evidence that the guardrail's per-message-only design is a
real gap, not just a suspicion.

Run from the repo root:
    streamlit run laboratoire/redteam/dashboard.py
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

RESULTS_DIR = Path(__file__).resolve().parent / "results"

st.set_page_config(page_title="Red Team Dashboard", layout="wide")
st.title("🛡️ Accountant Agent — Red Team Results")


def load_results(filename: str) -> list[dict]:
    path = RESULTS_DIR / filename
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("results", [])


pair_results = load_results("pair_results.json")
crescendo_results = load_results("crescendo_results.json")

if not pair_results and not crescendo_results:
    st.warning(
        "No results found yet. Run `python laboratoire/redteam/run_pair_attack.py` "
        "and/or `python laboratoire/redteam/run_crescendo_attack.py` first."
    )
    st.stop()

all_results = pair_results + crescendo_results
df = pd.DataFrame(all_results)

# ── Top-line comparison ──
col1, col2, col3 = st.columns(3)


def success_rate(rows: list[dict]) -> str:
    if not rows:
        return "no data"
    successes = sum(1 for r in rows if "SUCCESS" in str(r.get("outcome", "")).upper())
    return f"{successes}/{len(rows)}"

with col1:
    st.metric("PAIR — objectives achieved", success_rate(pair_results))
with col2:
    st.metric("Crescendo — objectives achieved", success_rate(crescendo_results))
with col3:
    errors = sum(1 for r in all_results if r.get("outcome") == "ERROR")
    st.metric("Runs that errored", errors)

st.divider()

# ── Per-objective breakdown ──
st.subheader("Per-objective outcomes")
if not df.empty:
    display_df = df[["attack_type", "objective", "outcome", "score"]].copy()
    display_df["objective"] = display_df["objective"].str.slice(0, 90) + "..."
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Score comparison chart ──
st.subheader("Scale scores by objective")
scored = df[df["score"].notna()].copy()
if not scored.empty:
    scored["objective_short"] = scored["objective"].str.slice(0, 40) + "..."
    pivot = scored.pivot_table(index="objective_short", columns="attack_type", values="score", aggfunc="first")
    st.bar_chart(pivot)
else:
    st.info("No numeric scores captured yet — check the raw outcome column above.")

# ── Raw JSON, for anything the table doesn't show ──
with st.expander("Raw results (PAIR)"):
    st.json(pair_results)
with st.expander("Raw results (Crescendo)"):
    st.json(crescendo_results)
