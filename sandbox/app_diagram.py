#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent Orchestrator — Health Insurance Benefits
Streamlit app (Python 3.11) to diagram the architecture and the problem/solution in English.
"""
from __future__ import annotations

import streamlit as st
from graphviz import Digraph

st.set_page_config(
    page_title="AI Agent Orchestrator — Health Insurance",
    layout="wide",
    page_icon="🧭",
)

st.title("AI Agent Orchestrator — Health Insurance Benefits")
st.write(
    "Interactive diagrams (in English) that capture the architecture and the problem/solution "
    "for automating health insurance benefit activation with an AI agent orchestrator."
)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Settings")
compliance_label = st.sidebar.text_input("Compliance boundary label", "HIPAA / GDPR")
show_numbers = st.sidebar.checkbox("Show step numbers on arrows", value=True)
show_hitl = st.sidebar.checkbox("Show Human-in-the-Loop", value=True)

# -----------------------------
# Helper to prefix numbered labels
# -----------------------------
def num(i: int, text: str) -> str:
    return f"({i}) {text}" if show_numbers else text

# -----------------------------
# Architecture diagram
# -----------------------------
def make_architecture_diagram() -> Digraph:
    g = Digraph("architecture", graph_attr={
        "rankdir": "LR",
        "splines": "spline",
        "fontname": "Helvetica"
    }, node_attr={
        "shape": "box",
        "style": "rounded",
        "fontname": "Helvetica"
    }, edge_attr={
        "fontname": "Helvetica"
    })

    # External actors
    g.node("patient", "Patient")
    g.node("medical", "Medical Act\n(trigger)")
    g.node("insurer", "Health Insurance\nCompany")

    # Secure boundary
    with g.subgraph(name="cluster_boundary") as b:
        b.attr(label=f"Secure Boundary — {compliance_label}")
        b.attr(style="rounded")
        b.node("profile", "Agent Profile")
        b.node("llm", "LLM")
        b.node("sysmsg", "System Message")

        # Agent orchestrator
        with b.subgraph(name="cluster_agent") as a:
            a.attr(label='AI Agent "Orchestrator"\\nPlanning • Coordination • Autonomy')
            a.attr(style="rounded")
            a.node("agent", "Agent Orchestrator")

        # Cognition/tooling
        with b.subgraph(name="cluster_cognition") as c:
            c.attr(label="Capabilities")
            c.attr(style="rounded")
            c.node("memory", "Memory")
            c.node("knowledge", "Knowledge")
            c.node("tools", "Tools")

        # Optional Human in the Loop
        if show_hitl:
            b.node("hitl", "Human-in-the-Loop", style="dashed")

        # Internal edges
        b.edge("agent", "memory", label=num(4, "read/write"), dir="both")
        b.edge("agent", "knowledge", label=num(4, "retrieve"), dir="both")
        b.edge("agent", "tools", label=num(4, "invoke"), dir="both")
        b.edge("agent", "llm", label=num(5, "reason / generate"), dir="both")
        b.edge("sysmsg", "agent", label=num(6, "policy & guardrails"))
        b.edge("agent", "sysmsg", label=num(7, "status & rationale"))
        if show_hitl:
            b.edge("hitl", "agent", style="dashed", label=num(9, "review & approve"), dir="both")

    # Edges crossing the boundary
    g.edge("medical", "profile", label=num(1, "trigger"))
    g.edge("patient", "profile", label=num(2, "requirement / request"))
    g.edge("insurer", "profile", label=num(3, "payer rules / plan data"))
    g.edge("insurer", "sysmsg", label=num(8, "notifications & validation"), dir="both")

    # Layout nudges
    g.edge("profile", "agent", style="invis")  # helps place profile near agent
    return g

# -----------------------------
# Problem & solution diagram
# -----------------------------
def make_problem_solution_diagram() -> Digraph:
    g = Digraph("problem_solution", graph_attr={
        "rankdir": "TB",
        "splines": "spline",
        "fontname": "Helvetica"
    }, node_attr={
        "shape": "box",
        "style": "rounded",
        "fontname": "Helvetica"
    }, edge_attr={
        "fontname": "Helvetica"
    })

    g.node("problem", "Problem: Activating health insurance benefits requires complete, timely, compliant medical reports")

    with g.subgraph(name="cluster_roles") as r:
        r.attr(label="Friction by Stakeholder", style="rounded")
        r.node("mp", "Medical Professionals\n• admin burden\n• report quality varies")
        r.node("pt", "Patients\n• no/slow access to benefits")
        r.node("ic", "Insurance Company\n• weak orchestration\n• manual reviews")
        r.edge("mp", "problem")
        r.edge("pt", "problem")
        r.edge("ic", "problem")

    with g.subgraph(name="cluster_effects") as e:
        e.attr(label="Downstream Effects", style="rounded")
        e.node("unfinished", "Unfinished reports")
        e.node("delayed", "Delayed submissions")
        e.node("rejected", "Rejected claims")
        e.edge("problem", "unfinished")
        e.edge("problem", "delayed")
        e.edge("problem", "rejected")

    with g.subgraph(name="cluster_solution") as s:
        s.attr(label="Solution", style="rounded")
        s.node("orchestrator", "AI Agent Orchestrator\n• guides structured reporting\n• validates & completes docs\n• coordinates with payer\n• keeps humans in the loop")
        s.node("outcomes", "Outcomes\n• faster benefits\n• fewer rejections\n• auditability & compliance")
        s.edge("orchestrator", "outcomes")

    g.edge("problem", "orchestrator", label="address with")
    return g

# -----------------------------
# UI
# -----------------------------
tab1, tab2 = st.tabs(["Architecture", "Problem & Solution"])

with tab1:
    st.subheader("Architecture")
    arch = make_architecture_diagram()
    st.graphviz_chart(arch, width='stretch')
    st.caption("Numbers on arrows correspond to the main flow steps.")
    st.download_button("Download architecture .dot", data=arch.source, file_name="architecture.dot", mime="text/plain")
    with st.expander("Show DOT source"):
        st.code(arch.source, language="dot")

with tab2:
    st.subheader("Problem & Solution")
    ps = make_problem_solution_diagram()
    st.graphviz_chart(ps, width='stretch')
    st.download_button("Download problem-solution .dot", data=ps.source, file_name="problem_solution.dot", mime="text/plain")
    with st.expander("Show DOT source"):
        st.code(ps.source, language="dot")

st.markdown("---")
