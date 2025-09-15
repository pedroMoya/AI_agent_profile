import streamlit as st

st.set_page_config(page_title="Health Report Orchestrator", layout="wide")

# --- Helper: convert multiline text into bullets without using backslashes in f-strings ---
def bullets_from_multiline(text: str, indent="  - "):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(f"{indent}{ln}" for ln in lines) if lines else f"{indent}(pending)"

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Problem Statement", "Solution & Key Roles", "Architecture", "Architecture (Icons)", "Flow (1–9)", "Impact", "Technology Stack", "Playground"],)

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
    st.graphviz_chart(dot, use_container_width="stretch")

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

elif page == "Technology Stack":
    st.title("Technology Stack (High-Level Architecture)")

    dot = r"""
    digraph G {
      rankdir=LR; splines=spline; fontname="Helvetica";
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
        langchain -> memory;
        langchain -> knowledge;
        langchain -> tools;
        langgraph -> memory;
        langgraph -> tools;
        system -> orchestrator [label="policy"];
      }

      patient  [label="Patient Request / Trigger"];
      clinician[label="Healthcare Professional"];
      insurer  [label="Insurance Company"];

      patient  -> profile;
      clinician-> profile;
      insurer  -> profile;

      orchestrator -> insurer [label="reports / status"];
      insurer -> system       [label="rules / templates"];

      subgraph cluster_interop {
        label="Interoperability & Standards";
        color=gray;
        mcp [label="MCP\n(Model Context Protocol)"];
      }
      mcp -- orchestrator [style=dashed, label="tool/runtime interop"];
    }
    """
    st.graphviz_chart(dot, use_container_width="stretch")

    st.subheader("Key Elements")
    st.markdown("""
- **LangChain** — LLM calls, tools, structured prompting (drafts, validations, ontology queries).  
- **LangGraph** — graph/state-based control for multi-step flows (auditable steps 1–9).  
- **Memory & Knowledge** — prior reports, insurer rules, compliance templates (RAG).  
- **Tools** — validators, template generators, EHR/insurer connectors.  
- **MCP (Model Context Protocol)** — interoperability across LLM runtimes/agents.  
- **Compliance bound
    y** — HIPAA/GDPR guardrails with human-in-the-loop.
    """)

elif page == "Architecture (Icons)":
    import base64
    from pathlib import Path
    import streamlit as st
    import streamlit.components.v1 as components

    st.title("Architecture (Icons & Connections)")
    st.caption("Pure HTML + SVG, responsive via viewBox and aspect-ratio (no Graphviz).")

    # --- 1) Locate icons directory ---
    BASE = Path(__file__).resolve().parent
    CANDIDATES = [
        BASE / "assets" / "icons",
        BASE / "sandbox" / "assets" / "icons",
        BASE.parent / "assets" / "icons",
        BASE.parent / "sandbox" / "assets" / "icons",
    ]
    ICON_DIR = next((p for p in CANDIDATES if p.exists()), CANDIDATES[0])

    @st.cache_data
    def icon_data_uri(path: Path) -> str:
        """Return a data: URI (base64) for a PNG file; empty string if missing."""
        if not path.exists():
            return ""
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{b64}"

    names = [
        "agent_profile","orchestrator","llm","system","langchain","langgraph",
        "memory","knowledge","tools","patient","clinician","insurer","mcp",
    ]
    icons = {n: icon_data_uri(ICON_DIR / f"{n}.png") for n in names}
    missing = [n for n, uri in icons.items() if not uri]
    if missing:
        st.warning(
            "Missing icons in: " + ICON_DIR.as_posix() +
            "\n- " + "\n- ".join(f"{m}.png" for m in missing)
        )

    # --- 2) Canvas & layout (intrinsic SVG coordinates) ---
    VW, VH = 1200, 720       # internal SVG width/height; scales responsively
    NODE_W, NODE_H = 180, 120
    ICON_SIZE = 48

    def pos(x, y):
        """Top-left (x,y) plus center coordinates for edge endpoints."""
        return {"x": x, "y": y, "cx": x + NODE_W/2, "cy": y + NODE_H/2}

    nodes = {
        # External actors
        "patient":      pos(  40, 100),
        "clinician":    pos(  40, 280),
        "insurer":      pos(  40, 460),
        # Compliance boundary (center)
        "profile":      pos( 320, 280),
        "orchestrator": pos( 560, 280),
        "llm":          pos( 560, 120),
        "system":       pos( 560, 440),
        "langchain":    pos( 800, 180),
        "langgraph":    pos( 800, 380),
        "memory":       pos(1020, 120),
        "knowledge":    pos(1020, 280),
        "tools":        pos(1020, 440),
        # Interoperability
        "mcp":          pos( 800, 560),
    }

    # Edges: (src, dst, label, style) where style is "solid" or "dashed-bidir"
    edges = [
        ("patient","profile","", "solid"),
        ("clinician","profile","", "solid"),
        ("insurer","profile","", "solid"),
        ("profile","orchestrator","context","solid"),
        ("orchestrator","llm","", "solid"),
        ("system","orchestrator","policy","solid"),
        ("orchestrator","langchain","", "solid"),
        ("orchestrator","langgraph","", "solid"),
        ("langchain","memory","", "solid"),
        ("langchain","knowledge","", "solid"),
        ("langchain","tools","", "solid"),
        ("langgraph","memory","", "solid"),
        ("langgraph","tools","", "solid"),
        ("orchestrator","insurer","reports/status","solid"),
        ("insurer","system","rules/templates","solid"),
        ("mcp","orchestrator","interop","dashed-bidir"),  # bidirectional interop
    ]

    # --- 3) Build responsive SVG ---
    def node_g(key: str, title: str, icon_uri: str, highlight=False) -> str:
        """Return an SVG group for a node (rounded card + icon + label)."""
        n = nodes[key]
        rx = 12
        border = "#2563eb" if highlight else "#cbd5e1"
        stroke_w = 2 if highlight else 1
        img_tag = (
            f'<image href="{icon_uri}" x="{(NODE_W-ICON_SIZE)/2}" y="12" width="{ICON_SIZE}" height="{ICON_SIZE}"/>'
            if icon_uri else ""
        )
        return f'''
        <g transform="translate({n["x"]},{n["y"]})">
          <rect width="{NODE_W}" height="{NODE_H}" rx="{rx}" ry="{rx}"
                fill="#f8fafc" stroke="{border}" stroke-width="{stroke_w}"/>
          {img_tag}
          <text x="{NODE_W/2}" y="{ICON_SIZE+36}" text-anchor="middle"
                font-family="Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
                font-size="12" font-weight="600" fill="#0f172a">{title}</text>
        </g>
        '''

    def edge_line(a: str, b: str, label: str, style: str) -> str:
        """Return an SVG line with arrowheads and an optional mid-label."""
        A, B = nodes[a], nodes[b]
        stroke = "#475569" if style.startswith("solid") else "#64748b"
        dash = 'stroke-dasharray="6,5"' if style.startswith("dashed") else ""
        # Arrowheads
        marker_end = 'marker-end="url(#arrow)"' if style.startswith("solid") else 'marker-end="url(#arrow-dashed)"'
        marker_start = marker_end if "bidir" in style else ""
        # Midpoint label
        mx, my = (A["cx"] + B["cx"]) / 2, (A["cy"] + B["cy"]) / 2 - 10
        label_el = (
            f'<text x="{mx}" y="{my}" font-size="11" text-anchor="middle" fill="#475569">{label}</text>'
            if label else ""
        )
        return f'''
          <line x1="{A["cx"]}" y1="{A["cy"]}" x2="{B["cx"]}" y2="{B["cy"]}"
                stroke="{stroke}" stroke-width="1.5" {dash} {marker_start} {marker_end} />
          {label_el}
        '''

    svg_edges = "\n".join(edge_line(*e) for e in edges)

    # Compliance rectangle (inside the SVG coordinate system)
    comp_x, comp_y, comp_w, comp_h = 300, 60, 820, 520

    # Responsive CSS + SVG:
    # - Wrapper uses width:100% and aspect-ratio to preserve proportions.
    # - SVG uses viewBox and scales to fill the wrapper.
    html = f"""
    <style>
      .svg-wrap {{
        position: relative;
        width: 100%;
        aspect-ratio: {VW} / {VH};
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
      }}
      .svg-wrap > svg {{
        width: 100%;
        height: 100%;
        display: block;
      }}
      .badge {{
        position: absolute;
        left: {comp_x + 12}px;
        top: {comp_y - 24}px;
        font: 600 12px/1 'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        color:#dc2626; background:#fff; padding:4px 8px; border:1px solid #fecaca; border-radius:8px;
        pointer-events: none;
      }}
    </style>

    <div class="svg-wrap">
      <svg viewBox="0 0 {VW} {VH}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#475569"/>
          </marker>
          <marker id="arrow-dashed" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#64748b"/>
          </marker>
        </defs>

        <!-- Compliance boundary rectangle -->
        <rect x="{comp_x}" y="{comp_y}" width="{comp_w}" height="{comp_h}" rx="14" ry="14"
              fill="none" stroke="#ef4444" stroke-width="2"/>

        <!-- Edges -->
        {svg_edges}

        <!-- Nodes -->
        {node_g("patient","Patient", icons["patient"])}
        {node_g("clinician","Healthcare Professional", icons["clinician"])}
        {node_g("insurer","Insurance Company", icons["insurer"])}

        {node_g("profile","Agent Profile", icons["agent_profile"], highlight=True)}
        {node_g("orchestrator","Agent (Orchestrator & Planner)", icons["orchestrator"])}
        {node_g("llm","LLM", icons["llm"])}
        {node_g("system","System message / policies", icons["system"])}
        {node_g("langchain","LangChain", icons["langchain"])}
        {node_g("langgraph","LangGraph", icons["langgraph"])}
        {node_g("memory","Memory store", icons["memory"])}
        {node_g("knowledge","Knowledge base", icons["knowledge"])}
        {node_g("tools","Specialized Tools", icons["tools"])}

        {node_g("mcp","MCP (Model Context Protocol)", icons["mcp"])}
      </svg>

      <div class="badge">Compliance Boundary: HIPAA / GDPR</div>
    </div>
    """

    # components.html needs a fixed iframe height; the SVG scales to width inside
    components.html(html, height=VH + 80, scrolling=False)


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
