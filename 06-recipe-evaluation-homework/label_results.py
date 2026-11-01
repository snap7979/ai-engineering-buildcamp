import csv
import json
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
RESULTS_PATH = APP_DIR / "results.json"
LABELS_PATH = APP_DIR / "labels.csv"
CSV_FIELDS = ("case_id", "question", "category", "type", "label", "comments")


def load_labels():
    if not LABELS_PATH.exists():
        return {}

    with LABELS_PATH.open(newline="", encoding="utf-8") as labels_file:
        return {
            row["case_id"]: row
            for row in csv.DictReader(labels_file)
            if row.get("case_id")
        }


def save_review(case_id, item):
    labels = load_labels()
    labels[str(case_id)] = {
        "case_id": str(case_id),
        "question": item["question"],
        "category": item["category"],
        "type": item["type"],
        "label": st.session_state[f"label_{case_id}"],
        "comments": st.session_state[f"comments_{case_id}"],
    }

    with LABELS_PATH.open("w", newline="", encoding="utf-8") as labels_file:
        writer = csv.DictWriter(labels_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(labels[key] for key in sorted(labels, key=int))


def move_case(offset, case_count):
    st.session_state.case_index = min(
        max(st.session_state.case_index + offset, 0), case_count - 1
    )


st.set_page_config(page_title="Recipe Response Labeling", layout="wide")
st.title("Recipe Assistant: Label the Results")

with RESULTS_PATH.open(encoding="utf-8") as results_file:
    responses = json.load(results_file)

labels = load_labels()
case_count = len(responses)
if case_count == 0:
    st.info("No responses found in results.json.")
    st.stop()

reviewed_count = sum(row.get("label") in {"Good", "Bad"} for row in labels.values())
bad_count = sum(row.get("label") == "Bad" for row in labels.values())
st.progress(reviewed_count / case_count, text=f"Reviewed {reviewed_count} of {case_count}")
st.caption(f"Bad labels: {bad_count}")

if "case_index" not in st.session_state:
    st.session_state.case_index = 0

case_index = st.session_state.case_index
case_id = case_index + 1
item = responses[case_index]
saved = labels.get(str(case_id), {})
label_key = f"label_{case_id}"
comments_key = f"comments_{case_id}"

if label_key not in st.session_state:
    saved_label = saved.get("label", "")
    st.session_state[label_key] = saved_label if saved_label in {"Good", "Bad"} else "Unlabeled"
if comments_key not in st.session_state:
    st.session_state[comments_key] = saved.get("comments", "")

st.caption(f"Case {case_id} of {case_count}")
st.markdown(f"**Category:** {item['category']}  \n**Type:** {item['type']}")
st.subheader("Question")
st.write(item["question"])
st.subheader("Agent answer")
st.markdown(item["output"])

st.radio(
    "Label",
    options=("Unlabeled", "Good", "Bad"),
    horizontal=True,
    key=label_key,
    on_change=save_review,
    args=(case_id, item),
)
st.text_area(
    "Evidence-based comments",
    key=comments_key,
    on_change=save_review,
    args=(case_id, item),
    placeholder="Note the specific evidence in the answer that supports your label.",
)

previous_column, next_column = st.columns(2)
with previous_column:
    st.button(
        "Previous",
        disabled=case_index == 0,
        on_click=move_case,
        args=(-1, case_count),
        use_container_width=True,
    )
with next_column:
    st.button(
        "Next",
        disabled=case_index == case_count - 1,
        on_click=move_case,
        args=(1, case_count),
        use_container_width=True,
    )