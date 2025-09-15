import streamlit as st

st.set_page_config(page_title="Health Report Orchestrator", layout="wide")

# --- Helper: convert multiline text into bullets without using backslashes in f-strings ---
def bullets_from_multiline(text: str, indent="  - "):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(f"{indent}{ln}" for ln in lines) if lines else f"{indent}(pending)"

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Problem Statement", "Architecture (Graphviz)", "Flow (1–9)", "Technology Stack", "Architecture (SVG Icons)", "Playground"],)

if page == "Problem Statement":
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
        "complete, on-time, policy-compliant reports."
    )

# --- Architecture view (Graphviz) ---
elif page == "Architecture (Graphviz)":
    st.title("Proposed architecture (whiteboard → app)")
    st.caption("Compliance Boundary: HIPAA / GDPR. The agent operates with supervision (human-in-the-loop).")

    dot = r"""
    digraph G {
      rankdir=LR;
      splines=spline;
      fontname="Helvetica";

      node [shape=box, style="rounded", fontsize=11, fontname="Helvetica"];
      edge [fontsize=10, fontname="Helvetica"];

      subgraph cluster_comp {
        label="Compliance Boundary: HIPAA / GDPR";
        color=red;

        profile     [label="Agent Profile"];
        orchestrator[label="Agent\n(Orchestrator & Planner)"];
        langchain   [label="LangChain\n(LLM + Tools orchestration)"];
        langgraph   [label="LangGraph\n(Graph-based workflow)"];
        memory      [label="Memory store"];
        knowledge   [label="Knowledge base"];
        tools       [label="Specialized Tools"];
        system      [label="System message / policies"];

        profile -> orchestrator [label="context"];
        orchestrator -> langchain;
        orchestrator -> langgraph;
        langchain -> tools;
        langgraph -> tools;

        knowledge -> langchain;
        memory -> langchain;
        system -> orchestrator;
      }

      # Outside boundary
      medical [label="Medical Act\n(trigger)"];
      patient [label="Patient\nRequest"];
      insurer [label="Health Insurance Company"];

      # Inputs into boundary
      medical -> profile [label="(1)"];
      patient -> profile [label="(2)"];
      insurer -> profile [label="(3)"];

      # Outputs / feedback
      orchestrator -> insurer [label="(8) Report/Status"];
    }
    """
    try:
        from graphviz import Source
        st.graphviz_chart(dot, use_container_width=True)
    except Exception as e:
        st.warning("Graphviz is not available in this environment.")
        st.code(dot, language="dot")

# --- Flow view ---
elif page == "Flow (1–9)":
    st.title("Operational flow (1–9)")
    st.markdown(
        """
        1) Trigger: medical act (e.g., discharge, exam, or consultation)  
        2) Patient request / requirements  
        3) Insurance policy → rules/templates  
        4) Agent orchestrates required **documents & data**  
        5) Clinician composes the report (human-in-the-loop)  
        6) Compliance checks (HIPAA/GDPR good practices)  
        7) Attachments: orders, signed PDF, tests, insurer forms  
        8) Submit to insurer (status & traceability)  
        9) Feedback loop → improve prompts/templates  
        """
    )

# --- Technology Stack ---
elif page == "Technology Stack":
    st.title("Technology Stack & boundary")
    st.markdown(
        """
        **Core**  
        - Streamlit (UI)  
        - Python (ETL + orchestration)  
        - LLM provider (planning, drafting, validation)

        **Memory & Knowledge**  
        - Vector store / DB  
        - Policy & templates

        **Tools**  
        - PDF generation/signing  
        - Email/HTTP clients  
        - Schedulers

        **Compliance Boundary**  
        - HIPAA / GDPR  
        - Logging, audit trails, and data minimization
        """
    )

# --- Architecture (SVG Icons) ---
elif page == "Architecture (SVG Icons)":
    st.title("Architecture (SVG Icons)")
    st.caption("Compliance Boundary: HIPAA / GDPR. The agent operates with supervision (human-in-the-loop).")

    import streamlit.components.v1 as components

    # Simple inline SVG/HTML illustrative diagram (icons/labels are placeholders).
    VH = 560
    html = f"""
    <style>
      .arch-wrap {{ width:100%; max-width:1200px; margin:0 auto; }}
      .badge {{ margin-top:8px; font: 13px/1.4 Helvetica, Arial, sans-serif; color:#444; }}
      svg text {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; }}
      .node {{ rx:10; ry:10; }}
      .comp {{ fill:none; stroke:#ea4335; stroke-width:2; }}
    </style>
    <div class="arch-wrap">
      <svg viewBox="0 0 1200 {VH}" width="100%" height="{VH}">
        <rect class="comp" x="40" y="40" width="1120" height="{VH-120}"></rect>
        <text x="52" y="60" fill="#ea4335">Compliance Boundary: HIPAA / GDPR</text>

        <!-- Nodes (illustrative) -->
        <rect x="80" y="90" width="180" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="90" y="120">Agent Profile</text>

        <rect x="300" y="90" width="220" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="310" y="120">Agent (Orchestrator & Planner)</text>

        <rect x="560" y="90" width="170" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="570" y="120">LangChain</text>

        <rect x="760" y="90" width="170" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="770" y="120">LangGraph</text>

        <rect x="960" y="90" width="160" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="970" y="120">Specialized Tools</text>

        <rect x="300" y="170" width="220" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="310" y="200">System message / policies</text>

        <rect x="560" y="170" width="170" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="570" y="200">Memory store</text>

        <rect x="760" y="170" width="170" height="48" fill="#f1f3f4" class="node"></rect>
        <text x="770" y="200">Knowledge base</text>

        <!-- External -->
        <text x="80" y="260">Medical Act (trigger)</text>
        <text x="80" y="280">Patient Request</text>
        <text x="80" y="300">Health Insurance Company</text>
      </svg>

      <div class="badge">Compliance Boundary: HIPAA / GDPR</div>
    </div>
    """

    # components.html needs a fixed iframe height; the SVG scales to width inside
    components.html(html, height=VH + 80, scrolling=False)

# --- Playground ---
elif page == "Playground":
    st.title("Playground: checklist & draft prototype")

    st.subheader("Checklist for submission")
    st.markdown(
        """
- Validate **identity** of patient and clinician (names, IDs).
- Confirm **policy** and **requirements** for the insurance company.
- Ensure **attachments** are listed and complete.
- Verify **dates** and **deadlines** (avoid rejections).
- Final **human review** (clinical and legal sense).
        """
    )

    st.subheader("Report draft (skeleton)")
    professional = st.text_input("Healthcare professional")
    insurer = st.text_input("Health insurance company")
    case_id = st.text_input("Case / Folio")
    date_val = st.date_input("Date")

    st.caption("This playground does not replace clinical or legal judgment; it supports the operational flow.")
