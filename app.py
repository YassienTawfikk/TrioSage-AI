"""
TrioSage AI — Multi-Agent Decision Support System
Streamlit UI: Landing screen (API key) + Main screen (scenario input, progress, results)
"""

import streamlit as st
from orchestrator import run_pipeline, validate_inputs, AllAgentsFailedError


# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="TrioSage AI — Multi-Agent Advisor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────
# CSS Injection — all styling lives here
# ──────────────────────────────────────────────

def inject_css():
    """Inject all custom CSS for the app — responsive, premium dark theme."""
    st.markdown("""
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Resets ── */
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(145deg, #0a0a14 0%, #0f0f1a 40%, #141428 100%); }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; max-width: 100% !important; }

    /* ── Landing Card ── */
    .landing-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    .landing-card {
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.8) 0%, rgba(20, 20, 45, 0.9) 100%);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        width: 100%;
        max-width: 480px;
        backdrop-filter: blur(20px);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(124, 58, 237, 0.08);
        animation: fadeInUp 0.6s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ── Logo / Branding ── */
    .app-logo {
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .app-logo .icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 40%, #6d28d9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0.25rem;
        line-height: 1.5;
    }

    /* ── Privacy Note ── */
    .privacy-note {
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        background: rgba(124, 58, 237, 0.08);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: #a78bfa;
        line-height: 1.4;
    }

    /* ── Top Bar ── */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(124, 58, 237, 0.15);
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    .top-bar-title {
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .api-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 20px;
        padding: 0.35rem 0.85rem;
        font-size: 0.78rem;
        color: #4ade80;
    }

    /* ── Progress Tracker ── */
    .progress-tracker {
        background: rgba(30, 30, 60, 0.5);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
    }
    .progress-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    .progress-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
    }
    .progress-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
        transition: all 0.3s ease;
    }
    .dot-waiting { background: #475569; }
    .dot-running {
        background: #7c3aed;
        box-shadow: 0 0 12px rgba(124, 58, 237, 0.6);
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
    }
    .dot-done { background: #22c55e; box-shadow: 0 0 8px rgba(34, 197, 94, 0.4); }
    .dot-failed { background: #ef4444; box-shadow: 0 0 8px rgba(239, 68, 68, 0.4); }
    .progress-label {
        font-size: 0.9rem;
        color: #e2e8f0;
        font-weight: 500;
    }
    .progress-status {
        margin-left: auto;
        font-size: 0.78rem;
        font-weight: 500;
    }
    .status-waiting { color: #64748b; }
    .status-running { color: #a78bfa; }
    .status-done { color: #4ade80; }
    .status-failed { color: #f87171; }

    /* ── Result Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 30, 60, 0.3);
        border-radius: 12px;
        padding: 0.35rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        font-weight: 500;
        font-size: 0.9rem;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(124, 58, 237, 0.2) !important;
        color: #a78bfa !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }

    /* ── Agent Badge ── */
    .agent-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .badge-nvc { background: rgba(244, 114, 182, 0.15); color: #f472b6; border: 1px solid rgba(244, 114, 182, 0.3); }
    .badge-kahneman { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-covey { background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-synthesis { background: rgba(167, 139, 250, 0.15); color: #a78bfa; border: 1px solid rgba(167, 139, 250, 0.3); }

    /* ── Response Card ── */
    .response-card {
        background: rgba(30, 30, 60, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        line-height: 1.7;
        color: #cbd5e1;
    }
    .response-card h2, .response-card h3 {
        color: #e2e8f0;
        margin-top: 1rem;
    }
    .response-card strong { color: #e2e8f0; }
    .response-unavailable {
        text-align: center;
        padding: 2rem;
        color: #f87171;
        background: rgba(239, 68, 68, 0.05);
        border: 1px dashed rgba(239, 68, 68, 0.2);
        border-radius: 12px;
    }

    /* ── Error Box ── */
    .error-box {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #fca5a5;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    /* ── Streamlit overrides ── */
    .stTextArea textarea {
        background: rgba(30, 30, 60, 0.5) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(124, 58, 237, 0.5) !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.1) !important;
    }
    .stTextInput input {
        background: rgba(30, 30, 60, 0.5) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
    }
    .stTextInput input:focus {
        border-color: rgba(124, 58, 237, 0.5) !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.1) !important;
    }

    /* Primary button */
    .stButton > button[kind="primary"],
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
    }

    /* Secondary / ghost button */
    .ghost-btn > button {
        background: transparent !important;
        color: #a78bfa !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        box-shadow: none !important;
    }
    .ghost-btn > button:hover {
        background: rgba(124, 58, 237, 0.1) !important;
        box-shadow: none !important;
    }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        .landing-card { padding: 2rem 1.5rem; margin: 1rem; }
        .app-title { font-size: 1.6rem; }
        .top-bar { flex-direction: column; align-items: flex-start; }
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
    }
    @media (max-width: 480px) {
        .landing-card { padding: 1.5rem 1.25rem; border-radius: 16px; }
        .app-title { font-size: 1.4rem; }
        .app-logo .icon { font-size: 2.5rem; }
        .progress-tracker { padding: 1rem; }
        .response-card { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────

def init_session_state():
    """Initialize all session state keys with defaults."""
    defaults = {
        "api_key": "",
        "screen": "landing",       # "landing" or "main"
        "results": None,           # dict from run_pipeline
        "is_running": False,       # True while pipeline is executing
        "agent_status": {},        # {agent_name: "waiting"|"running"|"done"|"failed"}
        "error_message": "",       # Inline error message
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ──────────────────────────────────────────────
# Screen 1 — Landing
# ──────────────────────────────────────────────

def render_landing():
    """Render the API key entry landing screen."""
    st.markdown("""
    <div class="landing-container">
        <div class="landing-card">
            <div class="app-logo">
                <span class="icon">🔮</span>
                <h1 class="app-title">TrioSage AI</h1>
                <p class="app-subtitle">
                    Three wise advisors. Three different worldviews.<br>
                    One unified recommendation.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered columns for the input (adaptive width)
    _, col_center, _ = st.columns([1, 2, 1])
    with col_center:
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Paste your Gemini API key here",
            label_visibility="collapsed",
            key="api_key_input",
        )

        st.markdown("""
        <div class="privacy-note">
            <span>🔒</span>
            <span>Your API key stays in session memory only — never stored, logged, or sent anywhere except to Google's Gemini API.</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Continue →", use_container_width=True, key="continue_btn"):
            if api_key_input and api_key_input.strip():
                st.session_state.api_key = api_key_input.strip()
                st.session_state.screen = "main"
                st.rerun()
            else:
                st.markdown("""
                <div class="error-box">
                    <span>⚠️</span>
                    <span>Please enter your Gemini API key to continue.</span>
                </div>
                """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Progress Tracker Component
# ──────────────────────────────────────────────

def render_progress_tracker(agent_status: dict):
    """Render the live progress tracker with colored dots."""
    agents_info = [
        ("nvc", "NVC — Nonviolent Communication"),
        ("kahneman", "Kahneman — Fast & Slow Thinking"),
        ("covey", "Covey — 7 Habits of Effectiveness"),
        ("synthesizer", "Synthesizer — Unified Recommendation"),
    ]

    rows_html = ""
    for name, label in agents_info:
        status = agent_status.get(name, "waiting")
        dot_class = f"dot-{status}"
        status_class = f"status-{status}"
        status_text = status.capitalize()

        rows_html += f"""
        <div class="progress-row">
            <div class="progress-dot {dot_class}"></div>
            <span class="progress-label">{label}</span>
            <span class="progress-status {status_class}">{status_text}</span>
        </div>
        """

    st.markdown(f"""
    <div class="progress-tracker">
        <div class="progress-title">Pipeline Progress</div>
        {rows_html}
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Results Tabs Component
# ──────────────────────────────────────────────

def render_results(results: dict):
    """Render the tabbed results view with agent badges and formatted responses."""
    tab_nvc, tab_kahneman, tab_covey, tab_synthesis = st.tabs([
        "🌱 NVC", "🧠 Kahneman", "🎯 Covey", "🔮 Synthesis"
    ])

    tab_config = [
        (tab_nvc, "nvc", "NVC — Nonviolent Communication", "Empathy-first • Observe → Feel → Need → Request", "badge-nvc"),
        (tab_kahneman, "kahneman", "Kahneman — Thinking, Fast & Slow", "Cognitive bias detection • System 1 vs System 2", "badge-kahneman"),
        (tab_covey, "covey", "Covey — The 7 Habits", "Strategic effectiveness • Proactive & principle-centered", "badge-covey"),
        (tab_synthesis, "synthesis", "Unified Synthesis", "Integrated recommendation from all advisors", "badge-synthesis"),
    ]

    for tab, key, title, lens, badge_class in tab_config:
        with tab:
            st.markdown(f'<div class="agent-badge {badge_class}">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #64748b; font-size: 0.85rem; margin-bottom: 1rem;">{lens}</p>', unsafe_allow_html=True)

            response = results.get(key)
            if response:
                st.markdown(f'<div class="response-card">', unsafe_allow_html=True)
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="response-unavailable">
                    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">⚠️</p>
                    <p><strong>Response unavailable</strong></p>
                    <p style="font-size: 0.85rem; color: #94a3b8;">This advisor encountered an error and could not provide analysis.</p>
                </div>
                """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Screen 2 — Main
# ──────────────────────────────────────────────

def render_main():
    """Render the main application screen with scenario input, progress, and results."""

    # Top bar
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown('<span class="top-bar-title">🔮 TrioSage AI</span>', unsafe_allow_html=True)
    with col_badge:
        masked_key = st.session_state.api_key[:4] + "•" * 8
        col_b, col_x = st.columns([3, 1])
        with col_b:
            st.markdown(f'<div class="api-badge">🔑 {masked_key}</div>', unsafe_allow_html=True)
        with col_x:
            if st.button("✕", key="clear_key_btn", help="Clear API key and return to landing"):
                st.session_state.api_key = ""
                st.session_state.screen = "landing"
                st.session_state.results = None
                st.session_state.agent_status = {}
                st.session_state.error_message = ""
                st.rerun()

    st.markdown('<div style="border-bottom: 1px solid rgba(124,58,237,0.15); margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

    # Scenario input
    scenario = st.text_area(
        "Describe your scenario",
        placeholder="Describe any real-life situation, conflict, or decision you're facing. The more detail you provide, the richer the advice will be...",
        height=150,
        label_visibility="collapsed",
        key="scenario_input",
    )

    # Analyze button (right-aligned)
    _, col_btn = st.columns([3, 1])
    with col_btn:
        analyze_clicked = st.button("✨ Analyze", use_container_width=True, key="analyze_btn")

    # Error message display
    if st.session_state.error_message:
        st.markdown(f"""
        <div class="error-box">
            <span>⚠️</span>
            <span>{st.session_state.error_message}</span>
        </div>
        """, unsafe_allow_html=True)

    # Handle analyze click
    if analyze_clicked:
        st.session_state.error_message = ""
        is_valid, error_msg = validate_inputs(scenario, st.session_state.api_key)

        if not is_valid:
            st.session_state.error_message = error_msg
            st.rerun()
        else:
            # Reset previous results
            st.session_state.results = None
            st.session_state.agent_status = {
                "nvc": "waiting",
                "kahneman": "waiting",
                "covey": "waiting",
                "synthesizer": "waiting",
            }
            st.session_state.is_running = True
            st.session_state.error_message = ""

            # Show progress tracker placeholder
            progress_placeholder = st.empty()

            def update_progress(agent_name: str, status: str):
                """Callback to update progress tracker in real-time."""
                st.session_state.agent_status[agent_name] = status
                with progress_placeholder:
                    render_progress_tracker(st.session_state.agent_status)

            # Render initial progress state
            with progress_placeholder:
                render_progress_tracker(st.session_state.agent_status)

            # Run the pipeline
            try:
                results = run_pipeline(
                    scenario=scenario,
                    api_key=st.session_state.api_key,
                    progress_callback=update_progress,
                )
                st.session_state.results = results
                st.session_state.is_running = False
            except AllAgentsFailedError as e:
                st.session_state.is_running = False
                st.session_state.error_message = str(e)
                st.rerun()

    # Show progress tracker if running (persistent state)
    if st.session_state.is_running and not analyze_clicked:
        render_progress_tracker(st.session_state.agent_status)

    # Show results if available
    if st.session_state.results:
        # Final progress tracker
        render_progress_tracker(st.session_state.agent_status)

        st.markdown("<br>", unsafe_allow_html=True)

        # Results tabs
        render_results(st.session_state.results)

        # "Try another scenario" button
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_reset = st.columns([3, 1])
        with col_reset:
            st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
            if st.button("🔄 Try another scenario", use_container_width=True, key="reset_btn"):
                st.session_state.results = None
                st.session_state.agent_status = {}
                st.session_state.error_message = ""
                st.session_state.is_running = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Main Entry Point
# ──────────────────────────────────────────────

def main():
    """Main app entry point — route to the appropriate screen."""
    inject_css()
    init_session_state()

    if st.session_state.screen == "landing":
        render_landing()
    else:
        render_main()


if __name__ == "__main__":
    main()
