import streamlit as st

st.set_page_config(page_title="Orquestador de Reportes de Salud", layout="wide")

# --- Sidebar ---
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Problema", "Arquitectura", "Flujo (1–9)", "Playground"])

st.sidebar.markdown("---")
st.sidebar.subheader("Actores")
st.sidebar.checkbox("Paciente", value=True, help="Solicitante de beneficios / requerimientos")
st.sidebar.checkbox("Profesional de la salud", value=True, help="Emite informes")
st.sidebar.checkbox("Aseguradora de salud", value=True, help="Recibe y valida informes")

st.sidebar.markdown("---")
st.sidebar.subheader("Gobernanza")
st.sidebar.checkbox("HIPAA / GDPR (frontera de cumplimiento)", value=True)
st.sidebar.checkbox("Human-in-the-loop (paso 9)", value=True)

# --- Problem view ---
if page == "Problema":
    st.title("Reports to activate health insurance benefits")

    st.markdown(
        """
        **Problema central:** los **informes médicos** que activan **beneficios de seguro de salud**
        llegan **incompletos**, **tarde** o son **rechazados**, afectando al paciente y a la aseguradora.
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Profesional de la salud")
        st.markdown(
            "- Entrega **informes de salud**\n"
            "  - Pueden quedar **sin finalizar**\n"
            "  - Pueden enviarse **con retraso**"
        )
    with c2:
        st.subheader("Paciente")
        st.markdown(
            "- **No recibe** beneficios a tiempo\n"
            "- Riesgo de **rechazo** por requisitos"
        )
    with c3:
        st.subheader("Aseguradora de salud")
        st.markdown(
            "- **No orquesta** un sistema mejor\n"
            "- Necesita **estandarización** y **trazabilidad**"
        )

    st.info(
        "Objetivo: orquestar con un **agente** (LLM + memoria/conocimiento/herramientas) un flujo "
        "que asegure informes completos, en plazo y conformes a normativa."
    )

# --- Architecture view ---
elif page == "Arquitectura":
    st.title("Arquitectura propuesta (tipo pizarra → app)")
    st.caption("Frontera de cumplimiento: HIPAA / GDPR. El agente opera supervisado (human-in-the-loop).")

    dot = r"""
    digraph G {
      rankdir=LR;
      splines=spline;
      fontname="Helvetica";

      node [shape=box, style="rounded", fontsize=11, fontname="Helvetica"];
      edge [fontsize=10, fontname="Helvetica"];

      subgraph cluster_comp {
        label="Cumplimiento: HIPAA / GDPR";
        color=red;

        agent_profile [label="Agent Profile"];
        agent [label="Agent\n(Orchestrator · Planning · 'Autónomo'*)"];
        llm [label="LLM"];
        system [label="System message"];
        memory [label="Memory"];
        knowledge [label="Knowledge"];
        tools [label="Tools"];

        # Relaciones internas
        agent_profile -> agent [label="(2)"];
        agent -> memory   [label="(4)"];
        agent -> knowledge[label="(4)"];
        agent -> tools    [label="(4)"];
        agent -> llm      [label="(5)"];
        llm   -> agent    [label="(6)"];
        system-> agent    [label="(7)"];
      }

      # Actores externos
      medical [label="Acto médico\n(trigger)"];
      patient [label="Paciente\nRequerimiento (request)"];
      insurer [label="Aseguradora de salud"];

      # Entradas a la frontera
      medical -> agent_profile [label="(1)"];
      patient -> agent_profile [label="(2)"];
      insurer -> agent_profile [label="(3)"];

      # Salidas / retroalimentación
      agent -> insurer [label="(8) Informe/estado"];
      insurer -> system [label="(8) Reglas/plantillas"];

      # Supervisión humana
      patient -> agent [style=dashed, label="(9) Human-in-the-loop"];
    }
    """
    st.graphviz_chart(dot, use_container_width=True)

    st.caption("(*) 'Autónomo' dentro de guardas de seguridad y con revisión humana.")

# --- Steps / Flow view ---
elif page == "Flujo (1–9)":
    st.title("Flujo numerado (1–9)")
    st.markdown(
        """
        1. **Acto médico (trigger):** ocurre un evento clínico que requiere informe.\n
        2. **Requerimiento del paciente:** se solicita activar beneficios; el perfil del agente recoge contexto del caso.\n
        3. **Aseguradora → Perfil del agente:** entrega reglas, plantillas y criterios de validación.\n
        4. **Agente usa Memory/Knowledge/Tools:** recupera antecedentes, políticas y herramientas (por ej., generador de plantillas, validadores).\n
        5. **Agente → LLM:** redacta/planifica borradores y checklists.\n
        6. **LLM → Agente:** devuelve texto/plan; el agente decide próximos pasos.\n
        7. **System message:** define políticas, tono y límites del LLM en tiempo de orquestación.\n
        8. **Intercambio con aseguradora:** se envían informes/estados y se reciben reglas/observaciones.\n
        9. **Human-in-the-loop:** el profesional verifica/edita antes de enviar; el paciente puede seguir el estado.
        """
    )

# --- Playground ---
else:
    st.title("Playground: prototipo de checklist y borrador")
    st.markdown("**Objetivo:** pre‑armar un checklist de requisitos y un esqueleto de informe para enviar a la aseguradora.")

    with st.form("form_playground"):
        colA, colB = st.columns(2)
        with colA:
            aseguradora = st.text_input("Aseguradora", placeholder="p. ej., SaludPlus")
            acto = st.text_input("Acto médico (trigger)", placeholder="p. ej., cirugía ambulatoria / licencia médica")
            diag = st.text_input("Diagnóstico / motivo principal", placeholder="p. ej., lumbociática aguda")
        with colB:
            fecha = st.date_input("Fecha del acto/reporte")
            profesional = st.text_input("Profesional responsable", placeholder="p. ej., Dr./Dra. ____")
            folio = st.text_input("Folio / N° de caso (opcional)")

        st.markdown("**Evolución / cambios desde el último informe**")
        evolucion = st.text_area("Describa SOLO los cambios y su fecha", height=120,
                                 placeholder="Ej.: 2025-09-12: inicio de fisioterapia; 2025-09-14: dolor disminuye a 3/10…")

        submitted = st.form_submit_button("Generar checklist + borrador")

    if submitted:
        st.subheader("Checklist sugerido")
        st.markdown(  f"""
            - Identificación del caso (folio: **{folio or 's/n'}**), profesional responsable y fecha **{fecha}**  
            - Acto médico que origina el beneficio: **{acto or '—'}**  
            - Diagnóstico/motivo principal: **{diag or '—'}**  
            - Evolución **solo cambios** con fecha (formato *YYYY-MM-DD*):  
              {('- ' + evolucion.replace('\\n', '\\n  - ')) if evolucion.strip() else '  - (pendiente)'}  
            - Adjuntos exigidos por la aseguradora **{aseguradora or '(definir)'}**:  
              - Orden médica / epicrisis  
              - Informe clínico firmado (PDF)  
              - Exámenes de respaldo (si aplica)  
              - Certificados/plantillas propias de la aseguradora  
            - Verificación de **plazos** y **formato** (cumplimiento HIPAA/GDPR)  
            - Revisión humana final (paso 9) y registro de envío
            """)
          

        st.subheader("Borrador de informe (esqueleto)")
        informe = f"""
        INFORME MÉDICO — Activación de beneficio
        Aseguradora: {aseguradora or '—'}    |    Fecha: {fecha}
        Profesional: {profesional or '—'}    |    Folio/Caso: {folio or 's/n'}

        1) Acto médico (trigger)
           - {acto or '—'}

        2) Diagnóstico / motivo principal
           - {diag or '—'}

        3) Evolución (solo cambios fechados)
        {evolucion if evolucion.strip() else '- (pendiente de completar por el profesional)'}

        4) Fundamentos clínicos y respaldo
           - Hallazgos relevantes, exámenes adjuntos, guías aplicadas.

        5) Recomendación / solicitud a la aseguradora
           - Indicar cobertura/beneficio solicitado y duración estimada.

        6) Cumplimiento y privacidad
           - Documento preparado bajo buenas prácticas y normativa HIPAA/GDPR.
        """.strip()
        st.code(informe, language="markdown")

    st.caption("Este playground no reemplaza el juicio clínico ni legal; sirve como apoyo operativo del flujo.")

