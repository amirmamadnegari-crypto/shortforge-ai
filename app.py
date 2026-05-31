"""
ShortForge AI - Main Streamlit Application
Production-ready YouTube Shorts viral content engine.
"""

import streamlit as st
import json
import logging
from typing import Optional

from config import config, ShortForgeConfig
from agents import IdeaAgent, HookAgent, ScriptAgent, ThumbnailAgent, SEOAgent, GrowthAgent
from utils import score_to_color, score_to_grade, validate_topic, safe_get, truncate_text

logger = logging.getLogger("ShortForgeAI.App")

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShortForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Bebas+Neue&display=swap');

/* ── Root Variables ── */
:root {
    --red: #FF0033;
    --gold: #FFD700;
    --green: #00FF88;
    --bg: #0A0A0A;
    --surface: #141414;
    --surface2: #1E1E1E;
    --border: #2A2A2A;
    --text: #F0F0F0;
    --muted: #888888;
}

/* ── Base ── */
.stApp { background: var(--bg); color: var(--text); font-family: 'Space Grotesk', sans-serif; }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #0A0A0A 0%, #1a0000 50%, #0A0A0A 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--red);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,0,51,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #FF0033, #FF6B35, #FFD700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1;
}
.hero p { color: var(--muted); font-size: 1.05rem; margin: 0.5rem 0 0; }
.hero .badge {
    display: inline-block;
    background: var(--red);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── Football Mode Banner ── */
.football-banner {
    background: linear-gradient(135deg, #006600, #003300);
    border: 1px solid #00AA00;
    border-left: 4px solid #00FF00;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.football-banner h3 { margin: 0; color: #00FF00; font-size: 1.1rem; }
.football-banner p { margin: 0.2rem 0 0; color: #88CC88; font-size: 0.85rem; }

/* ── Score Badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    font-weight: 700;
    font-size: 1rem;
    border: 2px solid;
    flex-shrink: 0;
}

/* ── Idea Card ── */
.idea-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
    position: relative;
}
.idea-card:hover { border-color: var(--red); }
.idea-card .rank {
    position: absolute;
    top: -8px;
    left: 12px;
    background: var(--red);
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    letter-spacing: 1px;
}
.idea-card h4 { margin: 0.5rem 0 0.25rem; font-size: 1rem; color: var(--text); }
.idea-card .reason { color: var(--muted); font-size: 0.85rem; line-height: 1.5; margin: 0; }
.idea-card .tags { margin-top: 0.75rem; display: flex; gap: 0.4rem; flex-wrap: wrap; }
.tag {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 20px;
}
.tag.emotion { border-color: #FF6B35; color: #FF6B35; }
.tag.potential { border-color: var(--gold); color: var(--gold); }
.tag.time { border-color: #888; }

/* ── Hook Card ── */
.hook-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--red);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
}
.hook-card .hook-text { font-size: 1.05rem; color: var(--text); font-weight: 500; margin: 0; }
.hook-card .hook-meta { color: var(--muted); font-size: 0.8rem; margin: 0.4rem 0 0; }
.hook-card .delivery-tip {
    background: var(--surface2);
    border-radius: 5px;
    padding: 0.4rem 0.75rem;
    font-size: 0.8rem;
    color: #aaa;
    margin-top: 0.5rem;
}

/* ── Script Sections ── */
.script-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}
.script-section .section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 0.75rem;
}
.label-hook { background: rgba(255,0,51,0.2); color: var(--red); border: 1px solid var(--red); }
.label-story { background: rgba(255,215,0,0.15); color: var(--gold); border: 1px solid var(--gold); }
.label-loop { background: rgba(0,255,136,0.15); color: var(--green); border: 1px solid var(--green); }
.label-cta { background: rgba(100,100,255,0.2); color: #8888FF; border: 1px solid #8888FF; }
.script-text { color: var(--text); line-height: 1.8; font-size: 0.95rem; white-space: pre-wrap; }
.visual-cue {
    background: var(--surface2);
    border-left: 2px solid #555;
    padding: 0.4rem 0.75rem;
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: #888;
    border-radius: 0 5px 5px 0;
}

/* ── Thumbnail Color Swatch ── */
.color-swatch {
    display: inline-block;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    border: 2px solid var(--border);
    vertical-align: middle;
    margin-right: 6px;
}

/* ── Score Radar ── */
.score-dimension {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
}
.score-dimension:last-child { border-bottom: none; }
.dim-label { width: 160px; font-size: 0.85rem; color: var(--muted); flex-shrink: 0; }
.dim-bar-container { flex: 1; background: var(--surface2); border-radius: 4px; height: 8px; overflow: hidden; }
.dim-bar { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
.dim-score { width: 40px; text-align: right; font-weight: 700; font-size: 0.9rem; flex-shrink: 0; }

/* ── Calendar ── */
.cal-week-header {
    background: linear-gradient(90deg, var(--red), #AA0022);
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 8px 8px 0 0;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.cal-day {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: none;
    padding: 0.75rem 1.2rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.cal-day:last-child { border-radius: 0 0 8px 8px; }
.cal-day-num { color: var(--red); font-weight: 700; font-size: 0.85rem; width: 55px; flex-shrink: 0; }
.cal-day-content h5 { margin: 0 0 0.2rem; font-size: 0.9rem; }
.cal-day-content p { margin: 0; color: var(--muted); font-size: 0.8rem; }

/* ── General Metric Card ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    text-align: center;
}
.metric-card .metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    line-height: 1;
    margin: 0.25rem 0;
}
.metric-card .metric-label { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.5px !important;
    border-radius: 8px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Space Grotesk', sans-serif !important; }
.stTabs [aria-selected="true"] { color: var(--red) !important; border-bottom-color: var(--red) !important; }
.stExpander { border-color: var(--border) !important; background: var(--surface) !important; border-radius: 8px !important; }
div[data-testid="stVerticalBlock"] { gap: 0; }
.stMarkdown h2 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; color: var(--text); }
.stMarkdown h3 { font-size: 1.1rem; color: var(--text); }
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE INIT ───────────────────────────────────────────────────────
def init_session():
    defaults = {
        "ideas_result": None,
        "hooks_result": None,
        "script_result": None,
        "thumbnail_result": None,
        "seo_result": None,
        "viral_score_result": None,
        "calendar_result": None,
        "growth_result": None,
        "football_mode": False,
        "current_topic": "",
        "selected_hook": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ─── COMPONENT HELPERS ────────────────────────────────────────────────────────

def render_score_badge(score: int, size: int = 52) -> str:
    color = score_to_color(score)
    return f"""<div class="score-badge" style="color:{color};border-color:{color};width:{size}px;height:{size}px;font-size:{size*0.22}rem">{score}</div>"""


def render_idea_card(idea: dict) -> None:
    rank = idea.get("rank", "")
    title = idea.get("title", "")
    score = idea.get("viral_score", 0)
    reason = idea.get("viral_reason", "")
    emotion = idea.get("target_emotion", "")
    potential = idea.get("view_potential", "")
    post_time = idea.get("best_posting_time", "")
    color = score_to_color(score)

    st.markdown(f"""
    <div class="idea-card">
        <div class="rank">#{rank}</div>
        <div style="display:flex;align-items:center;gap:1rem;margin-top:0.25rem">
            {render_score_badge(score)}
            <div>
                <h4>{title}</h4>
                <p class="reason">{reason}</p>
            </div>
        </div>
        <div class="tags">
            <span class="tag emotion">😤 {emotion}</span>
            <span class="tag potential">📈 {potential}</span>
            <span class="tag time">🕐 {post_time}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hook_card(hook: dict, is_best: bool = False) -> None:
    text = hook.get("hook_text", "")
    hook_type = hook.get("hook_type", "")
    trigger = hook.get("psychological_trigger", "")
    score = hook.get("retention_score", 0)
    tip = hook.get("delivery_tip", "")
    color = score_to_color(score)
    star = "⭐ " if is_best else ""

    st.markdown(f"""
    <div class="hook-card" style="border-left-color:{color}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <p class="hook-text">{star}"{text}"</p>
            {render_score_badge(score, 40)}
        </div>
        <div class="hook-meta">🎯 {hook_type} &nbsp;|&nbsp; 🧠 {trigger}</div>
        {"<div class='delivery-tip'>💡 " + tip + "</div>" if tip else ""}
    </div>
    """, unsafe_allow_html=True)


def render_viral_score(result: dict) -> None:
    if result.get("error"):
        st.error(result.get("message", "Error scoring content"))
        return

    overall = result.get("overall_viral_score", 0)
    grade = result.get("grade", "?")
    dims = result.get("dimensions", {})
    color = score_to_color(overall)
    prediction = result.get("predicted_performance", {})

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Viral Score</div>
            <div class="metric-value" style="color:{color}">{overall}</div>
            <div style="color:{color};font-weight:700">Grade {grade}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Est. Views</div>
            <div class="metric-value" style="color:var(--gold);font-size:1.4rem">{prediction.get('views_range','N/A')}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Engagement</div>
            <div class="metric-value" style="color:var(--green);font-size:1.6rem">{prediction.get('engagement_rate','N/A')}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        virality = prediction.get('virality_probability', 'N/A')
        v_color = "#00FF88" if virality == "High" else "#FFD700" if virality == "Medium" else "#FF4444"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Virality</div>
            <div class="metric-value" style="color:{v_color};font-size:1.6rem">{virality}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    dim_labels = {
        "curiosity": "🔍 Curiosity",
        "emotion": "❤️ Emotion",
        "shareability": "🔁 Shareability",
        "retention_potential": "📺 Retention",
        "trend_alignment": "📈 Trend Alignment",
    }

    st.markdown("<div>", unsafe_allow_html=True)
    for dim_key, label in dim_labels.items():
        dim = dims.get(dim_key, {})
        score = dim.get("score", 0)
        reason = dim.get("reason", "")
        improvement = dim.get("improvement", "")
        bar_color = score_to_color(score)
        st.markdown(f"""
        <div class="score-dimension">
            <div class="dim-label">{label}</div>
            <div class="dim-bar-container">
                <div class="dim-bar" style="width:{score}%;background:{bar_color}"></div>
            </div>
            <div class="dim-score" style="color:{bar_color}">{score}</div>
        </div>
        """, unsafe_allow_html=True)
        if improvement:
            with st.expander(f"💡 Improve {label.split(' ')[-1]}"):
                st.write(f"**Why:** {reason}")
                st.write(f"**How to improve:** {improvement}")

    st.markdown("</div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        strengths = result.get("strengths", [])
        if strengths:
            st.markdown("**✅ Strengths**")
            for s in strengths:
                st.markdown(f"- {s}")
    with col_r:
        wins = result.get("quick_wins", [])
        if wins:
            st.markdown("**⚡ Quick Wins**")
            for w in wins:
                st.markdown(f"- {w}")


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1rem 0 0.5rem">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;
                        background:linear-gradient(90deg,#FF0033,#FFD700);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        letter-spacing:3px">ShortForge</div>
            <div style="color:#555;font-size:0.7rem;letter-spacing:2px;text-transform:uppercase">Content Engine v1.0</div>
        </div>
        <hr style="border-color:#2A2A2A;margin:0.75rem 0">
        """, unsafe_allow_html=True)

        st.markdown("### ⚙️ Settings")

        topic = st.text_input(
            "Topic / Keyword",
            placeholder="e.g. Cristiano Ronaldo, AI tools, Space...",
            help="The niche or keyword for your YouTube Shorts",
        )

        football_mode = st.toggle(
            "⚽ Football Creator Mode",
            value=st.session_state.football_mode,
            help="Enable football-specific content generation",
        )
        st.session_state.football_mode = football_mode

        st.markdown("<hr style='border-color:#2A2A2A'>", unsafe_allow_html=True)

        st.markdown("### 🎛️ Advanced Options")
        hook_style = st.selectbox("Hook Style", HookAgent.available_styles())
        script_tone = st.selectbox("Script Tone", ScriptAgent.available_tones())
        thumbnail_emotion = st.selectbox("Thumbnail Emotion", ThumbnailAgent.available_emotions())
        current_subs = st.number_input("Current Subscribers", min_value=0, value=0, step=100)
        posting_freq = st.selectbox("Posting Frequency", GrowthAgent.available_frequencies())

        st.markdown("<hr style='border-color:#2A2A2A'>", unsafe_allow_html=True)

        generate_all = st.button("⚡ Generate Everything", use_container_width=True)

        st.markdown("""
        <div style="margin-top:2rem;padding:1rem;background:#141414;border-radius:8px;border:1px solid #2A2A2A">
            <div style="font-size:0.7rem;color:#555;text-align:center;letter-spacing:1px;text-transform:uppercase">
                Powered by Claude AI<br>
                <span style="color:#FF0033">ShortForge AI © 2025</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    return {
        "topic": topic,
        "football_mode": football_mode,
        "hook_style": hook_style,
        "script_tone": script_tone,
        "thumbnail_emotion": thumbnail_emotion,
        "current_subs": current_subs,
        "posting_freq": posting_freq,
        "generate_all": generate_all,
    }


# ─── TAB RENDERERS ────────────────────────────────────────────────────────────

def tab_ideas(topic: str, football_mode: bool):
    st.markdown("## 💡 Viral Idea Generator")
    st.markdown("Generate 20 scored viral ideas ranked by virality potential.")

    col1, col2 = st.columns([3, 1])
    with col1:
        btn = st.button("🚀 Generate 20 Ideas", key="gen_ideas")
    with col2:
        filter_score = st.slider("Min Score", 0, 100, 60, key="idea_filter")

    if btn:
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Forging viral ideas..."):
            agent = IdeaAgent()
            st.session_state.ideas_result = agent.generate_ideas(msg, football_mode)

    result = st.session_state.ideas_result
    if not result:
        st.info("👆 Enter a topic and click Generate to start.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    ideas = result.get("ideas", [])
    filtered = [i for i in ideas if i.get("viral_score", 0) >= filter_score]

    st.markdown(f"<div style='color:#888;font-size:0.85rem;margin-bottom:1rem'>Showing {len(filtered)}/{len(ideas)} ideas (score ≥ {filter_score})</div>", unsafe_allow_html=True)

    if result.get("top_insight"):
        st.markdown(f"<div style='background:#1E1E1E;border-left:3px solid #FFD700;padding:0.75rem 1rem;border-radius:0 8px 8px 0;margin-bottom:1.25rem;color:#ccc;font-size:0.9rem'>💡 <strong>Key Insight:</strong> {result['top_insight']}</div>", unsafe_allow_html=True)

    for idea in filtered:
        render_idea_card(idea)
        # Allow selecting idea as topic for other tabs
        if st.button(f"Use this idea →", key=f"use_idea_{idea.get('rank')}"):
            st.session_state.current_topic = idea.get("title", topic)
            st.success(f"Selected: {idea.get('title')}")


def tab_hooks(topic: str, hook_style: str, football_mode: bool):
    st.markdown("## 🎣 Hook Generator")
    st.markdown("10 attention-grabbing hooks that stop the scroll in 3 seconds.")

    if st.button("🎯 Generate 10 Hooks", key="gen_hooks"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Crafting scroll-stopping hooks..."):
            agent = HookAgent()
            st.session_state.hooks_result = agent.generate_hooks(msg, hook_style, football_mode)

    result = st.session_state.hooks_result
    if not result:
        st.info("👆 Generate hooks for your topic.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    hooks = result.get("hooks", [])
    best_idx = result.get("best_hook", 1) - 1
    strategy = result.get("strategy_note", "")

    if strategy:
        st.markdown(f"<div style='background:#1E1E1E;border-left:3px solid #FF0033;padding:0.75rem 1rem;border-radius:0 8px 8px 0;margin-bottom:1.25rem;color:#ccc;font-size:0.9rem'>🧠 <strong>Strategy:</strong> {strategy}</div>", unsafe_allow_html=True)

    for i, hook in enumerate(hooks):
        is_best = (i == best_idx)
        render_hook_card(hook, is_best)
        if is_best:
            if st.button("Use as script hook →", key=f"use_hook_{i}"):
                st.session_state.selected_hook = hook.get("hook_text", "")
                st.success("Hook selected for script generation!")


def tab_script(topic: str, script_tone: str, football_mode: bool):
    st.markdown("## 📝 Shorts Script Generator")
    st.markdown("Full 30-60 second scripts with hook, story, curiosity loop, and CTA.")

    selected_hook = st.session_state.get("selected_hook", "")
    hook_input = st.text_area(
        "Opening Hook (or leave blank for AI to write one)",
        value=selected_hook,
        height=70,
        placeholder="Paste a hook from the Hook Generator, or leave empty...",
    )

    if st.button("✍️ Generate Script", key="gen_script"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Writing your viral script..."):
            agent = ScriptAgent()
            st.session_state.script_result = agent.generate_script(msg, hook_input, script_tone, football_mode)

    result = st.session_state.script_result
    if not result:
        st.info("👆 Generate a script for your Short.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    duration = result.get("estimated_duration_seconds", 0)
    word_count = result.get("word_count", 0)
    script = result.get("script", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Duration</div><div class='metric-value' style='color:var(--red)'>{duration}s</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Words</div><div class='metric-value' style='color:var(--gold)'>{word_count}</div></div>", unsafe_allow_html=True)
    with col3:
        wpm = int(word_count / (duration / 60)) if duration else 0
        st.markdown(f"<div class='metric-card'><div class='metric-label'>WPM</div><div class='metric-value' style='color:var(--green)'>{wpm}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    sections = [
        ("hook", "HOOK", "label-hook", "0:00 - 0:03"),
        ("main_story", "MAIN STORY", "label-story", "0:03 - 0:45"),
        ("curiosity_loop", "CURIOSITY LOOP", "label-loop", "0:45 - 0:55"),
        ("call_to_action", "CALL TO ACTION", "label-cta", "0:55 - 1:00"),
    ]

    for key, label, css_class, time_range in sections:
        section = script.get(key, {})
        if not section:
            continue
        text = section.get("text", "")
        visual = section.get("visual_cue", "")
        overlay = section.get("text_overlay", "")

        st.markdown(f"""
        <div class="script-section">
            <span class="section-label {css_class}">{label}</span>
            <span style="float:right;font-size:0.75rem;color:#555">{time_range}</span>
            <div class="script-text">{text}</div>
            {"<div class='visual-cue'>🎬 " + visual + "</div>" if visual else ""}
            {"<div class='visual-cue'>📝 TEXT: " + overlay + "</div>" if overlay else ""}
        </div>
        """, unsafe_allow_html=True)

    # Full readable script
    with st.expander("📄 Full Readable Script (copy-ready)"):
        full = result.get("full_script_readable", "")
        st.text_area("", value=full, height=300, label_visibility="collapsed")

    pro_tips = result.get("pro_tips", [])
    if pro_tips:
        st.markdown("**🏆 Pro Tips:**")
        for tip in pro_tips:
            st.markdown(f"- {tip}")


def tab_thumbnail(topic: str, thumbnail_emotion: str, football_mode: bool):
    st.markdown("## 🖼️ Thumbnail Intelligence System")
    st.markdown("Data-driven thumbnail strategies with psychology-backed design.")

    if st.button("🎨 Generate Thumbnail Strategy", key="gen_thumb"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Analyzing thumbnail psychology..."):
            agent = ThumbnailAgent()
            st.session_state.thumbnail_result = agent.generate_thumbnail_strategy(msg, thumbnail_emotion, football_mode)

    result = st.session_state.thumbnail_result
    if not result:
        st.info("👆 Generate thumbnail concepts for your Short.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    concepts = result.get("thumbnail_concepts", [])
    recommended = result.get("recommended_concept", 1) - 1
    mobile_tip = result.get("mobile_optimization_tip", "")
    donts = result.get("thumbnail_dont", [])

    if mobile_tip:
        st.markdown(f"<div style='background:#1E1E1E;border-left:3px solid #FF6B35;padding:0.75rem 1rem;border-radius:0 8px 8px 0;margin-bottom:1.25rem;color:#ccc;font-size:0.9rem'>📱 <strong>Mobile Tip:</strong> {mobile_tip}</div>", unsafe_allow_html=True)

    for i, concept in enumerate(concepts):
        is_rec = (i == recommended)
        label = "⭐ RECOMMENDED" if is_rec else f"Concept {i+1}"
        border_color = "#FFD700" if is_rec else "#2A2A2A"

        with st.expander(f"{label}: {concept.get('concept_name', '')}", expanded=is_rec):
            col_l, col_r = st.columns([1, 1])

            with col_l:
                st.markdown("**🎨 Color Palette**")
                palette = concept.get("color_palette", {})
                for color_key in ["primary", "secondary", "accent", "background"]:
                    hex_val = palette.get(color_key, "#000000")
                    st.markdown(f"<span class='color-swatch' style='background:{hex_val}'></span> **{color_key.title()}:** `{hex_val}`", unsafe_allow_html=True)
                if palette.get("rationale"):
                    st.caption(palette["rationale"])

                st.markdown("<br>**📝 Text Strategy**", unsafe_allow_html=True)
                text_data = concept.get("thumbnail_text", {})
                st.markdown(f"**Main:** {text_data.get('main_text', '')}")
                st.markdown(f"**Sub:** {text_data.get('sub_text', '')}")
                st.markdown(f"**Font:** {text_data.get('font_style', '')}")
                st.markdown(f"**Placement:** {text_data.get('text_placement', '')}")

            with col_r:
                st.markdown("**📐 Composition**")
                comp = concept.get("composition", {})
                st.markdown(f"- Layout: {comp.get('layout', '')}")
                st.markdown(f"- Focal Point: {comp.get('focal_point', '')}")
                st.markdown(f"- Background: {comp.get('background_style', '')}")

                st.markdown("<br>**🧠 Psychology**", unsafe_allow_html=True)
                psych = concept.get("psychology", {})
                st.markdown(f"**Why it works:** {psych.get('why_it_works', '')}")
                st.markdown(f"**Curiosity gap:** {psych.get('curiosity_gap', '')}")

                ctr = concept.get("ctr_score", 0)
                ctr_color = score_to_color(ctr)
                st.markdown(f"<div style='margin-top:1rem'>CTR Score: <strong style='color:{ctr_color};font-size:1.3rem'>{ctr}/100</strong></div>", unsafe_allow_html=True)

    if donts:
        st.markdown("**❌ Thumbnail Don'ts:**")
        for d in donts:
            st.markdown(f"- {d}")


def tab_seo(topic: str, football_mode: bool):
    st.markdown("## 🔍 SEO Generator")
    st.markdown("Titles, descriptions, hashtags, and keywords for maximum discovery.")

    script_context = st.text_area(
        "Script context (optional)",
        height=60,
        placeholder="Paste a brief script summary to improve SEO relevance...",
    )

    if st.button("🔎 Generate SEO Package", key="gen_seo"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Optimizing for YouTube search..."):
            agent = SEOAgent()
            st.session_state.seo_result = agent.generate_seo(msg, script_context, football_mode)

    result = st.session_state.seo_result
    if not result:
        st.info("👆 Generate SEO for your Short.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    seo_tab1, seo_tab2, seo_tab3, seo_tab4 = st.tabs(["📌 Titles", "📄 Description", "#️⃣ Hashtags", "🔑 Keywords"])

    with seo_tab1:
        titles = result.get("titles", [])
        best_idx = result.get("best_title", 1) - 1
        for i, t in enumerate(titles):
            is_best = (i == best_idx)
            score = t.get("seo_score", 0)
            color = score_to_color(score)
            star = "⭐ " if is_best else ""
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid {'#FFD700' if is_best else 'var(--border)'};
                        border-radius:8px;padding:1rem;margin-bottom:0.5rem">
                <div style="font-size:1.05rem;font-weight:500">{star}{t.get('title','')}</div>
                <div style="color:#666;font-size:0.8rem;margin-top:0.3rem">
                    SEO Score: <span style="color:{color};font-weight:700">{score}</span> &nbsp;|&nbsp;
                    {t.get('character_count',0)} chars &nbsp;|&nbsp;
                    Clickbait: {t.get('click_bait_level','')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with seo_tab2:
        desc = result.get("description", {})
        full_desc = desc.get("full_description", "")
        char_count = desc.get("character_count", 0)
        st.markdown(f"**Character count:** {char_count}")
        st.text_area("YouTube Description", value=full_desc, height=250, label_visibility="collapsed")

    with seo_tab3:
        hashtags = result.get("hashtags", {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Primary**")
            for tag in hashtags.get("primary", []):
                st.markdown(f"`{tag}`")
        with col2:
            st.markdown("**Niche**")
            for tag in hashtags.get("niche", []):
                st.markdown(f"`{tag}`")
        with col3:
            st.markdown("**Trending**")
            for tag in hashtags.get("trending", []):
                st.markdown(f"`{tag}`")

        all_tags = (
            hashtags.get("primary", []) +
            hashtags.get("niche", []) +
            hashtags.get("trending", [])
        )
        all_tags_str = " ".join(all_tags)
        st.text_area("Copy all hashtags", value=all_tags_str, height=80)

    with seo_tab4:
        kw = result.get("keywords", {})
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Primary Keywords**")
            for k in kw.get("primary_keywords", []):
                st.markdown(f"- {k}")
            st.markdown("**Long-tail Keywords**")
            for k in kw.get("long_tail", []):
                st.markdown(f"- {k}")
        with col2:
            st.markdown("**LSI Keywords**")
            for k in kw.get("lsi_keywords", []):
                st.markdown(f"- {k}")
            competition = kw.get("competition_level", "")
            if competition:
                st.markdown(f"**Competition Level:** `{competition}`")

    if result.get("seo_strategy"):
        st.info(f"💡 **SEO Strategy:** {result['seo_strategy']}")


def tab_viral_score(topic: str, football_mode: bool):
    st.markdown("## 📊 Viral Score System")
    st.markdown("Score your content across 5 viral dimensions.")

    col1, col2 = st.columns(2)
    with col1:
        hook_input = st.text_area("Hook", height=70, placeholder="Your opening hook...")
        title_input = st.text_input("Title", placeholder="Your video title...")
    with col2:
        script_input = st.text_area("Script Summary", height=70, placeholder="Brief script summary...")

    if st.button("📊 Score My Content", key="gen_score"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Analyzing viral potential..."):
            agent = GrowthAgent()
            st.session_state.viral_score_result = agent.score_content(
                topic=msg,
                hook=hook_input,
                script_summary=script_input,
                title=title_input,
                football_mode=football_mode,
            )

    result = st.session_state.viral_score_result
    if not result:
        st.info("👆 Enter your content details and score it.")
        return

    render_viral_score(result)


def tab_calendar(topic: str, posting_freq: str, football_mode: bool):
    st.markdown("## 📅 Content Calendar")
    st.markdown("30-day strategic posting plan to build channel momentum.")

    if st.button("📅 Generate 30-Day Calendar", key="gen_calendar"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Planning your 30-day content strategy..."):
            agent = GrowthAgent()
            st.session_state.calendar_result = agent.generate_calendar(msg, posting_freq, football_mode)

    result = st.session_state.calendar_result
    if not result:
        st.info("👆 Generate your content calendar.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    strategy = result.get("strategy_overview", "")
    if strategy:
        st.markdown(f"<div style='background:#1E1E1E;border-left:3px solid #FF0033;padding:0.75rem 1rem;border-radius:0 8px 8px 0;margin-bottom:1.5rem;color:#ccc;font-size:0.9rem'>📋 <strong>Strategy:</strong> {strategy}</div>", unsafe_allow_html=True)

    monthly = result.get("monthly_strategy", {})
    milestones = result.get("milestone_targets", {})

    if monthly:
        col1, col2, col3, col4 = st.columns(4)
        weeks = [
            (col1, "week1_focus", "Week 1"),
            (col2, "week2_focus", "Week 2"),
            (col3, "week3_focus", "Week 3"),
            (col4, "week4_focus", "Week 4"),
        ]
        for col, key, label in weeks:
            with col:
                st.markdown(f"<div class='metric-card'><div class='metric-label'>{label}</div><div style='color:var(--red);font-size:0.85rem;margin-top:0.3rem'>{monthly.get(key,'')}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    weeks_data = result.get("weeks", [])
    for week in weeks_data:
        week_num = week.get("week", "")
        theme = week.get("theme", "")
        goal = week.get("goal", "")
        days = week.get("days", [])

        with st.expander(f"📅 Week {week_num}: {theme}", expanded=(week_num == 1)):
            st.caption(f"🎯 Goal: {goal}")
            st.markdown(f"<div class='cal-week-header'>WEEK {week_num} — {theme.upper()}</div>", unsafe_allow_html=True)
            for day in days:
                day_num = day.get("day", "")
                title = day.get("title_idea", "")
                content_type = day.get("content_type", "")
                post_time = day.get("posting_time", "")
                notes = day.get("notes", "")
                expected = day.get("expected_performance", "")

                st.markdown(f"""
                <div class="cal-day">
                    <div class="cal-day-num">Day {day_num}<br><span style="color:#555;font-size:0.7rem">{post_time}</span></div>
                    <div class="cal-day-content">
                        <h5>{title}</h5>
                        <p>{content_type} · {expected}</p>
                        {"<p style='color:#666;font-size:0.75rem;margin-top:0.2rem'>💡 " + notes + "</p>" if notes else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    if milestones:
        st.markdown("<br>### 🏆 Milestone Targets", unsafe_allow_html=False)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Day 7</div><div style='color:var(--green);font-size:0.9rem;margin-top:0.3rem'>{milestones.get('day_7','')}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Day 14</div><div style='color:var(--gold);font-size:0.9rem;margin-top:0.3rem'>{milestones.get('day_14','')}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Day 30</div><div style='color:var(--red);font-size:0.9rem;margin-top:0.3rem'>{milestones.get('day_30','')}</div></div>", unsafe_allow_html=True)


def tab_growth(topic: str, current_subs: int, football_mode: bool):
    st.markdown("## 🚀 Channel Growth Advisor")
    st.markdown("Personalized growth roadmap with content pillars and audience strategy.")

    if st.button("🚀 Generate Growth Strategy", key="gen_growth"):
        valid, msg = validate_topic(topic)
        if not valid:
            st.error(msg)
            return
        with st.spinner("Building your growth roadmap..."):
            agent = GrowthAgent()
            st.session_state.growth_result = agent.get_growth_advice(msg, current_subs, football_mode)

    result = st.session_state.growth_result
    if not result:
        st.info("👆 Generate your channel growth strategy.")
        return
    if result.get("error"):
        st.error(result.get("message"))
        return

    analysis = result.get("channel_analysis", {})
    posting = result.get("posting_strategy", {})
    audience = result.get("audience_targeting", {})
    phases = result.get("growth_phases", [])
    pillars = result.get("content_pillars", [])
    monetization = result.get("monetization_path", {})

    # Channel analysis header
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Growth Potential</div><div class='metric-value' style='color:var(--green);font-size:1.3rem'>{analysis.get('growth_potential','')}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Competition</div><div class='metric-value' style='color:var(--gold);font-size:1.3rem'>{analysis.get('competition_level','')}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Stage</div><div class='metric-value' style='color:var(--red);font-size:1.1rem'>{analysis.get('current_stage','')}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    growth_tab1, growth_tab2, growth_tab3, growth_tab4 = st.tabs(["📌 Content Pillars", "👥 Audience", "📈 Growth Phases", "💰 Monetization"])

    with growth_tab1:
        for pillar in pillars:
            with st.expander(f"🏛️ {pillar.get('pillar_name','')} — {pillar.get('posting_ratio','')}"):
                st.write(pillar.get("description", ""))
                ideas = pillar.get("example_ideas", [])
                if ideas:
                    st.markdown("**Example Ideas:**")
                    for idea in ideas:
                        st.markdown(f"- {idea}")

    with growth_tab2:
        st.markdown(f"**🎯 Primary:** {audience.get('primary_audience','')}")
        st.markdown(f"**🎯 Secondary:** {audience.get('secondary_audience','')}")
        demo = audience.get("demographics", {})
        if demo:
            st.markdown(f"**Age Range:** {demo.get('age_range','')}")
            interests = demo.get("interests", [])
            if interests:
                st.markdown(f"**Interests:** {', '.join(interests)}")
        col_l, col_r = st.columns(2)
        with col_l:
            pain_points = audience.get("pain_points", [])
            if pain_points:
                st.markdown("**😤 Pain Points:**")
                for p in pain_points:
                    st.markdown(f"- {p}")
        with col_r:
            desires = audience.get("desires", [])
            if desires:
                st.markdown("**✨ Desires:**")
                for d in desires:
                    st.markdown(f"- {d}")

    with growth_tab3:
        for phase in phases:
            phase_num = phase.get("phase", "")
            name = phase.get("name", "")
            duration = phase.get("duration", "")
            goal = phase.get("goal", "")
            tactics = phase.get("tactics", [])
            metrics = phase.get("success_metrics", "")
            colors = ["#FF0033", "#FFD700", "#00FF88"]
            c = colors[phase_num - 1] if phase_num <= 3 else "#888"
            with st.expander(f"Phase {phase_num}: {name} ({duration})", expanded=(phase_num == 1)):
                st.markdown(f"<div style='border-left:3px solid {c};padding-left:1rem'>", unsafe_allow_html=True)
                st.markdown(f"**🎯 Goal:** {goal}")
                if tactics:
                    st.markdown("**⚡ Tactics:**")
                    for t in tactics:
                        st.markdown(f"- {t}")
                st.markdown(f"**📊 Success Metrics:** {metrics}")
                st.markdown("</div>", unsafe_allow_html=True)

    with growth_tab4:
        st.markdown(f"**🌱 At 1K Subs:** {monetization.get('milestone_1k_subs','')}")
        st.markdown(f"**🚀 At 10K Subs:** {monetization.get('milestone_10k_subs','')}")
        revenues = monetization.get("revenue_streams", [])
        if revenues:
            st.markdown("**💰 Revenue Streams:**")
            for r in revenues:
                st.markdown(f"- {r}")

    wins = result.get("quick_wins", [])
    if wins:
        st.markdown("### ⚡ Quick Wins")
        for w in wins:
            st.markdown(f"<div style='background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--green);border-radius:0 8px 8px 0;padding:0.6rem 1rem;margin-bottom:0.4rem;font-size:0.9rem'>{w}</div>", unsafe_allow_html=True)


# ─── MAIN APP ─────────────────────────────────────────────────────────────────

def main():
    init_session()
    settings = render_sidebar()

    topic = settings["topic"] or st.session_state.current_topic
    football_mode = settings["football_mode"]

    # ── Hero ──
    if football_mode:
        st.markdown("""
        <div class="hero">
            <div class="badge">⚽ Football Creator Mode Active</div>
            <h1>ShortForge AI</h1>
            <p>The ultimate AI engine for viral football YouTube Shorts — powered by Claude</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="football-banner">
            <div style="font-size:2.5rem">⚽</div>
            <div>
                <h3>Football Creator Mode</h3>
                <p>All features are now optimized for football content: player stories, match moments, records, and fan psychology</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hero">
            <div class="badge">⚡ AI Content Engine</div>
            <h1>ShortForge AI</h1>
            <p>Generate viral YouTube Shorts from any topic — ideas, hooks, scripts, thumbnails, SEO, and growth strategy</p>
        </div>
        """, unsafe_allow_html=True)

    # Handle "Generate Everything" button
    if settings["generate_all"] and topic:
        valid, msg = validate_topic(topic)
        if valid:
            with st.spinner("⚡ Generating your complete content package... This may take a minute."):
                idea_agent = IdeaAgent()
                hook_agent = HookAgent()
                script_agent = ScriptAgent()
                thumb_agent = ThumbnailAgent()
                seo_agent = SEOAgent()
                growth_agent = GrowthAgent()

                st.session_state.ideas_result = idea_agent.generate_ideas(msg, football_mode)
                hooks_result = hook_agent.generate_hooks(msg, settings["hook_style"], football_mode)
                st.session_state.hooks_result = hooks_result
                best_hook = hooks_result.get("hooks", [{}])[0].get("hook_text", "") if not hooks_result.get("error") else ""
                st.session_state.script_result = script_agent.generate_script(msg, best_hook, settings["script_tone"], football_mode)
                st.session_state.thumbnail_result = thumb_agent.generate_thumbnail_strategy(msg, settings["thumbnail_emotion"], football_mode)
                st.session_state.seo_result = seo_agent.generate_seo(msg, "", football_mode)
                st.success("✅ Complete content package generated! Browse the tabs below.")
        else:
            st.error(msg)

    # ── Main Tabs ──
    tabs = st.tabs([
        "💡 Ideas",
        "🎣 Hooks",
        "📝 Script",
        "🖼️ Thumbnail",
        "🔍 SEO",
        "📊 Viral Score",
        "📅 Calendar",
        "🚀 Growth",
    ])

    with tabs[0]:
        tab_ideas(topic, football_mode)
    with tabs[1]:
        tab_hooks(topic, settings["hook_style"], football_mode)
    with tabs[2]:
        tab_script(topic, settings["script_tone"], football_mode)
    with tabs[3]:
        tab_thumbnail(topic, settings["thumbnail_emotion"], football_mode)
    with tabs[4]:
        tab_seo(topic, football_mode)
    with tabs[5]:
        tab_viral_score(topic, football_mode)
    with tabs[6]:
        tab_calendar(topic, settings["posting_freq"], football_mode)
    with tabs[7]:
        tab_growth(topic, settings["current_subs"], football_mode)


if __name__ == "__main__":
    main()
