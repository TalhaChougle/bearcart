import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import time
import requests
import urllib.parse
from datetime import datetime, timedelta
import random
import string
import io
import re

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="BearCart Intelligence",
    layout="wide",
    page_icon="🐻",
    initial_sidebar_state="expanded"
)

# ==========================================
# LIGHT THEME — CLEAN ANALYTICS PALETTE
# ==========================================
st.markdown("""
<style>
:root {
    --bg:        #F7F8FA;
    --surface:   #FFFFFF;
    --border:    #E4E7EC;
    --text:      #111827;
    --muted:     #6B7280;
    --accent:    #2563EB;
    --accent2:   #0EA5E9;
    --green:     #059669;
    --amber:     #D97706;
    --red:       #DC2626;
    --purple:    #7C3AED;
    --shadow:    0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04);
}

html, body, .stApp {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Radio buttons */
div[data-testid="stRadio"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    display: block !important;
}
div[data-testid="stRadio"] label:hover { background: var(--bg) !important; }

/* Headings */
h1, h2, h3, h4 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    letter-spacing: -0.3px;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: var(--shadow) !important;
}
div[data-testid="metric-container"] label,
div[data-testid="metric-container"] [data-testid="stMetricLabel"],
div[data-testid="metric-container"] [data-testid="stMetricLabel"] p,
div[data-testid="metric-container"] [data-testid="stMetricLabel"] div {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    color: var(--muted) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"],
div[data-testid="metric-container"] [data-testid="stMetricValue"] div {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    letter-spacing: -0.5px !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"],
div[data-testid="metric-container"] [data-testid="stMetricDelta"] div {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 20px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #1D4ED8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: var(--muted) !important;
    padding: 10px 20px !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* Info / success / warning boxes */
.stSuccess, .stInfo, .stWarning {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* File uploader */
.stFileUploader {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
.stFileUploader > div {
    background: var(--surface) !important;
}
[data-testid="stFileUploadDropzone"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    color: var(--text) !important;
}
[data-testid="stFileUploadDropzone"] button {
    background: var(--accent) !important;
    color: white !important;
    border-radius: 6px !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Plotly chart container */
.js-plotly-plot { border-radius: 12px !important; }

/* Custom card class */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: var(--shadow);
    margin-bottom: 16px;
}

.tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}
.tag-blue  { background: #DBEAFE; color: #1D4ED8; }
.tag-green { background: #D1FAE5; color: #065F46; }
.tag-amber { background: #FEF3C7; color: #92400E; }
.tag-red   { background: #FEE2E2; color: #991B1B; }
.tag-purple{ background: #EDE9FE; color: #5B21B6; }

.section-header {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    margin-bottom: 12px;
    margin-top: 4px;
}

/* Chat bubbles */
.chat-user {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 12px 12px 2px 12px;
    padding: 10px 14px;
    margin: 6px 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #1E3A8A;
    text-align: right;
}
.chat-ai {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px 12px 12px 2px;
    padding: 12px 16px;
    margin: 6px 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: var(--text);
    line-height: 1.6;
}
.chat-ai strong { color: var(--accent); }

/* Coupon box */
.coupon-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0FDF4 100%);
    border: 2px dashed #93C5FD;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 1.4rem;
    font-weight: 500;
    color: var(--accent);
    letter-spacing: 3px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PLOTLY LIGHT TEMPLATE
# ==========================================
PLOT_TEMPLATE = dict(
    layout=go.Layout(
        font=dict(family="DM Sans, sans-serif", color="#111827"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        colorway=["#2563EB", "#0EA5E9", "#059669", "#D97706", "#7C3AED", "#DC2626"],
        xaxis=dict(gridcolor="#F3F4F6", linecolor="#E4E7EC", tickfont=dict(color="#6B7280")),
        yaxis=dict(gridcolor="#F3F4F6", linecolor="#E4E7EC", tickfont=dict(color="#6B7280")),
        legend=dict(bgcolor="white", bordercolor="#E4E7EC", borderwidth=1),
        margin=dict(l=40, r=20, t=40, b=40),
    )
)

def styled_chart(fig, title=""):
    fig.update_layout(
        template=None,
        font=dict(family="Arial, sans-serif", color="#111827"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title=dict(text=f"<b>{title}</b>", font=dict(size=14, color="#111827"), x=0, pad=dict(l=0)),
        colorway=["#2563EB", "#0EA5E9", "#059669", "#D97706", "#7C3AED", "#DC2626"],
        margin=dict(l=10, r=10, t=45 if title else 20, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=12)),
    )
    fig.update_xaxes(gridcolor="#F3F4F6", linecolor="#E4E7EC", tickfont=dict(color="#6B7280", size=11))
    fig.update_yaxes(gridcolor="#F3F4F6", linecolor="#E4E7EC", tickfont=dict(color="#6B7280", size=11))
    return fig

# ==========================================
# DATA ENGINE
# ==========================================
@st.cache_data
def get_data(file_bytes=None):
    if file_bytes is not None:
        import io
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        np.random.seed(42)
        n = 1500
        df = pd.DataFrame({
            "session_id": range(n),
            "pages_viewed": np.random.randint(1, 10, n),
            "product_views": np.random.randint(0, 8, n),
            "add_to_cart": np.random.choice([0, 1, 2], n, p=[0.7, 0.2, 0.1]),
            "time_spent_sec": np.random.randint(10, 900, n),
            "device": np.random.choice(["Mobile", "Desktop"], n, p=[0.7, 0.3]),
            "location": np.random.choice(["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune"], n),
            "hour_of_day": np.random.choice(range(24), n, p=[
                0.01,0.01,0.01,0.01,0.02,0.03,0.04,0.06,0.07,0.06,0.05,0.05,
                0.05,0.05,0.05,0.06,0.06,0.07,0.07,0.06,0.05,0.04,0.03,0.02
            ]),
            "order_value": np.where(np.random.random(n) > 0.85, np.random.uniform(30, 200, n), 0.0),
            "traffic_source": np.random.choice(["gsearch", "bsearch", "socialbook", "direct", "email"], n, p=[0.45, 0.2, 0.15, 0.12, 0.08]),
            "is_repeat_session": np.random.choice([0, 1], n, p=[0.7, 0.3]),
            "created_at": pd.date_range("2024-01-01", periods=n, freq="2h"),
        })

    # Normalize columns
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Standardise traffic source
    if "traffic_source" in df.columns:
        df["traffic_source"] = df["traffic_source"].fillna("direct").str.lower().str.strip()
        df["traffic_source"] = df["traffic_source"].replace({
            "gsearch": "Google Search", "gsearch_ads": "Google Ads",
            "bsearch": "Bing Search", "bsearch_ads": "Bing Ads",
            "socialbook": "Social", "nan": "Direct", "nan_ads": "Direct",
        })
        mask = ~df["traffic_source"].isin(["Google Search","Google Ads","Bing Search","Bing Ads","Social","Direct","email"])
        df.loc[mask, "traffic_source"] = "Direct"

    if "device" in df.columns:
        df["device"] = df["device"].str.capitalize()

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["hour_of_day"] = df["created_at"].dt.hour
        df["month"] = df["created_at"].dt.to_period("M").astype(str)
        df["week"] = df["created_at"].dt.isocalendar().week.astype(int)
        df["day_of_week"] = df["created_at"].dt.day_name()

    if "hour_of_day" not in df.columns:
        df["hour_of_day"] = np.random.randint(0, 24, len(df))
    if "session_id" not in df.columns:
        df["session_id"] = range(1, len(df) + 1)
    if "order_value" not in df.columns:
        df["order_value"] = 0.0
    if "location" not in df.columns:
        df["location"] = "Unknown"
    if "is_repeat_session" not in df.columns:
        df["is_repeat_session"] = 0

    # Intent scoring
    df["intent_score"] = (
        df["product_views"] * 2 +
        df["add_to_cart"] * 8 +
        df["time_spent_sec"] / 60 +
        df["pages_viewed"]
    )

    def segment(score):
        if score > 25: return "High Intent"
        elif score > 12: return "Medium Intent"
        return "Low Intent"

    df["segment"] = df["intent_score"].apply(segment)
    df["potential_revenue"] = df["segment"].map(
        lambda x: random.randint(1000, 5000) if x == "High Intent" else 0
    )

    return df

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("## 🐻 BearCart AI")
    st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)

    menu = st.radio(
        "",
        ["🚀 Dashboard", "📊 Deep Analysis", "🧠 AI Chat", "⚡ Action Center", "🔮 Future Lab", "🧹 Data Lab", "▶ Use Cases"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="section-header">Data Source</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        df = get_data(file_bytes)
        st.success(f"✅ {len(df):,} rows loaded")
    else:
        df = get_data()
        st.info("ℹ️ Demo dataset active")

    st.markdown("---")
    st.markdown('<div class="section-header">Quick Stats</div>', unsafe_allow_html=True)
    hi = len(df[df["segment"] == "High Intent"])
    conv = len(df[df["order_value"] > 0])
    st.markdown(f"""
    <div style='font-family:DM Sans;font-size:0.82rem;line-height:2'>
    📦 Sessions: <b>{len(df):,}</b><br>
    🔥 High Intent: <b>{hi:,}</b><br>
    💳 Conversions: <b>{conv:,}</b><br>
    📈 Conv. Rate: <b>{conv/len(df)*100:.1f}%</b>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# HELPER: segment color map
# ==========================================
SEG_COLORS = {"High Intent": "#2563EB", "Medium Intent": "#0EA5E9", "Low Intent": "#D1D5DB"}

# ==========================================
# 1. DASHBOARD
# ==========================================
if menu == "🚀 Dashboard":
    st.markdown("# Traffic Intelligence")
    st.markdown('<p style="color:#6B7280;font-family:DM Sans;margin-top:-10px">Real-time clickstream analytics · BearCart</p>', unsafe_allow_html=True)

    # ---- KPI Row ----
    conv_rate = len(df[df["order_value"] > 0]) / len(df) * 100
    avg_order = df[df["order_value"] > 0]["order_value"].mean() if len(df[df["order_value"] > 0]) > 0 else 0
    revenue = df["order_value"].sum()
    mobile_share = (df["device"].str.lower() == "mobile").mean() * 100 if "device" in df.columns else 0

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px">
        <div style="background:#fff;border:1px solid #E4E7EC;border-radius:12px;padding:16px 18px">
            <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Total Sessions</div>
            <div style="font-size:28px;font-weight:800;color:#111827;letter-spacing:-1px;line-height:1">{len(df):,}</div>
            <div style="font-size:12px;font-weight:600;color:#059669;margin-top:6px">▲ +12%</div>
        </div>
        <div style="background:#fff;border:1px solid #E4E7EC;border-radius:12px;padding:16px 18px">
            <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Revenue</div>
            <div style="font-size:28px;font-weight:800;color:#111827;letter-spacing:-1px;line-height:1">₹{revenue:,.0f}</div>
            <div style="font-size:12px;font-weight:600;color:#059669;margin-top:6px">▲ +8.3%</div>
        </div>
        <div style="background:#fff;border:1px solid #E4E7EC;border-radius:12px;padding:16px 18px">
            <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Conv. Rate</div>
            <div style="font-size:28px;font-weight:800;color:#111827;letter-spacing:-1px;line-height:1">{conv_rate:.1f}%</div>
            <div style="font-size:12px;font-weight:600;color:#059669;margin-top:6px">▲ +0.4%</div>
        </div>
        <div style="background:#fff;border:1px solid #E4E7EC;border-radius:12px;padding:16px 18px">
            <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Avg. Order</div>
            <div style="font-size:28px;font-weight:800;color:#111827;letter-spacing:-1px;line-height:1">₹{avg_order:.0f}</div>
            <div style="font-size:12px;font-weight:600;color:#DC2626;margin-top:6px">▼ -2.1%</div>
        </div>
        <div style="background:#fff;border:1px solid #E4E7EC;border-radius:12px;padding:16px 18px">
            <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Mobile Share</div>
            <div style="font-size:28px;font-weight:800;color:#111827;letter-spacing:-1px;line-height:1">{mobile_share:.0f}%</div>
            <div style="font-size:12px;font-weight:600;color:#059669;margin-top:6px">▲ steady</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ---- Row 1: Hourly Traffic + Segment Donut ----
    c1, c2 = st.columns([2, 1])
    with c1:
        trend = df.groupby("hour_of_day").size().reset_index(name="Sessions")
        trend.columns = ["Hour", "Sessions"]
        trend = trend.sort_values("Hour").reset_index(drop=True)
        # Ensure all 24 hours exist
        all_hours = pd.DataFrame({"Hour": range(24)})
        trend = all_hours.merge(trend, on="Hour", how="left").fillna(0)
        trend["Sessions"] = trend["Sessions"].astype(int)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend["Hour"], y=trend["Sessions"],
            mode="lines", fill="tozeroy",
            line=dict(color="#2563EB", width=2.5),
            fillcolor="rgba(37,99,235,0.08)",
            hovertemplate="<b>%{x}:00</b><br>Sessions: %{y}<extra></extra>"
        ))
        fig = styled_chart(fig, "Hourly Traffic Pattern")
        fig.update_xaxes(tickvals=list(range(0, 24, 3)), ticktext=[f"{h}:00" for h in range(0, 24, 3)])
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        seg_counts = df["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig2 = go.Figure(go.Pie(
            labels=seg_counts["Segment"],
            values=seg_counts["Count"],
            hole=0.62,
            marker=dict(colors=["#2563EB", "#0EA5E9", "#E5E7EB"]),
            textinfo="percent",
            hoverinfo="label+value",
        ))
        fig2.update_layout(
            annotations=[dict(text="Segments", x=0.5, y=0.5, font_size=13, showarrow=False, font_color="#111827", font_family="DM Sans")],
            showlegend=True,
            legend=dict(orientation="h", x=0, y=-0.12, font=dict(size=11)),
            margin=dict(t=40,b=10,l=10,r=10),
            paper_bgcolor="white",
            font=dict(family="DM Sans"),
        )
        fig2.update_layout(title=dict(text="User Segments", font=dict(size=15, weight=700), x=0))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ---- Row 2: Traffic Sources + Device Split ----
    c3, c4 = st.columns([1, 1])
    with c3:
        if "traffic_source" in df.columns:
            src = df["traffic_source"].value_counts().reset_index()
            src.columns = ["Source", "Sessions"]
            fig3 = go.Figure(go.Bar(
                x=src["Sessions"], y=src["Source"],
                orientation="h",
                marker=dict(color=["#2563EB","#0EA5E9","#059669","#D97706","#7C3AED"][:len(src)]),
                hovertemplate="%{y}: <b>%{x:,}</b><extra></extra>"
            ))
            fig3 = styled_chart(fig3, "Traffic Sources")
            fig3.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with c4:
        if "device" in df.columns:
            dev = df.groupby("device").agg(Sessions=("session_id","count"), Revenue=("order_value","sum")).reset_index()
            fig4 = go.Figure()
            fig4.add_trace(go.Bar(name="Sessions", x=dev["device"], y=dev["Sessions"], marker_color="#2563EB", yaxis="y"))
            fig4.add_trace(go.Scatter(name="Revenue ₹", x=dev["device"], y=dev["Revenue"], mode="lines+markers",
                                      line=dict(color="#D97706", width=2.5), marker=dict(size=8), yaxis="y2"))
            fig4.update_layout(
                yaxis=dict(title="Sessions", gridcolor="#F3F4F6"),
                yaxis2=dict(title="Revenue ₹", overlaying="y", side="right", gridcolor="#F3F4F6"),
                legend=dict(orientation="h", y=1.1),
                paper_bgcolor="white", plot_bgcolor="white",
                font=dict(family="DM Sans"),
                margin=dict(l=10,r=10,t=45,b=10),
                title=dict(text="Device: Sessions vs Revenue", font=dict(size=15,weight=700), x=0)
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    # ---- Row 3: Revenue over time ----
    if "month" in df.columns:
        monthly = df.groupby("month").agg(Revenue=("order_value","sum"), Sessions=("session_id","count")).reset_index()
        monthly = monthly.sort_values("month")
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=monthly["month"], y=monthly["Revenue"], name="Revenue ₹",
                              marker_color="#2563EB", opacity=0.85))
        fig5 = styled_chart(fig5, "Monthly Revenue Trend")
        st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

# ==========================================
# 2. DEEP ANALYSIS
# ==========================================
elif menu == "📊 Deep Analysis":
    st.markdown("# Deep Analysis")
    st.markdown('<p style="color:#6B7280;font-family:DM Sans;margin-top:-10px">Explore patterns, behaviours, and segment data</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Intent & Behaviour", "📍 Location", "📅 Time Patterns", "📐 Data Explorer"])

    # Tab 1: Intent & Behaviour
    with tab1:
        st.markdown("### Principle 1 — Know Your Audience")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Audience = User segments by intent, device, and behaviour patterns.</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.scatter(
                df.sample(min(1500, len(df))),
                x="time_spent_sec", y="product_views",
                color="segment",
                size="intent_score",
                color_discrete_map=SEG_COLORS,
                labels={"time_spent_sec": "Time Spent (sec)", "product_views": "Product Views"},
                opacity=0.65,
            )
            fig = styled_chart(fig, "Time Spent vs Product Views — by Segment")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with c2:
            # Simplify complexity — engagement funnel
            funnel_data = {
                "Stage": ["Sessions", "Page Views >3", "Product Views", "Add to Cart", "Purchased"],
                "Count": [
                    len(df),
                    len(df[df["pages_viewed"] > 3]),
                    len(df[df["product_views"] > 0]),
                    len(df[df["add_to_cart"] > 0]),
                    len(df[df["order_value"] > 0]),
                ]
            }
            fig2 = go.Figure(go.Funnel(
                y=funnel_data["Stage"],
                x=funnel_data["Count"],
                marker=dict(color=["#2563EB","#3B82F6","#60A5FA","#93C5FD","#059669"]),
                textposition="inside",
                textinfo="value+percent initial",
                connector=dict(line=dict(color="#E4E7EC", width=2))
            ))
            fig2.update_layout(
                paper_bgcolor="white", font=dict(family="DM Sans"),
                margin=dict(l=10,r=10,t=45,b=10),
                title=dict(text="Conversion Funnel", font=dict(size=15,weight=700), x=0)
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        # Intent score distribution
        fig3 = go.Figure()
        for seg, color in SEG_COLORS.items():
            sub = df[df["segment"] == seg]["intent_score"]
            fig3.add_trace(go.Histogram(x=sub, name=seg, marker_color=color, opacity=0.7, nbinsx=30))
        fig3 = styled_chart(fig3, "Intent Score Distribution by Segment")
        fig3.update_layout(barmode="overlay")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # Tab 2: Location
    with tab2:
        st.markdown("### Principle 8 — Provide Context")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Geographic breakdown of traffic, intent, and revenue contribution.</p>', unsafe_allow_html=True)

        if "location" in df.columns:
            loc = df.groupby("location").agg(
                Sessions=("session_id","count"),
                Revenue=("order_value","sum"),
                High_Intent=("segment", lambda x: (x=="High Intent").sum()),
                Avg_Intent=("intent_score","mean")
            ).reset_index().sort_values("Revenue", ascending=False)

            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure(go.Bar(
                    x=loc["location"], y=loc["Sessions"],
                    marker_color="#2563EB",
                    hovertemplate="<b>%{x}</b><br>Sessions: %{y:,}<extra></extra>"
                ))
                fig = styled_chart(fig, "Sessions by Location")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            with c2:
                fig2 = px.bar(
                    loc, x="location", y="Revenue",
                    color="Avg_Intent",
                    color_continuous_scale=["#BFDBFE","#2563EB"],
                    labels={"Revenue": "Revenue ₹", "Avg_Intent": "Avg Intent"}
                )
                fig2 = styled_chart(fig2, "Revenue & Avg Intent by Location")
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

            st.dataframe(
                loc.rename(columns={"High_Intent":"High Intent Users","Avg_Intent":"Avg Intent Score"}),
                use_container_width=True, hide_index=True
            )

    # Tab 3: Time Patterns
    with tab3:
        st.markdown("### Principle 9 — Interactive Elements")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Peak hours, weekly patterns, and seasonal revenue trends.</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            # Heatmap: hour vs segment
            pivot = df.groupby(["hour_of_day","segment"]).size().unstack(fill_value=0)
            fig = go.Figure(go.Heatmap(
                z=pivot.values.T,
                x=pivot.index,
                y=pivot.columns.tolist(),
                colorscale=[[0,"#F0F9FF"],[0.5,"#3B82F6"],[1,"#1E3A8A"]],
                hovertemplate="Hour %{x}:00<br>Segment: %{y}<br>Sessions: %{z}<extra></extra>"
            ))
            fig.update_layout(
                paper_bgcolor="white", font=dict(family="DM Sans"),
                margin=dict(l=10,r=10,t=45,b=10),
                title=dict(text="Sessions Heatmap: Hour × Segment", font=dict(size=15,weight=700), x=0),
                xaxis_title="Hour of Day", yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with c2:
            if "day_of_week" in df.columns:
                days_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                dow = df.groupby("day_of_week").agg(Sessions=("session_id","count"), Revenue=("order_value","sum")).reset_index()
                dow["day_of_week"] = pd.Categorical(dow["day_of_week"], categories=days_order, ordered=True)
                dow = dow.sort_values("day_of_week")
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=dow["day_of_week"], y=dow["Sessions"], name="Sessions", marker_color="#2563EB"))
                fig2.add_trace(go.Scatter(x=dow["day_of_week"], y=dow["Revenue"], name="Revenue ₹",
                                          mode="lines+markers", line=dict(color="#D97706",width=2.5), yaxis="y2"))
                fig2.update_layout(
                    yaxis=dict(title="Sessions", gridcolor="#F3F4F6"),
                    yaxis2=dict(title="Revenue ₹", overlaying="y", side="right"),
                    paper_bgcolor="white", plot_bgcolor="white",
                    font=dict(family="DM Sans"), legend=dict(orientation="h",y=1.1),
                    margin=dict(l=10,r=10,t=45,b=10),
                    title=dict(text="Weekly Traffic & Revenue", font=dict(size=15,weight=700), x=0)
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # Tab 4: Data Explorer
    with tab4:
        st.markdown("### Principle 3 — Choose the Right Chart Type")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Pick any two columns and chart type to explore the data interactively.</p>', unsafe_allow_html=True)

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        col_a, col_b, col_c = st.columns(3)
        x_col = col_a.selectbox("X Axis", numeric_cols, index=0)
        y_col = col_b.selectbox("Y Axis", numeric_cols, index=min(1, len(numeric_cols)-1))
        chart_type = col_c.selectbox("Chart Type", ["Scatter", "Bar", "Box", "Histogram", "Line"])

        color_col = st.selectbox("Color by", ["None"] + cat_cols)
        color_arg = None if color_col == "None" else color_col

        sample = df.sample(min(2000, len(df)))
        if chart_type == "Scatter":
            fig = px.scatter(sample, x=x_col, y=y_col, color=color_arg, opacity=0.6)
        elif chart_type == "Bar":
            fig = px.bar(sample, x=x_col, y=y_col, color=color_arg)
        elif chart_type == "Box":
            fig = px.box(sample, x=color_arg, y=y_col, color=color_arg)
        elif chart_type == "Histogram":
            fig = px.histogram(sample, x=x_col, color=color_arg, nbins=40, barmode="overlay")
        else:
            fig = px.line(df.groupby(x_col)[y_col].mean().reset_index(), x=x_col, y=y_col)

        fig = styled_chart(fig, f"{chart_type}: {x_col} vs {y_col}")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with st.expander("📋 Raw Data Preview"):
            st.dataframe(df.head(200), use_container_width=True)

# ==========================================
# 3. AI CHAT
# ==========================================
elif menu == "🧠 AI Chat":
    st.markdown("# AI Data Chat")
    st.markdown('<p style="color:#6B7280;font-family:DM Sans;margin-top:-10px">Ask anything about your data in plain English</p>', unsafe_allow_html=True)

    # Build context summary for AI
    hi = len(df[df["segment"] == "High Intent"])
    mi = len(df[df["segment"] == "Medium Intent"])
    lo = len(df[df["segment"] == "Low Intent"])
    conv = len(df[df["order_value"] > 0])
    revenue = df["order_value"].sum()
    top_src = df["traffic_source"].value_counts().idxmax() if "traffic_source" in df.columns else "N/A"
    mobile_pct = (df["device"].str.lower() == "mobile").mean() * 100 if "device" in df.columns else 0
    avg_intent = df["intent_score"].mean()

    DATA_CONTEXT = f"""
You are BearCart Intelligence AI — an expert e-commerce data analyst assistant embedded in an analytics dashboard.

CURRENT DATASET SUMMARY:
- Total sessions: {len(df):,}
- High Intent users: {hi:,} ({hi/len(df)*100:.1f}%)
- Medium Intent users: {mi:,} ({mi/len(df)*100:.1f}%)
- Low Intent users: {lo:,} ({lo/len(df)*100:.1f}%)
- Total conversions (orders placed): {conv:,}
- Conversion rate: {conv/len(df)*100:.1f}%
- Total revenue: ₹{revenue:,.0f}
- Top traffic source: {top_src}
- Mobile share: {mobile_pct:.0f}%
- Average intent score: {avg_intent:.1f}
- Available columns: {', '.join(df.columns.tolist())}

Key principles from the FDS curriculum this app implements:
1. Know your audience — segment by intent, device, location
2. Simplify complexity — clear charts, no clutter
3. Choose the right chart type — funnels, scatter, heatmaps
4. Clear & descriptive titles
5. Label clearly — all axes and data points labelled
6. Colour wisely — consistent blue palette
7. Consistent formatting — DM Sans throughout
8. Provide context — benchmarks and deltas on KPIs
9. Interactive elements — explorer tab, filters
10. Data integrity — columns validated and normalized
11. Balance detail & simplicity
12. Tell a story — narrative under each section
13. Responsive design — wide layout, sidebar
14. Seek feedback — AI chat for analysis

Answer questions clearly, concisely, and with data-backed reasoning. Be direct and insightful.
When relevant, suggest specific action items based on the data.
"""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown('<div class="section-header" style="margin-top:16px">Quick Questions</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    quick_q = None
    if q1.button("Why is conversion low?", use_container_width=True): quick_q = "Why is my conversion rate low and what should I do?"
    if q2.button("Best traffic source?", use_container_width=True): quick_q = "Which traffic source has the highest quality users?"
    if q3.button("Mobile vs Desktop?", use_container_width=True): quick_q = "Compare mobile vs desktop user behaviour and revenue"
    if q4.button("Retention strategy?", use_container_width=True): quick_q = "What retention strategy do you recommend based on this data?"

    # Input
    user_input = st.text_input("Ask anything about your data...", value=quick_q or "", placeholder="e.g. Why is mobile traffic high but revenue low?")

    if st.button("Send →") and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        messages = [{"role": "user", "content": DATA_CONTEXT + "\n\nUser: " + user_input}]
        for h in st.session_state.chat_history[-6:]:
            messages.append({"role": h["role"], "content": h["content"]})

        with st.spinner("Analysing..."):
            try:
                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1000,
                        "messages": messages
                    },
                    timeout=30
                )
                answer = resp.json()["content"][0]["text"]
            except Exception as e:
                answer = f"⚠️ Could not reach AI API. Error: {str(e)}"

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ==========================================
# 4. ACTION CENTER
# ==========================================
elif menu == "⚡ Action Center":
    st.markdown("# Action Center")
    st.markdown('<p style="color:#6B7280;font-family:DM Sans;margin-top:-10px">Automated marketing actions powered by your data</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📱 WhatsApp Alerts", "🎟️ Coupon Generator", "💰 Ad Budget Optimizer"])

    with tab1:
        st.markdown("### Principle 12 — Tell a Story")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Reach high-intent users who haven\'t converted yet with a personalised WhatsApp message.</p>', unsafe_allow_html=True)

        hi_users = df[(df["segment"] == "High Intent") & (df["order_value"] == 0)]
        st.markdown(f"""
        <div class="card">
        <span class="tag tag-blue">{len(hi_users):,} users</span> are high intent but haven't purchased yet.<br>
        <span style="font-size:0.85rem;color:#6B7280">Potential revenue if 20% convert: ₹{hi_users['potential_revenue'].sum() * 0.2:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

        template = st.selectbox("Message Template", [
            "Low Stock Alert — Urgent",
            "Exclusive Discount for You",
            "You Left Items in Your Cart",
            "Custom Message"
        ])

        templates = {
            "Low Stock Alert — Urgent": "🚨 Hurry! Items you viewed are almost sold out. Secure yours now before they're gone! Shop now at bearcart.in 🐻",
            "Exclusive Discount for You": "🎁 We've got something special just for you! Use code BEAR15 for 15% off your next order. Valid 24 hrs only.",
            "You Left Items in Your Cart": "👋 Hey! You left something in your cart. Your items are waiting — complete your order now at bearcart.in",
        }

        message = st.text_area(
            "Message",
            value=templates.get(template, "Type your custom message here..."),
            height=100
        )

        phone = st.text_input("Test Phone Number (with country code)", placeholder="+91 9876543210")

        if st.button("🚀 Launch WhatsApp Campaign"):
            encoded = urllib.parse.quote(message)
            number = phone.replace(" ", "").replace("+", "") if phone else ""
            if number:
                link = f"https://wa.me/{number}?text={encoded}"
            else:
                link = f"https://wa.me/?text={encoded}"
            st.markdown(f'<a href="{link}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:10px 24px;border-radius:8px;font-family:DM Sans;font-weight:600;cursor:pointer;font-size:0.9rem">📱 Open WhatsApp</button></a>', unsafe_allow_html=True)
            st.success(f"✅ Message ready for {len(hi_users):,} high-intent users.")

    with tab2:
        st.markdown("### Neon Coupon Generator")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Mint unique, trackable discount codes for target segments.</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        segment_target = col1.selectbox("Target Segment", ["High Intent", "Medium Intent", "Low Intent", "All"])
        discount_pct = col2.slider("Discount %", 5, 50, 15)
        expiry_days = col3.slider("Expiry (days)", 1, 30, 7)

        if st.button("✨ Generate Coupon Code"):
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            seg_prefix = {"High Intent": "VIP", "Medium Intent": "MID", "Low Intent": "WIN", "All": "BEAR"}
            code = f"{seg_prefix.get(segment_target, 'BEAR')}{discount_pct}-{suffix}"
            expiry = (datetime.now() + timedelta(days=expiry_days)).strftime("%d %b %Y")

            target_count = len(df[df["segment"] == segment_target]) if segment_target != "All" else len(df)
            est_revenue = target_count * 0.1 * avg_order if "avg_order" in dir() else target_count * 0.1 * 150

            st.markdown(f'<div class="coupon-box">🎟️ {code}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="margin-top:12px">
            <span class="tag tag-green">{discount_pct}% Off</span>
            <span class="tag tag-blue" style="margin-left:6px">{segment_target}</span>
            <span class="tag tag-amber" style="margin-left:6px">Expires {expiry}</span><br><br>
            📊 Target users: <b>{target_count:,}</b><br>
            💰 Est. revenue if 10% redeem: <b>₹{est_revenue:,.0f}</b>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### Ad Budget Optimizer")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Stop wasting ad spend on low-intent window shoppers.</p>', unsafe_allow_html=True)

        daily_budget = st.number_input("Current Daily Ad Budget (₹)", value=5000, step=500)

        lo_users = df[df["segment"] == "Low Intent"]
        lo_pct = len(lo_users) / len(df)
        waste = daily_budget * lo_pct
        optimized = daily_budget - waste
        monthly_saving = waste * 30

        col1, col2, col3 = st.columns(3)
        col1.metric("Wasted on Low Intent", f"₹{waste:,.0f}/day", delta=f"-{lo_pct*100:.0f}% of budget", delta_color="inverse")
        col2.metric("Optimized Budget", f"₹{optimized:,.0f}/day", delta="Focused spend")
        col3.metric("Monthly Saving", f"₹{monthly_saving:,.0f}", delta="Recovered")

        fig = go.Figure(go.Waterfall(
            name="Budget Flow",
            orientation="v",
            measure=["absolute", "relative", "total"],
            x=["Current Budget", "Remove Low-Intent Waste", "Optimized Budget"],
            y=[daily_budget, -waste, 0],
            connector=dict(line=dict(color="#E4E7EC")),
            decreasing=dict(marker=dict(color="#DC2626")),
            increasing=dict(marker=dict(color="#059669")),
            totals=dict(marker=dict(color="#2563EB")),
        ))
        fig = styled_chart(fig, "Ad Budget Waterfall — Where Money Goes")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ==========================================
# 5. FUTURE LAB
# ==========================================
elif menu == "🔮 Future Lab":
    st.markdown("# Future Lab")
    st.markdown('<p style="color:#6B7280;font-family:DM Sans;margin-top:-10px">Predictive analytics, forecasting & customer sentiment</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Revenue Forecast", "😊 Sentiment Speedometer", "🎯 Predictive Scoring"])

    with tab1:
        st.markdown("### Principle 11 — Balance Detail & Simplicity")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Next 14-day revenue forecast with confidence intervals using trend extrapolation.</p>', unsafe_allow_html=True)

        forecast_days = st.slider("Forecast Horizon (days)", 7, 30, 14)

        # Build a historical base from data
        if "month" in df.columns and df["order_value"].sum() > 0:
            base_daily = df["order_value"].sum() / max(1, df["created_at"].nunique())
        else:
            base_daily = 5000

        np.random.seed(99)
        days_hist = 30
        hist_dates = [datetime.now() - timedelta(days=days_hist-i) for i in range(days_hist)]
        hist_rev = base_daily * (1 + 0.1*np.sin(np.arange(days_hist)*0.4)) + np.random.normal(0, base_daily*0.08, days_hist)

        fut_dates = [datetime.now() + timedelta(days=i+1) for i in range(forecast_days)]
        trend = 1.015
        fut_rev = [hist_rev[-1] * (trend**i) * (1 + 0.08*np.sin(i*0.4)) for i in range(1, forecast_days+1)]
        upper = [v * 1.18 for v in fut_rev]
        lower = [v * 0.82 for v in fut_rev]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_dates, y=hist_rev, name="Historical",
            line=dict(color="#2563EB", width=2),
            hovertemplate="%{x|%d %b}<br>₹%{y:,.0f}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=fut_dates + fut_dates[::-1],
            y=upper + lower[::-1],
            fill="toself", fillcolor="rgba(37,99,235,0.08)",
            line=dict(color="rgba(0,0,0,0)"), name="Confidence Band", showlegend=True
        ))
        fig.add_trace(go.Scatter(
            x=fut_dates, y=fut_rev, name="Forecast",
            line=dict(color="#059669", width=2.5, dash="dot"),
            hovertemplate="%{x|%d %b}<br>Forecast: ₹%{y:,.0f}<extra></extra>"
        ))
        fig = styled_chart(fig, f"Revenue Forecast — Next {forecast_days} Days")
        fig.add_vline(x=datetime.now(), line_dash="dash", line_color="#D97706", annotation_text="Today")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        k1, k2, k3 = st.columns(3)
        k1.metric("7-day Forecast", f"₹{sum(fut_rev[:7]):,.0f}")
        k2.metric("14-day Forecast", f"₹{sum(fut_rev[:14]):,.0f}")
        k3.metric("Growth Rate", "+1.5%/day", delta="Upward trend")

    with tab2:
        st.markdown("### Customer Sentiment Speedometer")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Real-time happiness index derived from intent scores and conversion patterns.</p>', unsafe_allow_html=True)

        conv_rate = len(df[df["order_value"] > 0]) / len(df) * 100
        hi_pct = len(df[df["segment"] == "High Intent"]) / len(df) * 100
        avg_intent_norm = df["intent_score"].mean() / df["intent_score"].max() * 100
        sentiment_score = (conv_rate * 0.4 + hi_pct * 0.3 + avg_intent_norm * 0.3)

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(sentiment_score, 1),
            delta={"reference": 45, "valueformat": ".1f"},
            title={"text": "Customer Sentiment Index", "font": {"family": "DM Sans", "size": 16}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"family": "DM Sans"}},
                "bar": {"color": "#2563EB", "thickness": 0.25},
                "steps": [
                    {"range": [0, 33], "color": "#FEE2E2"},
                    {"range": [33, 66], "color": "#FEF3C7"},
                    {"range": [66, 100], "color": "#D1FAE5"},
                ],
                "threshold": {"line": {"color": "#DC2626", "width": 3}, "value": 33},
            },
            number={"font": {"family": "DM Mono", "size": 40}, "suffix": " / 100"}
        ))
        fig.update_layout(
            paper_bgcolor="white", font=dict(family="DM Sans"),
            margin=dict(l=40, r=40, t=20, b=20), height=320
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        label = "🟢 Positive" if sentiment_score > 66 else ("🟡 Neutral" if sentiment_score > 33 else "🔴 Needs Attention")
        st.markdown(f"""
        <div class="card" style="text-align:center">
        <div style="font-size:1.4rem;font-weight:700">{label}</div>
        <div style="color:#6B7280;font-size:0.9rem;margin-top:4px">
        Conv. Rate {conv_rate:.1f}% · High Intent {hi_pct:.0f}% · Intent Index {avg_intent_norm:.0f}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### Predictive User Scoring")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Top users ranked by conversion probability for immediate outreach.</p>', unsafe_allow_html=True)

        # Score users
        scored = df.copy()
        scored["conv_prob"] = (
            scored["intent_score"] / scored["intent_score"].max() * 0.6 +
            scored["add_to_cart"] / max(1, scored["add_to_cart"].max()) * 0.3 +
            scored["is_repeat_session"] * 0.1
        ).clip(0, 1)
        scored["conv_prob_pct"] = (scored["conv_prob"] * 100).round(1)

        top_users = scored[scored["segment"] == "High Intent"].nlargest(20, "conv_prob_pct")[
            ["session_id", "device", "pages_viewed", "product_views", "add_to_cart", "intent_score", "conv_prob_pct"]
        ].reset_index(drop=True)
        top_users.columns = ["Session ID", "Device", "Pages", "Products Viewed", "Add to Cart", "Intent Score", "Conv. Prob %"]

        st.dataframe(top_users, use_container_width=True, hide_index=True)

        fig = px.histogram(scored, x="conv_prob_pct", color="segment",
                           color_discrete_map=SEG_COLORS, nbins=30,
                           barmode="overlay", opacity=0.75,
                           labels={"conv_prob_pct": "Conversion Probability %"})
        fig = styled_chart(fig, "Conversion Probability Distribution")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ==========================================
# 6. DATA LAB — UPLOAD + CLEAN + ANALYSE
# ==========================================
elif menu == "🧹 Data Lab":
    st.markdown("# Data Lab")
    st.markdown('<p style="color:#6B7280;font-family:DM Sans;margin-top:-10px">Upload any CSV · auto-clean it · explore the result</p>', unsafe_allow_html=True)

    # ── CLEANING ENGINE ──────────────────────────────────────
    def run_cleaning_pipeline(raw_df):
        log = []
        df_clean = raw_df.copy()
        original_shape = df_clean.shape

        # 1. Normalise column names
        old_cols = df_clean.columns.tolist()
        df_clean.columns = (
            df_clean.columns
            .str.strip()
            .str.lower()
            .str.replace(r"[\s\-/]+", "_", regex=True)
            .str.replace(r"[^\w]", "", regex=True)
        )
        renamed = [(o, n) for o, n in zip(old_cols, df_clean.columns) if o != n]
        if renamed:
            log.append(("info", f"Normalised {len(renamed)} column name(s): {', '.join(f'{o}→{n}' for o,n in renamed[:5])}{'…' if len(renamed)>5 else ''}"))

        # 2. Drop fully empty columns
        empty_cols = [c for c in df_clean.columns if df_clean[c].isna().all()]
        if empty_cols:
            df_clean.drop(columns=empty_cols, inplace=True)
            log.append(("warning", f"Dropped {len(empty_cols)} fully-empty column(s): {', '.join(empty_cols)}"))

        # 3. Drop fully empty rows
        empty_rows_before = len(df_clean)
        df_clean.dropna(how="all", inplace=True)
        dropped_empty = empty_rows_before - len(df_clean)
        if dropped_empty:
            log.append(("warning", f"Removed {dropped_empty:,} fully-empty row(s)"))

        # 4. Duplicate detection & removal
        dupe_count = df_clean.duplicated().sum()
        if dupe_count:
            df_clean.drop_duplicates(inplace=True)
            log.append(("warning", f"Removed {dupe_count:,} exact duplicate row(s)"))
        else:
            log.append(("success", "No exact duplicates found"))

        # 5. Smart type inference — parse dates
        for col in df_clean.columns:
            if df_clean[col].dtype == object:
                sample = df_clean[col].dropna().head(50).astype(str)
                date_patterns = [r"\d{4}-\d{2}-\d{2}", r"\d{2}/\d{2}/\d{4}", r"\d{2}-\d{2}-\d{4}"]
                if any(sample.str.match(p).mean() > 0.6 for p in date_patterns):
                    try:
                        df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")
                        log.append(("info", f"Parsed '{col}' as datetime"))
                    except Exception:
                        pass

        # 6. Numeric coercion — strip currency/percent symbols
        for col in df_clean.select_dtypes("object").columns:
            sample = df_clean[col].dropna().head(100).astype(str)
            cleaned_sample = sample.str.replace(r"[₹$€£,%\s]", "", regex=True)
            numeric_ratio = pd.to_numeric(cleaned_sample, errors="coerce").notna().mean()
            if numeric_ratio > 0.8:
                df_clean[col] = pd.to_numeric(
                    df_clean[col].astype(str).str.replace(r"[₹$€£,%\s]", "", regex=True),
                    errors="coerce"
                )
                log.append(("info", f"Coerced '{col}' to numeric (stripped symbols)"))

        # 7. Whitespace trimming on remaining string columns
        str_cols = df_clean.select_dtypes("object").columns.tolist()
        if str_cols:
            df_clean[str_cols] = df_clean[str_cols].apply(lambda s: s.str.strip() if s.dtype == object else s)
            log.append(("info", f"Trimmed whitespace in {len(str_cols)} string column(s)"))

        # 8. Per-column null analysis & imputation
        null_report = []
        for col in df_clean.columns:
            n_null = df_clean[col].isna().sum()
            if n_null == 0:
                continue
            pct = n_null / len(df_clean) * 100
            dtype = df_clean[col].dtype

            if pct > 60:
                df_clean.drop(columns=[col], inplace=True)
                null_report.append((col, n_null, pct, "dropped — >60% missing"))
                log.append(("warning", f"Dropped column '{col}' — {pct:.0f}% missing values"))
            elif dtype in [np.float64, np.int64, float, int] or pd.api.types.is_numeric_dtype(df_clean[col]):
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                null_report.append((col, n_null, pct, f"filled with median ({median_val:.2f})"))
            elif pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                df_clean[col].fillna(method="ffill", inplace=True)
                null_report.append((col, n_null, pct, "forward-filled (datetime)"))
            else:
                mode_val = df_clean[col].mode()
                fill_val = mode_val[0] if len(mode_val) > 0 else "Unknown"
                df_clean[col].fillna(fill_val, inplace=True)
                null_report.append((col, n_null, pct, f"filled with mode ('{fill_val}')"))

        if null_report:
            log.append(("warning", f"Handled nulls in {len(null_report)} column(s) — see Null Report below"))
        else:
            log.append(("success", "No missing values detected"))

        # 9. Outlier flagging (IQR method) — flag, don't remove
        outlier_summary = {}
        for col in df_clean.select_dtypes(include=np.number).columns:
            q1 = df_clean[col].quantile(0.25)
            q3 = df_clean[col].quantile(0.75)
            iqr = q3 - q1
            if iqr == 0:
                continue
            lower_b = q1 - 3 * iqr
            upper_b = q3 + 3 * iqr
            outliers = ((df_clean[col] < lower_b) | (df_clean[col] > upper_b)).sum()
            if outliers > 0:
                outlier_summary[col] = {"count": int(outliers), "lower": round(lower_b, 2), "upper": round(upper_b, 2)}
        if outlier_summary:
            log.append(("info", f"Flagged outliers in {len(outlier_summary)} numeric column(s) — see Outlier Report"))

        # 10. Cardinality check — flag high-cardinality string cols
        high_card = []
        for col in df_clean.select_dtypes("object").columns:
            u = df_clean[col].nunique()
            if u > 0.9 * len(df_clean) and u > 50:
                high_card.append(col)
        if high_card:
            log.append(("info", f"High-cardinality columns (may be IDs, not categories): {', '.join(high_card)}"))

        final_shape = df_clean.shape
        rows_removed = original_shape[0] - final_shape[0]
        cols_removed = original_shape[1] - final_shape[1]
        log.append(("success", f"Pipeline complete — {rows_removed:,} rows and {cols_removed} columns removed. Final shape: {final_shape[0]:,} rows × {final_shape[1]} cols"))

        return df_clean, log, null_report, outlier_summary

    # ── UI ───────────────────────────────────────────────────
    tab_upload, tab_clean, tab_explore = st.tabs(["📂 Upload", "🧹 Clean Report", "🔬 Explore Data"])

    with tab_upload:
        st.markdown("### Upload your dataset")
        st.markdown('<p style="font-family:DM Sans;color:#6B7280;font-size:0.9rem">Supports any CSV file. The cleaning pipeline will run automatically.</p>', unsafe_allow_html=True)

        lab_file = st.file_uploader("Drop your CSV here", type=["csv"], key="lab_upload")

        if lab_file:
            raw_bytes = lab_file.read()
            # Try multiple encodings
            for enc in ["utf-8", "latin-1", "cp1252"]:
                try:
                    raw_df = pd.read_csv(io.BytesIO(raw_bytes), encoding=enc)
                    break
                except Exception:
                    continue

            st.session_state["lab_raw"] = raw_df
            st.success(f"✅ File loaded — {raw_df.shape[0]:,} rows × {raw_df.shape[1]} columns")

            # Quick raw preview
            st.markdown("#### Raw data preview (first 10 rows)")
            st.dataframe(raw_df.head(10), use_container_width=True)

            # Raw stats
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Rows", f"{raw_df.shape[0]:,}")
            c2.metric("Columns", f"{raw_df.shape[1]}")
            c3.metric("Missing values", f"{raw_df.isna().sum().sum():,}")
            c4.metric("Duplicates", f"{raw_df.duplicated().sum():,}")

            st.markdown("#### Column overview")
            col_info = pd.DataFrame({
                "Column": raw_df.columns,
                "Type": raw_df.dtypes.astype(str).values,
                "Non-Null": raw_df.notna().sum().values,
                "Null": raw_df.isna().sum().values,
                "Null %": (raw_df.isna().sum() / len(raw_df) * 100).round(1).values,
                "Unique": raw_df.nunique().values,
                "Sample": [str(raw_df[c].dropna().iloc[0]) if raw_df[c].notna().any() else "—" for c in raw_df.columns]
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)

            if st.button("🚀 Run Cleaning Pipeline"):
                with st.spinner("Scanning and cleaning..."):
                    cleaned_df, log, null_report, outlier_summary = run_cleaning_pipeline(raw_df)
                st.session_state["lab_cleaned"] = cleaned_df
                st.session_state["lab_log"] = log
                st.session_state["lab_null"] = null_report
                st.session_state["lab_outliers"] = outlier_summary
                st.success("✅ Cleaning complete! Switch to the Clean Report tab.")
        else:
            st.markdown("""
            <div class="card" style="text-align:center;padding:40px">
            <div style="font-size:2rem;margin-bottom:12px">📂</div>
            <div style="font-size:1rem;font-weight:600;color:#111827">No file uploaded yet</div>
            <div style="font-size:0.85rem;color:#6B7280;margin-top:6px">Upload a CSV above to begin. The pipeline will handle nulls, duplicates,<br>type coercion, outlier detection, and whitespace cleaning automatically.</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_clean:
        if "lab_cleaned" not in st.session_state:
            st.info("Upload a file and run the pipeline first (Upload tab).")
        else:
            cleaned_df = st.session_state["lab_cleaned"]
            raw_df = st.session_state["lab_raw"]
            log = st.session_state["lab_log"]
            null_report = st.session_state["lab_null"]
            outlier_summary = st.session_state["lab_outliers"]

            st.markdown("### Cleaning pipeline report")

            # Before vs After KPIs
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Rows before", f"{raw_df.shape[0]:,}")
            c2.metric("Rows after", f"{cleaned_df.shape[0]:,}", delta=f"-{raw_df.shape[0]-cleaned_df.shape[0]:,}")
            c3.metric("Cols before", f"{raw_df.shape[1]}")
            c4.metric("Cols after", f"{cleaned_df.shape[1]}", delta=f"-{raw_df.shape[1]-cleaned_df.shape[1]}")
            c5.metric("Nulls removed", f"{raw_df.isna().sum().sum():,}", delta_color="inverse")

            st.markdown("---")
            st.markdown("#### Step-by-step log")
            icon_map = {"success": "✅", "warning": "⚠️", "info": "ℹ️"}
            color_map = {"success": "#D1FAE5", "warning": "#FEF3C7", "info": "#EFF6FF"}
            text_map  = {"success": "#065F46", "warning": "#92400E", "info": "#1E3A8A"}
            for level, msg in log:
                st.markdown(f"""
                <div style="background:{color_map[level]};border-radius:8px;padding:8px 14px;margin:4px 0;font-family:DM Sans;font-size:0.85rem;color:{text_map[level]}">
                {icon_map[level]} {msg}
                </div>""", unsafe_allow_html=True)

            # Null report table
            if null_report:
                st.markdown("---")
                st.markdown("#### Null value report")
                null_df = pd.DataFrame(null_report, columns=["Column", "Null Count", "Null %", "Action Taken"])
                null_df["Null %"] = null_df["Null %"].round(1).astype(str) + "%"
                st.dataframe(null_df, use_container_width=True, hide_index=True)

                # Null heatmap
                if len(null_df) > 0:
                    null_vals = [float(r[2]) for r in null_report]
                    null_cols = [r[0] for r in null_report]
                    fig_null = go.Figure(go.Bar(
                        x=null_vals, y=null_cols, orientation="h",
                        marker=dict(
                            color=null_vals,
                            colorscale=[[0,"#FEF3C7"],[0.5,"#F59E0B"],[1,"#DC2626"]]
                        ),
                        hovertemplate="%{y}: <b>%{x:.1f}%</b> missing<extra></extra>"
                    ))
                    fig_null = styled_chart(fig_null, "Missing value % by column")
                    fig_null.update_layout(yaxis=dict(categoryorder="total ascending"))
                    st.plotly_chart(fig_null, use_container_width=True, config={"displayModeBar": False})

            # Outlier report
            if outlier_summary:
                st.markdown("---")
                st.markdown("#### Outlier report (IQR × 3 method — flagged, not removed)")
                out_rows = []
                for col, info in outlier_summary.items():
                    out_rows.append({
                        "Column": col,
                        "Outlier Count": info["count"],
                        "Safe Lower Bound": info["lower"],
                        "Safe Upper Bound": info["upper"],
                        "Action": "Flagged only — review manually"
                    })
                st.dataframe(pd.DataFrame(out_rows), use_container_width=True, hide_index=True)

                # Outlier bar chart
                fig_out = go.Figure(go.Bar(
                    x=[r["Column"] for r in out_rows],
                    y=[r["Outlier Count"] for r in out_rows],
                    marker_color="#7C3AED",
                    hovertemplate="%{x}: <b>%{y}</b> outliers<extra></extra>"
                ))
                fig_out = styled_chart(fig_out, "Outlier count by column")
                st.plotly_chart(fig_out, use_container_width=True, config={"displayModeBar": False})

            # Download clean CSV
            st.markdown("---")
            st.markdown("#### Download cleaned dataset")
            csv_out = cleaned_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download clean CSV",
                data=csv_out,
                file_name=f"bearcart_cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with tab_explore:
        explore_df = st.session_state.get("lab_cleaned", st.session_state.get("lab_raw", None))

        if explore_df is None:
            st.info("Upload a file first (Upload tab). You can explore before or after cleaning.")
        else:
            st.markdown("### Explore your data")
            is_clean = "lab_cleaned" in st.session_state
            st.markdown(f'<span class="tag {"tag-green" if is_clean else "tag-amber"}">{"Cleaned dataset" if is_clean else "Raw dataset (run pipeline for best results)"}</span><br><br>', unsafe_allow_html=True)

            num_cols = explore_df.select_dtypes(include=np.number).columns.tolist()
            cat_cols = explore_df.select_dtypes("object").columns.tolist()
            date_cols = explore_df.select_dtypes("datetime").columns.tolist()
            all_cols = explore_df.columns.tolist()

            # ── Summary statistics
            st.markdown("#### Descriptive statistics")
            if num_cols:
                desc = explore_df[num_cols].describe().round(3)
                st.dataframe(desc, use_container_width=True)

            st.markdown("---")

            # ── Distribution explorer
            st.markdown("#### Distribution explorer")
            col_a, col_b = st.columns(2)
            sel_col = col_a.selectbox("Select column", all_cols, key="explore_dist_col")
            chart_type = col_b.selectbox("Chart type", ["Histogram", "Box Plot", "Bar (categorical)", "Line (if datetime)"], key="explore_chart_type")

            color_col = st.selectbox("Color by (optional)", ["None"] + cat_cols, key="explore_color")
            color_arg = None if color_col == "None" else color_col

            sample = explore_df.sample(min(5000, len(explore_df)), random_state=42)

            if chart_type == "Histogram" and explore_df[sel_col].dtype != object:
                fig_exp = px.histogram(sample, x=sel_col, color=color_arg, nbins=40, barmode="overlay", opacity=0.75)
            elif chart_type == "Box Plot" and explore_df[sel_col].dtype != object:
                fig_exp = px.box(sample, x=color_arg, y=sel_col, color=color_arg)
            elif chart_type == "Bar (categorical)":
                vc = explore_df[sel_col].value_counts().head(30).reset_index()
                vc.columns = [sel_col, "Count"]
                fig_exp = px.bar(vc, x=sel_col, y="Count", color=sel_col)
            elif chart_type == "Line (if datetime)" and explore_df[sel_col].dtype != object:
                ts = explore_df.sort_values(date_cols[0]) if date_cols else explore_df
                fig_exp = px.line(ts, x=ts.index, y=sel_col)
            else:
                vc = explore_df[sel_col].value_counts().head(30).reset_index()
                vc.columns = [sel_col, "Count"]
                fig_exp = px.bar(vc, x=sel_col, y="Count")

            fig_exp = styled_chart(fig_exp, f"Distribution of '{sel_col}'")
            st.plotly_chart(fig_exp, use_container_width=True, config={"displayModeBar": False})

            # ── Correlation heatmap
            if len(num_cols) >= 2:
                st.markdown("---")
                st.markdown("#### Correlation matrix")
                corr = explore_df[num_cols].corr().round(2)
                fig_corr = go.Figure(go.Heatmap(
                    z=corr.values,
                    x=corr.columns.tolist(),
                    y=corr.columns.tolist(),
                    colorscale=[[0,"#FEE2E2"],[0.5,"#F3F4F6"],[1,"#DBEAFE"]],
                    zmin=-1, zmax=1,
                    text=corr.values.round(2),
                    texttemplate="%{text}",
                    hovertemplate="%{x} × %{y}: <b>%{z}</b><extra></extra>"
                ))
                fig_corr.update_layout(
                    paper_bgcolor="white", font=dict(family="DM Sans", size=10),
                    margin=dict(l=10,r=10,t=40,b=10),
                    title=dict(text="Correlation matrix (numeric columns)", font=dict(size=15,weight=700), x=0)
                )
                st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

            # ── Scatter explorer
            if len(num_cols) >= 2:
                st.markdown("---")
                st.markdown("#### Scatter explorer")
                s1, s2, s3 = st.columns(3)
                x_s = s1.selectbox("X axis", num_cols, key="sc_x")
                y_s = s2.selectbox("Y axis", num_cols, index=min(1, len(num_cols)-1), key="sc_y")
                c_s = s3.selectbox("Color by", ["None"] + cat_cols, key="sc_c")
                fig_sc = px.scatter(
                    sample, x=x_s, y=y_s,
                    color=None if c_s == "None" else c_s,
                    opacity=0.55, trendline="ols" if len(sample) < 3000 else None
                )
                fig_sc = styled_chart(fig_sc, f"{x_s} vs {y_s}")
                st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

            # ── Category breakdown
            if cat_cols:
                st.markdown("---")
                st.markdown("#### Category breakdown")
                cat_sel = st.selectbox("Pick a categorical column", cat_cols, key="cat_sel")
                top_n = explore_df[cat_sel].value_counts().head(20)
                fig_cat = go.Figure(go.Bar(
                    x=top_n.index.astype(str),
                    y=top_n.values,
                    marker_color="#2563EB",
                    hovertemplate="%{x}: <b>%{y:,}</b><extra></extra>"
                ))
                fig_cat = styled_chart(fig_cat, f"Top values in '{cat_sel}'")
                st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

            # ── Full data table
            st.markdown("---")
            st.markdown("#### Full dataset viewer")
            search = st.text_input("Filter rows (search any value)", placeholder="Type to filter...")
            display_df = explore_df
            if search:
                mask = explore_df.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
                display_df = explore_df[mask]
                st.caption(f"{len(display_df):,} rows match '{search}'")
            st.dataframe(display_df, use_container_width=True, height=350)

# ==========================================
# 7. USE CASES
# ==========================================
elif menu == "▶ Use Cases":
    st.markdown("# Use Cases")
    st.markdown('<p style="color:#6B7280;margin-top:-10px">4 real company scenarios — select one to see how BearCart solved it</p>', unsafe_allow_html=True)

    cases = {
        "🛒 Cart Abandonment Crisis": {
            "company": "E-commerce · Q3 2024",
            "problem": "Despite 14,925 monthly sessions, revenue was plateauing. 1,203 high-intent users were adding to cart but not buying. The team had no visibility into where or why they dropped off.",
            "data": {"Sessions": "14,925", "Add to Cart": "2,239", "Purchased": "1,851", "Conv. Rate": "12.4%", "Est. Lost Revenue": "₹2,10,000"},
            "steps": [
                ("Segment by intent score", "BearCart identified 1,203 High Intent users who viewed 4+ products and spent 8+ mins but didn't buy."),
                ("Time heatmap analysis", "68% of abandonments happened between 8pm–11pm on mobile — users browsing after work."),
                ("Root cause found", "Mobile checkout had 4 steps vs 2 on desktop. 61% bounced at the payment screen."),
                ("WhatsApp campaign", "Launched retargeting to 1,203 users with code BEAR15 within 2 hours of abandonment."),
            ],
            "result": "✅ ₹2,10,000 recovered in 3 weeks. Conv. rate improved 12.4% → 15.1%.",
            "color": "#059669"
        },
        "📉 Traffic Drop Investigation": {
            "company": "Analytics · Feb 2025",
            "problem": "Sessions dropped 34% week-over-week with no change in ad spend. CEO needed root cause within 24 hours.",
            "data": {"Week 1 Sessions": "3,731", "Week 2 Sessions": "2,463", "WoW Change": "-34%", "Google Search Drop": "-52%", "Other Sources": "Stable"},
            "steps": [
                ("Source breakdown", "Traffic Sources chart showed Google Search fell from 1,678 → 806. All other sources flat or up."),
                ("Time heatmap check", "Drop was uniform across all hours — ruling out technical outage, pointing to ranking change."),
                ("Segment impact", "High Intent users dropped 41% — mostly Google Search arrivals. Revenue impact disproportionate."),
                ("Diagnosis", "Google core algorithm update confirmed. Recommended: boost email, increase Google Ads 30%, fix thin content pages."),
            ],
            "result": "✅ Root cause found in 2 hours. Email compensated 40% of lost traffic within 1 week.",
            "color": "#2563EB"
        },
        "📱 Mobile Revenue Gap": {
            "company": "UX Audit · Q4 2024",
            "problem": "62% of sessions came from mobile, but mobile generated only 31% of revenue. Desktop was converting at 3× the rate.",
            "data": {"Mobile Sessions": "9,253 (62%)", "Mobile Revenue": "₹26,105 (31%)", "Mobile Conv.": "7.1%", "Desktop Conv.": "21.3%", "Revenue Gap": "3.6×"},
            "steps": [
                ("Revenue per session", "Desktop ₹10.24/session vs Mobile ₹2.82/session — 3.6× gap, highest priority fix."),
                ("Behaviour analysis", "Mobile users viewed 1.8 products vs 3.2 desktop. Time on site 4m vs 8m 44s."),
                ("Funnel drop-off", "61% mobile drop at payment step. 14-field form, no UPI/wallet options for Indian users."),
                ("Fix & A/B test", "Checkout: 4 steps → 2 steps. Added PhonePe, GPay, Paytm. Ran A/B test on 50% of traffic."),
            ],
            "result": "✅ Mobile conv. rate 7.1% → 13.8%. ₹18,200 additional monthly mobile revenue.",
            "color": "#7C3AED"
        },
        "🎯 Ad Spend Reallocation": {
            "company": "Marketing · Jan 2025",
            "problem": "₹1,80,000/month ad budget. CMO felt ROAS was weak. BearCart found 30% of spend going to low-intent social traffic that never converted.",
            "data": {"Monthly Budget": "₹1,80,000", "Wasted (Low Intent)": "₹54,000", "Google Conv.": "14%", "Social Conv.": "8%", "Email Conv.": "22%"},
            "steps": [
                ("Segment-source overlap", "Low Intent users arrived from broad Instagram/Facebook audiences. Avg 1.2 pages, then bounced."),
                ("Cost per conversion", "Google ₹210/conv. Social ₹890/conv. Email ₹42/conv. Social was 21× more expensive than email."),
                ("Reallocation", "Cut social 60% (₹32,400 freed). Added ₹12,000 to email. Shifted ₹20,400 to Google branded keywords."),
                ("Coupon targeting", "VIP15 for High Intent, MID10 for Medium Intent — via email only, not social."),
            ],
            "result": "✅ ₹54,000/month recovered. ROAS improved 2.1× → 3.4×. Email list grew 28% in 6 weeks.",
            "color": "#D97706"
        }
    }

    selected = st.selectbox("Select a use case to explore", list(cases.keys()))
    case = cases[selected]

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #E4E7EC;border-radius:12px;padding:20px 24px;margin:12px 0">
        <div style="font-size:13px;font-weight:700;color:#6B7280;margin-bottom:4px">{case['company']}</div>
        <div style="font-size:14px;color:#111827;line-height:1.6;background:#F7F8FA;border-radius:8px;padding:12px 16px;margin-top:8px">{case['problem']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Key data points")
    cols = st.columns(len(case["data"]))
    for col, (k, v) in zip(cols, case["data"].items()):
        col.markdown(f"""
        <div style="background:#fff;border:1px solid #E4E7EC;border-radius:10px;padding:14px 16px;text-align:center">
            <div style="font-size:10px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">{k}</div>
            <div style="font-size:20px;font-weight:800;color:#111827;letter-spacing:-0.5px">{v}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### What the team did — step by step")
    for i, (title, desc) in enumerate(case["steps"], 1):
        st.markdown(f"""
        <div style="display:flex;gap:14px;margin-bottom:12px;align-items:flex-start">
            <div style="width:26px;height:26px;border-radius:50%;background:{case['color']};color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px">{i}</div>
            <div>
                <div style="font-size:13px;font-weight:700;color:#111827">{title}</div>
                <div style="font-size:12px;color:#6B7280;margin-top:3px;line-height:1.5">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#D1FAE5;border:1px solid #6EE7B7;border-radius:10px;padding:16px 20px;margin-top:8px;font-size:14px;font-weight:600;color:#065F46">
        {case['result']}
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-family:DM Sans;font-size:0.8rem;color:#9CA3AF;padding:10px 0">
🐻 BearCart Intelligence · ZeTheta Algorithms Pvt Ltd · CIN U62012MH2023PTC410415 · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
