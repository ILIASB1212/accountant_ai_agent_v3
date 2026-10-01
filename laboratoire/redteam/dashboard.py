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


def normalize_score(value) -> float | None:
    """
    Scores can show up as a real float (PAIR's 1-10 scale via
    SelfAskScaleScorer), a real bool, or -- from JSON files written before
    the _extract_final_score fix -- a string like "true"/"false"/"False".
    Normalize all of that to a plain 0.0-1.0-or-higher float so the chart
    below can treat PAIR and Crescendo consistently.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "false"):
            return 1.0 if lowered == "true" else 0.0
        try:
            return float(value)
        except ValueError:
            return None
    return None


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
df["score_numeric"] = df["score"].apply(normalize_score) if "score" in df.columns else None

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

st.caption(
    "'Objectives achieved' counts AttackOutcome.SUCCESS -- the guardrail "
    "stop all the specific attempt. Lower is better for your defenses."
)

st.divider()

# ── Per-objective breakdown ──
st.subheader("Per-objective outcomes")
if not df.empty:
    display_df = df[["attack_type", "objective", "outcome", "score"]].copy()
    display_df["objective"] = display_df["objective"].str.slice(0, 90) + "..."
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Pass/fail comparison chart (handles both PAIR's scale and Crescendo's binary scorer) ──
st.subheader("Guardrail held? (1 = attack succeeded, 0 = guardrail held)")
scored = df[df["score_numeric"].notna()].copy() if "score_numeric" in df.columns else pd.DataFrame()
if not scored.empty:
    scored["objective_short"] = scored["objective"].str.slice(0, 40) + "..."
    pivot = scored.pivot_table(
        index="objective_short", columns="attack_type", values="score_numeric", aggfunc="mean"
    )
    st.bar_chart(pivot)
else:
    st.info("No scores captured yet — check the raw outcome column above, or whether any runs errored.")

# ── Raw JSON, for anything the table doesn't show ──
with st.expander("Raw results (PAIR)"):
    st.json(pair_results)
with st.expander("Raw results (Crescendo)"):
    st.json(crescendo_results)
