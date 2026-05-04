"""
TrioSage AI — Multi-Agent Decision Support System
Streamlit frontend — editorial magazine aesthetic.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from orchestrator import run_pipeline, validate_inputs, AllAgentsFailedError

# ─── Page Config ─────────────────────────────

st.set_page_config(
    page_title="TrioSage AI",
    page_icon="△",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── FontAwesome ─────────────────────────────

st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">',
    unsafe_allow_html=True,
)

# ─── CSS ─────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Global ── */
*, html, body, [class*="st-"] { font-family: 'Inter', -apple-system, sans-serif !important; }
.stApp { background: #FFFFFF !important; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { max-width: 660px !important; padding-top: 2rem !important; }
h1, h2, h3, h4, h5, h6 { font-weight: 500 !important; color: #1A1A1A !important; }
p, li, span { color: #1A1A1A; line-height: 1.7; }
[data-testid="InputInstructions"] { display: none !important; }

/* ── Text Input ── */
.stTextInput > div > div { background: transparent !important; }
.stTextInput input {
    background: #F8F7F4 !important;
    border: 1px solid #E8E6E0 !important;
    border-radius: 8px !important;
    color: #1A1A1A !important;
    padding: 0.65rem 0.85rem !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus { border-color: #2D6A4F !important; box-shadow: none !important; }

/* ── Text Area ── */
.stTextArea textarea {
    background: #F8F7F4 !important;
    border: 1px solid #E8E6E0 !important;
    border-radius: 10px !important;
    color: #1A1A1A !important;
    font-size: 0.9rem !important;
    padding: 0.9rem 1rem !important;
    line-height: 1.7 !important;
}
.stTextArea textarea:focus { border-color: #2D6A4F !important; box-shadow: none !important; }
.stTextArea label, .stTextInput label {
    font-weight: 400 !important; color: #6B6860 !important; font-size: 0.8rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #2D6A4F !important;
    color: #FFF !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.4rem !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    box-shadow: none !important;
    white-space: nowrap !important;
    transition: background 0.15s ease !important;
}
.stButton > button * {
    color: #FFF !important;
}
.stButton > button div {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
}
.stButton > button p {
    margin: 0 !important;
    text-align: center !important;
    display: inline-block !important;
}
.stButton > button:hover { background: #245A42 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: transparent !important; border-bottom: 1px solid #E8E6E0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important; padding: 0.5rem 0.9rem !important;
    font-weight: 400 !important; font-size: 0.82rem !important;
    color: #6B6860 !important; border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] { color: #2D6A4F !important; border-bottom-color: #2D6A4F !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem !important; animation: fadeTab 0.2s ease; }
@keyframes fadeTab { from{opacity:0} to{opacity:1} }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #FAFAF8 !important; border-right: 1px solid #E8E6E0 !important; }

/* ── Progress ── */
.tracker { padding: 0.4rem 0 0.4rem 1.1rem; position: relative; }
.tracker::before {
    content:''; position:absolute; left:0.4rem; top:0.6rem; bottom:0.6rem;
    width:1px; background:#E8E6E0;
}
.tr { display:flex; align-items:center; gap:0.55rem; padding:0.3rem 0; position:relative; }
.ti { width:0.9rem; text-align:center; font-size:0.65rem; z-index:1; background:#FFF; padding:1px 0; }
.tw{color:#D5D3CD} .ta{color:#2D6A4F;animation:blink 1.2s ease-in-out infinite}
.td{color:#2D6A4F} .tf{color:#C0392B}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.tl { font-size:0.82rem; color:#1A1A1A; }
.ts { margin-left:auto; font-size:0.75rem; font-weight:500; }
.sw{color:#D5D3CD} .sa{color:#2D6A4F} .sd{color:#2D6A4F} .sf{color:#C0392B}

/* ── Utility ── */
.sep { border:none; border-top:1px solid #E8E6E0; margin:1rem 0; }
.muted { color:#6B6860; font-size:0.78rem; line-height:1.5; }
.err-box {
    background:#FDF6F5; border:1px solid #E8D5D0; border-radius:8px;
    padding:0.55rem 0.9rem; color:#C0392B; font-size:0.82rem; margin-top:0.5rem;
}
.unavail {
    text-align:center; padding:1.5rem; color:#C0392B;
    border:1px dashed #E8D5D0; border-radius:10px; font-size:0.82rem; background:#FDF6F5;
}

@media(max-width:640px){ .block-container{padding-left:1rem!important;padding-right:1rem!important;} }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────

for _k, _v in {
    "api_key": "", "screen": "landing", "results": None,
    "is_running": False, "agent_status": {}, "error_message": "",
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─── Agent Config ────────────────────────────

_AGENTS = [
    ("nvc",         "Nonviolent Communication", "fa-heart"),
    ("kahneman",    "Thinking, Fast & Slow",    "fa-brain"),
    ("covey",       "The 7 Habits",             "fa-compass"),
    ("synthesizer", "Synthesis",                "fa-layer-group"),
]

_STATUS = {
    "waiting": ("fa-regular fa-circle",          "tw", "sw", ""),
    "running": ("fa-solid fa-circle-half-stroke", "ta", "sa", "Thinking…"),
    "done":    ("fa-solid fa-circle-check",       "td", "sd", "Done"),
    "failed":  ("fa-solid fa-circle-xmark",       "tf", "sf", "Failed"),
}

_TAB_CFG = [
    ("nvc",       "Nonviolent Communication — Rosenberg", "fa-heart",      "#C0392B"),
    ("kahneman",  "Thinking, Fast & Slow — Kahneman",     "fa-brain",      "#2D6A4F"),
    ("covey",     "The 7 Habits — Covey",                 "fa-compass",    "#B8860B"),
    ("synthesis", "Unified Synthesis",                     "fa-layer-group","#6B6860"),
]

# ─── Helpers ─────────────────────────────────

def _tracker_html(status: dict) -> str:
    rows = ""
    for name, label, _ in _AGENTS:
        s = status.get(name, "waiting")
        fa, tc, sc, txt = _STATUS.get(s, _STATUS["waiting"])
        rows += (
            f'<div class="tr">'
            f'<span class="ti {tc}"><i class="{fa}"></i></span>'
            f'<span class="tl">{label}</span>'
            f'<span class="ts {sc}">{txt}</span>'
            f'</div>'
        )
    return f'<div class="tracker">{rows}</div>'


# ─── Landing ─────────────────────────────────

def _landing():
    st.markdown("<div style='height:10vh'></div>", unsafe_allow_html=True)

    _, cc, _ = st.columns([1, 3, 1])
    with cc:
        # Title
        st.markdown("""
        <div style="text-align:center;margin-bottom:1.5rem;">
            <h2 style="margin:0 0 0.2rem 0;font-size:1.5rem;">TrioSage AI</h2>
            <p class="muted" style="font-size:0.88rem;">
                Three perspectives on your situation.<br>One unified recommendation.
            </p>
        </div>
        <hr class="sep">
        """, unsafe_allow_html=True)

        # API key label
        st.markdown(
            '<p style="color:#6B6860;font-size:0.82rem;margin-bottom:0.2rem;">'
            '<i class="fa-solid fa-key" style="color:#2D6A4F;margin-right:0.25rem;font-size:0.7rem;"></i>'
            'Your Gemini API key <span style="font-size:0.75rem;">(<a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#2D6A4F;text-decoration:underline;">Get one here</a>)</span></p>',
            unsafe_allow_html=True,
        )

        # Full-width input
        key_input = st.text_input(
            "key", type="password", value="",
            placeholder="Paste your key here (⌘V)",
            label_visibility="collapsed", key="key_in",
        )

        # Paste button (JS clipboard) — below input, small and subtle
        st.html(
            '''
            <div style="display:flex;align-items:center;gap:10px;margin-top:2px;font-family:'Inter',sans-serif;">
                <button id="custom-paste-btn" style="
                    background:transparent; border:1px solid #E8E6E0; border-radius:5px;
                    padding:4px 12px; cursor:pointer; font-size:12px; color:#6B6860;
                    display:inline-flex; align-items:center; gap:5px;
                    font-family:'Inter',sans-serif;
                " onmouseover="this.style.background='#F8F7F4'" onmouseout="this.style.background='transparent'">
                    <i class="fa-regular fa-clipboard"></i> Paste from clipboard
                </button>
                <span style="color:#B0ADA6;font-size:11px;">
                    <i class="fa-solid fa-lock" style="font-size:9px;margin-right:3px;"></i>
                    Session only — never stored
                </span>
            </div>
            <script>
            setTimeout(() => {
                const btn = window.parent.document.getElementById("custom-paste-btn") || document.getElementById("custom-paste-btn");
                if (btn && !btn.hasAttribute("data-listener-attached")) {
                    btn.setAttribute("data-listener-attached", "true");
                    btn.addEventListener("click", async function() {
                        try {
                            const text = await navigator.clipboard.readText();
                            let target = document.querySelector('input[type="password"]');
                            if (!target && window.parent) target = window.parent.document.querySelector('input[type="password"]');
                            if (target) {
                                target.focus();
                                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                                nativeSetter.call(target, text);
                                target.dispatchEvent(new Event('input', { bubbles: true }));
                                target.dispatchEvent(new Event('change', { bubbles: true }));
                            } else {
                                alert('Could not find the input box.');
                            }
                        } catch(e) {
                            alert('Browser blocked clipboard access. Please paste manually with ⌘V.');
                        }
                    });
                }
            }, 100);
            </script>
            ''',
            unsafe_allow_javascript=True
        )

        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        # Continue
        if st.button("Continue  →", use_container_width=True, key="btn_continue"):
            if key_input and key_input.strip():
                st.session_state.api_key = key_input.strip()
                st.session_state.screen = "main"
                st.rerun()
            else:
                st.markdown(
                    '<div class="err-box">Please enter your Gemini API key.</div>',
                    unsafe_allow_html=True,
                )


# ─── Main ────────────────────────────────────

def _main():
    # Top bar
    c1, c2 = st.columns([4, 2])
    with c1:
        st.markdown(
            '<p style="font-size:1.1rem;font-weight:500;color:#1A1A1A;margin:0;">TrioSage AI</p>',
            unsafe_allow_html=True,
        )
    with c2:
        masked = st.session_state.api_key[:5] + "····"
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:flex-end;gap:0.5rem;margin-top:0.1rem;">'
            f'<span class="muted"><i class="fa-solid fa-key" style="color:#2D6A4F;margin-right:3px;font-size:0.6rem;"></i>{masked}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Separator + clear button right-aligned
    cl, cr = st.columns([6, 1], vertical_alignment="bottom")
    with cl:
        st.markdown('<hr class="sep" style="margin-top:0.3rem;">', unsafe_allow_html=True)
    with cr:
        if st.button("✕ Clear", key="btn_clear", use_container_width=True):
            st.session_state.api_key = ""
            st.session_state.screen = "landing"
            st.session_state.results = None
            st.session_state.agent_status = {}
            st.session_state.error_message = ""
            st.session_state.is_running = False
            st.rerun()

    # Scenario input
    scenario = st.text_area(
        "Describe your situation",
        placeholder="What's on your mind? Describe any conflict, decision, or situation you're facing…",
        height=180, key="scenario_in",
    )

    # Analyze button — right aligned
    _, _btn = st.columns([3.5, 1.5])
    with _btn:
        clicked = st.button("Analyze  →", use_container_width=True, key="btn_go", disabled=st.session_state.is_running)

    # Error
    if st.session_state.error_message:
        st.markdown(
            f'<div class="err-box">{st.session_state.error_message}</div>',
            unsafe_allow_html=True,
        )

    # Run pipeline
    if clicked:
        st.session_state.error_message = ""
        ok, err = validate_inputs(scenario, st.session_state.api_key)
        if not ok:
            st.session_state.error_message = err
            st.rerun()
        else:
            st.session_state.results = None
            st.session_state.agent_status = {n: "waiting" for n, _, _ in _AGENTS}
            st.session_state.is_running = True

            holder = st.empty()

            def _cb(name, status):
                st.session_state.agent_status[name] = status
                holder.markdown(_tracker_html(st.session_state.agent_status), unsafe_allow_html=True)

            holder.markdown(_tracker_html(st.session_state.agent_status), unsafe_allow_html=True)

            try:
                res = run_pipeline(scenario, st.session_state.api_key, progress_callback=_cb)
                st.session_state.results = res
                st.session_state.is_running = False
            except AllAgentsFailedError as e:
                st.session_state.is_running = False
                st.session_state.error_message = str(e)
                st.rerun()

    # Sidebar progress after completion
    if st.session_state.agent_status and st.session_state.results:
        with st.sidebar:
            st.markdown("#### Pipeline progress")
            st.markdown(_tracker_html(st.session_state.agent_status), unsafe_allow_html=True)

    # Results
    if st.session_state.results:
        st.markdown('<hr class="sep">', unsafe_allow_html=True)
        _render_results(st.session_state.results)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        _, _b = st.columns([3.5, 1.5])
        with _b:
            if st.button("Try another →", use_container_width=True, key="btn_reset"):
                st.session_state.results = None
                st.session_state.agent_status = {}
                st.session_state.error_message = ""
                st.session_state.is_running = False
                st.rerun()


# ─── Results ─────────────────────────────────

def _render_results(results: dict):
    tabs = st.tabs(["♡ NVC", "◎ Kahneman", "⊕ Covey", "◈ Synthesis"])

    for tab, (key, title, icon, color) in zip(tabs, _TAB_CFG):
        with tab:
            st.markdown(
                f'<p style="color:#6B6860;font-size:0.8rem;margin-bottom:0.4rem;">'
                f'<i class="fa-solid {icon}" style="color:{color};margin-right:0.25rem;"></i>{title}</p>',
                unsafe_allow_html=True,
            )
            resp = results.get(key)
            if resp:
                st.markdown(resp)
            else:
                st.markdown(
                    '<div class="unavail">'
                    '<i class="fa-solid fa-circle-xmark" style="margin-right:0.25rem;"></i>'
                    'Response unavailable — this advisor encountered an error.</div>',
                    unsafe_allow_html=True,
                )


# ─── Entry ───────────────────────────────────

if st.session_state.screen == "landing":
    _landing()
else:
    _main()
