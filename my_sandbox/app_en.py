import streamlit as st

st.set_page_config(page_title="Health Report Orchestrator", layout="wide")

# --- Helper: convert multiline text into bullets without using backslashes in f-strings ---
def bullets_from_multiline(text: str, indent="  - "):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(f"{indent}{ln}" for ln in lines) if lines else f"{indent}(pending)"

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Problem", "Architecture", "Flow (1–9)", "Playground"])

st.sidebar.markdown("---")
st.sidebar.subheader("Actors")
st.sidebar.checkbox("Patient", value=True, help="Requests benefits / requirements")
st.sidebar.checkbox("Healthcare professional", value=True, help="Issues reports")
st.sidebar.checkbox("Health insurance company", value=True, help="Receives and validates reports")

st.sidebar.markdown("---")
st.sidebar.subheader("Governance")
st.sidebar.checkbox("HIPAA / GDPR boundary", value=True)
st.sidebar.checkbox("Human-in-the-loop (step 9)", value=True)

# --- Problem view ---
if page == "Problem":
    st.title("Reports to activate health insurance benefits")

    st.markdown(
        """
        **Core problem:** the **medical reports** needed to activate **health insurance benefits**
        arrive **incomplete**, **late**, or get **rejected**, impacting both patient and insurer.
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Healthcare professional")
        st.markdown(
            "- Submits **health reports**\n"
            "  - They can remain **unfinished**\n"
            "  - They can be **delayed**"
        )
    with c2:
        st.subheader("Patient")
        st.markdown(
            "- **Does not receive** benefits on time\n"
            "- Risk of **rejection** due to requirements"
        )
    with c3:
        st.subheader("Health insurance company")
        st.markdown(
            "- **Does not orchestrate** a better system\n"
            "- Needs **standardization** and **traceability**"
        )

    st.info(
        "Goal: use an **agent** (LLM + memory/knowledge/tools) to orchestrate a flow that ensures "
        "complete, on‑time, policy‑compliant reports."
    )

# --- Architecture view ---
elif page == "Architecture":
    st.title("Proposed architecture (whiteboard → app)")
    st.caption("Compliance boundary: HIPAA / GDPR. The agent operates with supervision (human-in-the-loop).")

    dot = r"""
    digraph G {
      rankdir=LR;
      splines=spline;
      fontname="Helvetica";

      node [shape=box, style="rounded", fontsize=11, fontname="Helvetica"];
      edge [fontsize=10, fontname="Helvetica"];

      subgraph cluster_comp {
        label="Compliance: HIPAA / GDPR";
        color=red;

        agent_profile [label="Agent Profile"];
        agent [label="Agent\n(Orchestrator · Planning · 'Autonomous'*)"];
        llm [label="LLM"];
        system [label="System message"];
        memory [label="Memory"];
        knowledge [label="Knowledge"];
        tools [label="Tools"];

        # Internal relations
        agent_profile -> agent [label="(2)"];
        agent -> memory   [label="(4)"];
        agent -> knowledge[label="(4)"];
        agent -> tools    [label="(4)"];
        agent -> llm      [label="(5)"];
        llm   -> agent    [label="(6)"];
        system-> agent    [label="(7)"];
      }

      # External actors
      medical [label="Medical Act\n(trigger)"];
      patient [label="Patient\nRequest"];
      insurer [label="Health Insurance Company"];

      # Inputs into boundary
      medical -> agent_profile [label="(1)"];
      patient -> agent_profile [label="(2)"];
      insurer -> agent_profile [label="(3)"];

      # Outputs / feedback
      agent -> insurer [label="(8) Report/Status"];
      insurer -> system [label="(8) Rules/Templates"];

      # Human supervision
      patient -> agent [style=dashed, label="(9) Human-in-the-loop"];
    }
    """
    st.graphviz_chart(dot, use_container_width=True)

    st.caption("(*) 'Autonomous' within guardrails and with human review.")

# --- Steps / Flow view ---
elif page == "Flow (1–9)":
    st.title("Numbered flow (1–9)")
    st.markdown(
        """
        1. **Medical Act (trigger):** a clinical event requires a report.\n
        2. **Patient request:** benefits are requested; the Agent Profile captures case context.\n
        3. **Insurer → Agent Profile:** sends rules, templates, and validation criteria.\n
        4. **Agent uses Memory/Knowledge/Tools:** retrieves policies and utilities (e.g., templates, validators).\n
        5. **Agent → LLM:** drafts/plans checklists and report content.\n
        6. **LLM → Agent:** returns text/plan; the agent decides next steps.\n
        7. **System message:** sets policies, tone, and limits during orchestration.\n
        8. **Exchange with insurer:** submit reports/status; receive rules/observations.\n
        9. **Human-in-the-loop:** clinician verifies/edits before sending; patient can follow status.
        """
    )

# --- Playground ---
else:
    st.title("Playground: checklist & draft prototype")
    st.markdown("**Goal:** prepare a requirements checklist and a report skeleton to send to the insurer.")

    with st.form("form_playground"):
        colA, colB = st.columns(2)
        with colA:
            insurer = st.text_input("Insurance company", placeholder="e.g., SaludPlus")
            trigger = st.text_input("Medical Act (trigger)", placeholder="e.g., outpatient surgery / sick leave")
            diagnosis = st.text_input("Primary diagnosis / reason", placeholder="e.g., acute lumbosciatica")
        with colB:
            date_val = st.date_input("Report date")
            professional = st.text_input("Responsible clinician", placeholder="Dr./MD ____")
            case_id = st.text_input("Case / Folio (optional)")

        st.markdown("**Clinical evolution / changes since last report**")
        evolution = st.text_area(
            "Enter ONLY the changes with their date",
            height=120,
            placeholder="Ex.: 2025-09-12: physiotherapy started; 2025-09-14: pain decreased to 3/10…",
        )

        submitted = st.form_submit_button("Generate checklist + draft")

    if submitted:
        # Precompute bullets to avoid backslashes inside f-strings
        evo_bullets = bullets_from_multiline(evolution, indent="  - ")

        st.subheader("Suggested checklist")
        st.markdown(
            f"""
- Case identification (folio: **{case_id or 'n/a'}**), responsible clinician and date **{date_val}**  
- Medical Act triggering the benefit: **{trigger or '—'}**  
- Primary diagnosis / reason: **{diagnosis or '—'}**  
- Evolution **changes only** with date (format *YYYY-MM-DD*):  
{evo_bullets}
- Attachments required by **{insurer or '(define)'}**:  
  - Medical order / discharge summary  
  - Signed clinical report (PDF)  
  - Supporting tests (if applicable)  
  - Insurer-specific certificates/templates  
- Verify **deadlines** and **format** (HIPAA/GDPR compliance)  
- Final **human review** (step 9) and submission log
            """
        )

        st.subheader("Report draft (skeleton)")
        draft = f"""
MEDICAL REPORT — Benefit activation
Insurance: {insurer or '—'}    |    Date: {date_val}
Clinician: {professional or '—'}    |    Case/Folio: {case_id or 'n/a'}

1) Medical Act (trigger)
   - {trigger or '—'}

2) Primary diagnosis / reason
   - {diagnosis or '—'}

3) Evolution (changes only, each with date)
{evolution if evolution.strip() else '- (to be completed by the clinician)'}

4) Clinical rationale & supporting evidence
   - Key findings, attached exams, applicable guidelines.

5) Request to insurer
   - Coverage/benefit requested and estimated duration.

6) Compliance & privacy
   - Prepared under HIPAA/GDPR good practices.
""".strip()
        st.code(draft, language="markdown")

    st.caption("This playground does not replace clinical or legal judgment; it supports the operational flow.")
