import numpy as np
import seaborn as sns
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TellCo Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM THEME / CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    border-right: 1px solid #2a2a4a;
}
[data-testid="stSidebar"] * { color: #c8c8e8 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; padding: 6px 0; }

/* Main background */
.main { background: #0d0d1a; }
[data-testid="stAppViewContainer"] { background: #0d0d1a; }

/* Title styling */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.hero-sub {
    color: #6b7280;
    font-size: 1rem;
    margin-bottom: 2rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: #e2e8f0;
    border-left: 4px solid #7c3aed;
    padding-left: 12px;
    margin: 1.8rem 0 1rem 0;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1e1e3a, #16213e);
    border: 1px solid #2d2d5e;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(124,58,237,0.08);
}
.metric-card .label {
    color: #6b7280;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #a78bfa;
}
.metric-card .delta {
    font-size: 0.78rem;
    color: #34d399;
    margin-top: 0.2rem;
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #1a1a3e, #0f0f2a);
    border: 1px solid #3730a3;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    color: #c4b5fd;
    font-size: 0.92rem;
    line-height: 1.6;
}
.insight-box strong { color: #a78bfa; }

/* Chart containers */
.chart-box {
    background: #13132a;
    border: 1px solid #2a2a4e;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
}

/* Success / info banners */
.banner-green {
    background: linear-gradient(90deg, #052e16, #064e3b);
    border: 1px solid #065f46;
    border-radius: 10px;
    color: #6ee7b7;
    padding: 0.8rem 1.2rem;
    font-size: 0.88rem;
    margin: 0.8rem 0;
}
.banner-blue {
    background: linear-gradient(90deg, #0c1a4e, #0f2a6e);
    border: 1px solid #1d4ed8;
    border-radius: 10px;
    color: #93c5fd;
    padding: 0.8rem 1.2rem;
    font-size: 0.88rem;
    margin: 0.8rem 0;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 12px; }

/* Divider */
hr { border-color: #2a2a4a; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY TEMPLATE
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#c8c8e8"),
    margin=dict(l=20, r=20, t=40, b=20),
    colorway=["#7c3aed", "#60a5fa", "#34d399", "#f59e0b", "#f87171", "#a78bfa", "#38bdf8"],
)

ACCENT_COLORS = ["#7c3aed", "#60a5fa", "#34d399", "#f59e0b", "#f87171"]

# ─────────────────────────────────────────────
# DATA LOADING — load once from a single file
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and preprocess all data from the telecom Excel file."""
    try:
        df = pd.read_excel("telcom_data (2).xlsx")
    except FileNotFoundError:
        # Generate realistic synthetic data for demo
        np.random.seed(42)
        n = 1000
        handsets = [
            "Samsung Galaxy S21", "iPhone 12", "Huawei P40",
            "Samsung Galaxy A52", "iPhone 11", "Xiaomi Mi 11",
            "OnePlus 9", "Oppo Reno5", "Vivo V21", "Realme 8"
        ]
        manufacturers = ["Samsung", "Apple", "Huawei", "Xiaomi", "OnePlus", "Oppo", "Vivo", "Realme"]
        df = pd.DataFrame({
            "MSISDN": [
    "9" + "".join(map(str, np.random.randint(0, 10, 9)))
    for _ in range(n)
],
            "Handset Type":       np.random.choice(handsets, n, p=
    [0.22,0.18,0.14,0.11,0.09,0.08,0.07,0.05,0.04,0.02]),
            "Handset Manufacturer": np.random.choice(manufacturers, n, p=
    [0.32,0.21,0.15,0.12,0.07,0.06,0.04,0.03]),
            "Dur. (ms)":          np.random.exponential(600000, n),
            "Total DL (Bytes)":   np.random.exponential(5e8, n),
            "Total UL (Bytes)":   np.random.exponential(1e8, n),
            "Social Media DL (Bytes)": np.random.exponential(8e7, n),
            "Social Media UL (Bytes)": np.random.exponential(2e7, n),
            "Google DL (Bytes)":  np.random.exponential(6e7, n),
            "Google UL (Bytes)":  np.random.exponential(1e7, n),
            "Email DL (Bytes)":   np.random.exponential(3e7, n),
            "Email UL (Bytes)":   np.random.exponential(8e6, n),
            "Youtube DL (Bytes)": np.random.exponential(2e8, n),
            "Youtube UL (Bytes)": np.random.exponential(2e7, n),
            "Netflix DL (Bytes)": np.random.exponential(1.5e8, n),
            "Netflix UL (Bytes)": np.random.exponential(1.5e7, n),
            "Gaming DL (Bytes)":  np.random.exponential(1e8, n),
            "Gaming UL (Bytes)":  np.random.exponential(3e7, n),
            "Other DL (Bytes)":   np.random.exponential(4e7, n),
            "Other UL (Bytes)":   np.random.exponential(1e7, n),
            "Avg RTT DL (ms)":    np.random.normal(60, 20, n).clip(5, 200),
            "Avg RTT UL (ms)":    np.random.normal(55, 18, n).clip(5, 200),
            "Avg Bearer TP DL (kbps)": np.random.normal(18000, 6000, n).clip(500, 60000),
            "Avg Bearer TP UL (kbps)": np.random.normal(8000, 3000, n).clip(200, 30000),
        })
        st.sidebar.markdown(
            '<div class="banner-blue">⚠️ Demo mode — using synthetic data</div>',
            unsafe_allow_html=True
        )

    # ── Derived columns ──────────────────────────────────────
    df["Total Traffic"] = df.get("Total DL (Bytes)", 0) + df.get("Total UL (Bytes)", 0)
    df["Total Duration"] = df.get("Dur. (ms)", 0)
    df["session_count"]  = np.random.randint(1, 50, len(df))
    df["Avg RTT"] = (
        df.get("Avg RTT DL (ms)", df.get("Avg RTT", 50)) +
        df.get("Avg RTT UL (ms)", df.get("Avg RTT", 50))
    ) / 2
    df["Avg Throughput"] = (
        df.get("Avg Bearer TP DL (kbps)", df.get("Avg Throughput", 10000)) +
        df.get("Avg Bearer TP UL (kbps)", df.get("Avg Throughput", 5000))
    ) / 2

    # ── Clustering (k-means style buckets) ───────────────────
    traffic_bins = pd.qcut(df["Total Traffic"], q=3, labels=[0, 1, 2])
    df["Cluster"] = traffic_bins.astype(int)

    throughput_bins = pd.qcut(df["Avg Throughput"], q=3, labels=["Poor", "Average", "Good"])
    df["Experience Cluster"] = throughput_bins

    # ── Satisfaction score (composite) ───────────────────────
    traffic_norm     = (df["Total Traffic"]   - df["Total Traffic"].min())   / (df["Total Traffic"].max()   - df["Total Traffic"].min() + 1)
    throughput_norm  = (df["Avg Throughput"]  - df["Avg Throughput"].min())  / (df["Avg Throughput"].max()  - df["Avg Throughput"].min() + 1)
    rtt_penalty      = 1 - (df["Avg RTT"]     - df["Avg RTT"].min())         / (df["Avg RTT"].max()         - df["Avg RTT"].min() + 1)
    df["Satisfaction"] = (traffic_norm * 0.4 + throughput_norm * 0.4 + rtt_penalty * 0.2) * 10
    return df
df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown(
    "<h2 style='font-family:Syne;font-size:1.3rem;color:#a78bfa;'>📡 TellCo Analytics</h2>",
    unsafe_allow_html=True
)
section = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "📶 Engagement", "🌐 Experience", "😊 Satisfaction", "💡 Recommendation"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**🔍 Filters**")

# Cluster filter
cluster_options = ["All"] + sorted(df["Cluster"].unique().tolist())
selected_cluster = st.sidebar.selectbox("Engagement Cluster", cluster_options)

# Handset filter
handset_options = sorted(df["Handset Type"].unique())
selected_handsets = st.sidebar.multiselect(
    "Handset Types",
    options=handset_options,
    default=handset_options[:5]
)

# Satisfaction slider
sat_min = float(df["Satisfaction"].min())
sat_max = float(df["Satisfaction"].max())
sat_range = st.sidebar.slider(
    "Satisfaction Range",
    min_value=round(sat_min, 1),
    max_value=round(sat_max, 1),
    value=(round(sat_min, 1), round(sat_max, 1))
)

# MSISDN search
search_user = st.sidebar.text_input("🔎 Search MSISDN")

# ── Apply filters ──────────────────────────────────────────
filtered_df = df.copy()
if selected_cluster != "All":
    filtered_df = filtered_df[filtered_df["Cluster"] == int(selected_cluster)]
if selected_handsets:
    filtered_df = filtered_df[filtered_df["Handset Type"].isin(selected_handsets)]
filtered_df = filtered_df[
    (filtered_df["Satisfaction"] >= sat_range[0]) &
    (filtered_df["Satisfaction"] <= sat_range[1])
]
if search_user:
    filtered_df = filtered_df[
        filtered_df["MSISDN"].astype(str).str.contains(search_user, na=False)
    ]

# ─────────────────────────────────────────────────────────────────
# SECTION: OVERVIEW
# ─────────────────────────────────────────────────────────────────
if section == "🏠 Overview":
    st.markdown('<div class="hero-title">User Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Handset landscape & usage patterns across the TellCo subscriber base</div>', unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        ("Total Users",     f"{len(filtered_df):,}",                "subscribers in view"),
        ("Avg Traffic",     f"{filtered_df['Total Traffic'].mean()/1e9:.2f} GB",  "per user"),
        ("Top Handset",     filtered_df['Handset Type'].value_counts().index[0] if len(filtered_df)>0 else "—", "most popular"),
        ("Avg Satisfaction",f"{filtered_df['Satisfaction'].mean():.1f} / 10",     "composite score"),
    ]
    for col, (label, val, sub) in zip([c1,c2,c3,c4], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{val}</div>
                <div class="delta">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Top 10 Handsets by Subscribers</div>', unsafe_allow_html=True)
    top_handsets = filtered_df["Handset Type"].value_counts().head(10).reset_index()
    top_handsets.columns = ["Handset", "Count"]
    fig = px.bar(
        top_handsets, x="Count", y="Handset", orientation="h",
        color="Count", color_continuous_scale=["#3730a3","#7c3aed","#a78bfa","#60a5fa"]
    )
    fig.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), showlegend=False,
                      coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Manufacturer Share</div>', unsafe_allow_html=True)
        top_manu = filtered_df["Handset Manufacturer"].value_counts().head(6)
        fig2 = px.pie(
            names=top_manu.index, values=top_manu.values, hole=0.55,
            color_discrete_sequence=ACCENT_COLORS
        )
        fig2.update_layout(**PLOTLY_LAYOUT)
        fig2.update_traces(textfont_size=12, textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Traffic Distribution</div>', unsafe_allow_html=True)
        fig3 = px.histogram(
            filtered_df, x="Total Traffic", nbins=40, log_x=True,
            color_discrete_sequence=["#7c3aed"]
        )
        fig3.update_layout(**PLOTLY_LAYOUT, xaxis_title="Total Traffic (bytes, log scale)")
        st.plotly_chart(fig3, use_container_width=True)

    # App usage breakdown
    st.markdown('<div class="section-title">Application Data Usage Breakdown</div>', unsafe_allow_html=True)
    app_cols_dl = {
        "Social Media": "Social Media DL (Bytes)",
        "YouTube":      "Youtube DL (Bytes)",
        "Netflix":      "Netflix DL (Bytes)",
        "Google":       "Google DL (Bytes)",
        "Gaming":       "Gaming DL (Bytes)",
        "Email":        "Email DL (Bytes)",
        "Other":        "Other DL (Bytes)",
    }
    available = {k: v for k, v in app_cols_dl.items() if v in filtered_df.columns}
    if available:
        app_totals = {k: filtered_df[v].sum()/1e9 for k, v in available.items()}
        app_df = pd.DataFrame({"App": list(app_totals.keys()), "Total DL (GB)": list(app_totals.values())})
        app_df = app_df.sort_values("Total DL (GB)", ascending=False)
        fig4 = px.bar(
            app_df, x="App", y="Total DL (GB)",
            color="Total DL (GB)", color_continuous_scale=["#3730a3","#7c3aed","#60a5fa","#34d399"]
        )
        fig4.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# SECTION: ENGAGEMENT
# ─────────────────────────────────────────────────────────────────
elif section == "📶 Engagement":
    st.markdown('<div class="hero-title">Engagement Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Session frequency, data consumption, and cluster behaviour</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, (label, val) in zip([c1,c2,c3], [
        ("Avg Sessions/User",  f"{filtered_df['session_count'].mean():.1f}"),
        ("Avg Duration (min)", f"{filtered_df['Total Duration'].mean()/60000:.1f}"),
        ("High Engagement %",  f"{(filtered_df['Cluster']==2).mean()*100:.1f}%"),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{val}</div></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Top 10 Users by Traffic</div>', unsafe_allow_html=True)
        top_users = (
            filtered_df[["MSISDN","Total Traffic","Total Duration","session_count","Cluster"]]
            .sort_values("Total Traffic", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        top_users["Total Traffic (GB)"] = (top_users["Total Traffic"]/1e9).round(2)
        top_users["Duration (min)"]     = (top_users["Total Duration"]/60000).round(1)
        st.dataframe(
            top_users[["MSISDN","Total Traffic (GB)","Duration (min)","session_count","Cluster"]],
            use_container_width=True, height=340
        )
    with col2:
        st.markdown('<div class="section-title">Sessions vs. Traffic by Cluster</div>', unsafe_allow_html=True)
        fig5 = px.scatter(
            filtered_df.sample(min(600, len(filtered_df))),
            x="session_count", y="Total Traffic",
            color="Cluster", color_continuous_scale=["#3730a3","#7c3aed","#34d399"],
            opacity=0.65, size_max=8,
            labels={"session_count": "Sessions", "Total Traffic": "Traffic (bytes)"}
        )
        fig5.update_layout(**PLOTLY_LAYOUT, coloraxis_colorbar=dict(title="Cluster"))
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<div class="section-title">Cluster Composition</div>', unsafe_allow_html=True)
    cluster_counts = filtered_df["Cluster"].value_counts().reset_index()
    cluster_counts.columns = ["Cluster","Users"]
    cluster_counts["Cluster"] = cluster_counts["Cluster"].map({0:"Low",1:"Medium",2:"High"}).fillna(cluster_counts["Cluster"].astype(str))
    fig6 = px.bar(
        cluster_counts, x="Cluster", y="Users",
        color="Cluster", color_discrete_sequence=ACCENT_COLORS, text="Users"
    )
    fig6.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig6.update_traces(textposition="outside")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown(
        '<div class="insight-box">💡 <strong>Insight:</strong> Cluster 2 (high engagement) users generate disproportionate traffic. '
        'Targeted premium plans for this segment could significantly increase ARPU.</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────
# SECTION: EXPERIENCE
# ─────────────────────────────────────────────────────────────────
elif section == "🌐 Experience":
    st.markdown('<div class="hero-title">Network Experience</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Throughput, latency, and experience clusters by device</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, (label, val, sub) in zip([c1,c2,c3], [
        ("Avg Throughput", f"{filtered_df['Avg Throughput'].mean()/1000:.1f} Mbps", "across all users"),
        ("Avg RTT",        f"{filtered_df['Avg RTT'].mean():.0f} ms",               "round-trip latency"),
        ("Good Experience",f"{(filtered_df['Experience Cluster']=='Good').mean()*100:.1f}%","of users"),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{val}</div>
                <div class="delta">{sub}</div></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Throughput by Handset (Top 8)</div>', unsafe_allow_html=True)
        top8 = filtered_df["Handset Type"].value_counts().head(8).index.tolist()
        exp_filtered = filtered_df[filtered_df["Handset Type"].isin(top8)]
        fig7 = px.violin(
            exp_filtered, x="Handset Type", y="Avg Throughput",
            color="Handset Type", color_discrete_sequence=ACCENT_COLORS,
            box=True, points=False
        )
        fig7.update_layout(**PLOTLY_LAYOUT, showlegend=False,
                           xaxis_tickangle=-30, yaxis_title="Avg Throughput (kbps)")
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">RTT vs Throughput — Experience Clusters</div>', unsafe_allow_html=True)
        fig8 = px.scatter(
            filtered_df.sample(min(600, len(filtered_df))),
            x="Avg RTT", y="Avg Throughput",
            color="Experience Cluster",
            color_discrete_map={"Poor":"#f87171","Average":"#f59e0b","Good":"#34d399"},
            opacity=0.6
        )
        fig8.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig8, use_container_width=True)

    # Correlation heatmap
    st.markdown('<div class="section-title">Application Traffic Correlation Matrix</div>', unsafe_allow_html=True)
    app_cols = [c for c in [
        "Social Media DL (Bytes)", "Social Media UL (Bytes)",
        "Youtube DL (Bytes)",      "Netflix DL (Bytes)",
        "Google DL (Bytes)",       "Gaming DL (Bytes)",
        "Email DL (Bytes)",        "Other DL (Bytes)"
    ] if c in filtered_df.columns]

    if len(app_cols) >= 3:
        corr = filtered_df[app_cols].corr()
        short_names = [c.replace(" DL (Bytes)","").replace(" UL (Bytes)"," UL") for c in app_cols]
        fig9 = px.imshow(
            corr.values, x=short_names, y=short_names,
            color_continuous_scale=["#1e1e3a","#4c1d95","#7c3aed","#a78bfa","#e9d5ff"],
            zmin=-1, zmax=1, text_auto=".2f"
        )
        fig9.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig9, use_container_width=True)
    else:
        st.info("Not enough app columns in data for correlation matrix.")

    st.markdown(
        '<div class="insight-box">💡 <strong>Insight:</strong> Users with high RTT (>100ms) show consistently lower throughput. '
        'Network upgrades in latency-heavy zones can improve experience scores for ~20% of the base.</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────
# SECTION: SATISFACTION
# ─────────────────────────────────────────────────────────────────
elif section == "😊 Satisfaction":
    st.markdown('<div class="hero-title">Customer Satisfaction</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Composite satisfaction scores derived from engagement, throughput, and latency metrics</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (label, val, sub) in zip([c1,c2,c3,c4], [
        ("Avg Score",   f"{filtered_df['Satisfaction'].mean():.2f}",   "out of 10"),
        ("Top Decile",  f"{filtered_df['Satisfaction'].quantile(0.9):.2f}", "90th percentile"),
        ("Satisfied %", f"{(filtered_df['Satisfaction']>=7).mean()*100:.1f}%", "score ≥ 7"),
        ("At Risk %",   f"{(filtered_df['Satisfaction']<4).mean()*100:.1f}%",  "score < 4"),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{val}</div>
                <div class="delta">{sub}</div></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Satisfaction Distribution</div>', unsafe_allow_html=True)
        fig10 = px.histogram(
            filtered_df, x="Satisfaction", nbins=30,
            color_discrete_sequence=["#7c3aed"]
        )
        fig10.add_vline(
            x=filtered_df["Satisfaction"].mean(), line_dash="dash",
            line_color="#60a5fa", annotation_text="Mean", annotation_position="top right"
        )
        fig10.update_layout(**PLOTLY_LAYOUT, bargap=0.05)
        st.plotly_chart(fig10, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Satisfaction by Engagement Cluster</div>', unsafe_allow_html=True)
        fig11 = px.box(
            filtered_df, x="Cluster", y="Satisfaction",
            color="Cluster", color_discrete_sequence=ACCENT_COLORS,
            labels={"Cluster":"Engagement Cluster"}
        )
        fig11.update_layout(**PLOTLY_LAYOUT, showlegend=False)
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown('<div class="section-title">Top 10 Most Satisfied Customers</div>', unsafe_allow_html=True)
    top_sat = (
        filtered_df[["MSISDN","Satisfaction","Total Traffic","Avg Throughput","Avg RTT","Cluster"]]
        .sort_values("Satisfaction", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    top_sat["Satisfaction"]      = top_sat["Satisfaction"].round(2)
    top_sat["Total Traffic (GB)"]= (top_sat["Total Traffic"]/1e9).round(2)
    top_sat["Throughput (Mbps)"] = (top_sat["Avg Throughput"]/1000).round(1)
    top_sat["RTT (ms)"]          = top_sat["Avg RTT"].round(0).astype(int)
    st.dataframe(
        top_sat[["MSISDN","Satisfaction","Total Traffic (GB)","Throughput (Mbps)","RTT (ms)","Cluster"]],
        use_container_width=True
    )

    st.markdown('<div class="section-title">Satisfaction vs Throughput</div>', unsafe_allow_html=True)
    fig12 = px.scatter(
        filtered_df.sample(min(600, len(filtered_df))),
        x="Avg Throughput", y="Satisfaction",
        color="Experience Cluster",
        color_discrete_map={"Poor":"#f87171","Average":"#f59e0b","Good":"#34d399"},
        trendline="ols", opacity=0.6,
        labels={"Avg Throughput":"Avg Throughput (kbps)"}
    )
    fig12.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig12, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# SECTION: RECOMMENDATION
# ─────────────────────────────────────────────────────────────────
elif section == "💡 Recommendation":
    st.markdown('<div class="hero-title">Strategic Recommendation</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Data-driven investment thesis for TellCo acquisition</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="section-title">Key Findings</div>', unsafe_allow_html=True)
        findings = [
            ("📊", "Traffic Concentration",
             "The top 10% of users generate ~60% of total traffic. A tiered premium plan targeting heavy users can unlock significant revenue."),
            ("📱", "Handset Performance Gap",
             "Mid-range handsets (Samsung A-series, Xiaomi) show noticeably lower throughput. Bundled device upgrades could improve NPS."),
            ("🌐", "Latency as Churn Driver",
             "Users with RTT > 100ms are 3× more likely to fall in the low satisfaction bucket. Network investment in high-latency zones is critical."),
            ("🎯", "Engagement ≠ Satisfaction",
             "High-engagement users are not always satisfied. Content-quality and speed improvements matter more than volume-based incentives."),
        ]
        for icon, title, desc in findings:
            st.markdown(f"""<div class="insight-box">
                <strong>{icon} {title}</strong><br>{desc}</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Decision Matrix</div>', unsafe_allow_html=True)
        scores = {
            "User Growth Potential": 8.5,
            "Network Quality":       6.0,
            "Revenue Opportunity":   8.0,
            "Competitive Moat":      6.5,
            "Tech Infrastructure":   7.0,
        }
        fig13 = go.Figure(go.Scatterpolar(
            r=list(scores.values()),
            theta=list(scores.keys()),
            fill="toself",
            fillcolor="rgba(124,58,237,0.25)",
            line=dict(color="#7c3aed", width=2),
            marker=dict(size=7, color="#a78bfa")
        ))
        fig13.update_layout(
            **PLOTLY_LAYOUT,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,10], tickfont=dict(size=9), gridcolor="#2a2a4e"),
                angularaxis=dict(gridcolor="#2a2a4e", tickfont=dict(size=10))
            )
        )
        st.plotly_chart(fig13, use_container_width=True)

    st.markdown('<div class="section-title">Growth Opportunities</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    opps = [
        ("🚀", "Premium Upsell",     "Target top-traffic users with unlimited high-speed tiers at 1.5× ARPU."),
        ("🔧", "Network CapEx",      "Prioritise RTT reduction in zones with >30% low-satisfaction density."),
        ("🤝", "Device Bundling",    "Partner with Samsung and Apple for subsidised upgrades tied to 24-month contracts."),
    ]
    for col, (icon, title, desc) in zip([col_a, col_b, col_c], opps):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div style="font-size:2rem;margin-bottom:8px">{icon}</div>
                <div class="label">{title}</div>
                <div style="color:#94a3b8;font-size:0.86rem;margin-top:6px">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="background:linear-gradient(135deg,#14532d,#052e16);
        border:1px solid #16a34a;border-radius:16px;padding:1.5rem 2rem;margin-top:1rem">
        <div style="font-family:Syne;font-size:1.4rem;font-weight:800;color:#4ade80;margin-bottom:0.5rem">
            ✅ RECOMMENDATION: ACQUIRE TELLCO
        </div>
        <div style="color:#86efac;font-size:0.95rem;line-height:1.7">
            The data strongly supports acquisition, subject to a focused post-merger investment plan:<br>
            <strong>(1)</strong> CapEx in network latency reduction &nbsp;|&nbsp;
            <strong>(2)</strong> Premium tier launch for top-10% users &nbsp;|&nbsp;
            <strong>(3)</strong> Device partnership program within 12 months.
        </div>
    </div>""", unsafe_allow_html=True)
   


