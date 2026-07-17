"""
frontend/components/pipeline.py
Pipeline progress visualization for LexAI.
"""

import streamlit as st

STAGE_KEYS = [
    "extract",
    "retrieve",
    "augment",
    "generate",
    "finalise",
]

STAGES = [
    {"key": "extract",  "icon": "📄", "label": "Extract",  "desc": "Reading document text"},
    {"key": "retrieve", "icon": "🔍", "label": "Retrieve",  "desc": "Fetching legal knowledge"},
    {"key": "augment",  "icon": "🧠", "label": "Augment",   "desc": "Building RAG prompt"},
    {"key": "generate", "icon": "⚡", "label": "Generate",  "desc": "GPT-4o-mini analysis"},
    {"key": "finalise", "icon": "✅", "label": "Finalise",  "desc": "Structuring output"},
]


def render_pipeline(active_stage: str = None, completed: list = None):
    """
    Render the 5-stage pipeline progress bar.
    active_stage: key of the currently running stage
    completed: list of keys of completed stages
    """
    completed = completed or []

    cols = st.columns(len(STAGES))

    for i, stage in enumerate(STAGES):
        with cols[i]:
            is_done   = stage["key"] in completed
            is_active = stage["key"] == active_stage

            if is_done:
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        padding: 0.5rem;
                        border: 2px solid #00c851;
                        border-radius: 8px;
                        color: #00c851;
                    ">
                        <div style="font-size: 1.5rem;">✅</div>
                        <div style="font-size: 0.75rem; font-weight: 600;">
                            {stage['label']}
                        </div>
                        <div style="font-size: 0.65rem; color: #aaa;">
                            {stage['desc']}
                        </div>
                        <div style="
                            background: #00c851;
                            color: black;
                            font-size: 0.6rem;
                            padding: 1px 6px;
                            border-radius: 10px;
                            margin-top: 4px;
                            font-weight: 700;
                        ">COMPLETED</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif is_active:
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        padding: 0.5rem;
                        border: 2px solid #00d4ff;
                        border-radius: 8px;
                        color: #00d4ff;
                    ">
                        <div style="font-size: 1.5rem;">{stage['icon']}</div>
                        <div style="font-size: 0.75rem; font-weight: 600;">
                            {stage['label']}
                        </div>
                        <div style="font-size: 0.65rem; color: #aaa;">
                            {stage['desc']}
                        </div>
                        <div style="
                            background: #00d4ff;
                            color: black;
                            font-size: 0.6rem;
                            padding: 1px 6px;
                            border-radius: 10px;
                            margin-top: 4px;
                            font-weight: 700;
                        ">ACTIVE</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        padding: 0.5rem;
                        border: 2px solid #444;
                        border-radius: 8px;
                        color: #444;
                    ">
                        <div style="font-size: 1.5rem;">{stage['icon']}</div>
                        <div style="font-size: 0.75rem; font-weight: 600;">
                            {stage['label']}
                        </div>
                        <div style="font-size: 0.65rem; color: #aaa;">
                            {stage['desc']}
                        </div>
                        <div style="
                            background: #444;
                            color: #aaa;
                            font-size: 0.6rem;
                            padding: 1px 6px;
                            border-radius: 10px;
                            margin-top: 4px;
                            font-weight: 700;
                        ">PENDING</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )