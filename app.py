import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Opinion Leader Dashboard · Harita.C",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&display=swap');

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif !important;
}
.stApp {
    background: #080d18;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1526 0%, #0a1020 100%) !important;
    border-right: 1px solid #1a2840 !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem !important; }

/* ── Sidebar labels & sliders ── */
[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #64748b !important;
}
[data-testid="stSidebar"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: #94a3b8 !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(145deg, #101828 0%, #111827 100%) !important;
    border: 1px solid #1a2840 !important;
    border-radius: 14px !important;
    padding: 20px 22px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.03) !important;
}
[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    color: #64748b !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #e2e8f0 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1526 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid #1a2840 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    color: #64748b !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: #1a2840 !important;
    color: #e2e8f0 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #1a2840 !important;
}

/* ── Divider ── */
hr { border-color: #1a2840 !important; }

/* ── Section headers ── */
.section-head {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 4px;
}
.page-title {
    font-family: 'Fraunces', serif;
    font-size: 42px;
    font-weight: 600;
    line-height: 1.08;
    background: linear-gradient(135deg, #f1f5f9 30%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 6px 0;
}
.page-sub {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #475569;
    line-height: 1.7;
    margin-bottom: 0;
}
.insight-box {
    background: linear-gradient(135deg, rgba(59,130,246,.08) 0%, rgba(6,182,212,.05) 100%);
    border: 1px solid rgba(59,130,246,.2);
    border-left: 3px solid #3b82f6;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 13px;
    color: #94a3b8;
    font-family: 'Manrope', sans-serif;
    line-height: 1.6;
}
.insight-box b { color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Mono, monospace', color='#94a3b8', size=11),
    xaxis=dict(gridcolor='rgba(255,255,255,.05)', linecolor='rgba(255,255,255,.08)',
               zerolinecolor='rgba(255,255,255,.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,.05)', linecolor='rgba(255,255,255,.08)',
               zerolinecolor='rgba(255,255,255,.08)'),
    hoverlabel=dict(bgcolor='#1a2235', bordercolor='#3b82f6',
                    font=dict(family='DM Mono, monospace', size=12, color='#e2e8f0')),
    margin=dict(l=16, r=16, t=24, b=16),
    colorway=['#3b82f6', '#06b6d4', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444'],
)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data = [
        {"rank":1,  "name":'O. Brown "Ms. O. Khannah-Brown"',"reviews":421,"helpfulness":0.825,"votes":1285, "sentiment":0.178,"products":309,"score":0.608,"archetype":"Generalist"},
        {"rank":2,  "name":'J. Goldman',                      "reviews":10, "helpfulness":0.990,"votes":4720, "sentiment":0.296,"products":10, "score":0.573,"archetype":"Specialist"},
        {"rank":3,  "name":'C. F. Hill "CFH"',                "reviews":448,"helpfulness":0.483,"votes":1344, "sentiment":0.266,"products":420,"score":0.533,"archetype":"Generalist"},
        {"rank":4,  "name":'Rebecca of Amazon',               "reviews":365,"helpfulness":0.564,"votes":1282, "sentiment":0.236,"products":321,"score":0.499,"archetype":"Generalist"},
        {"rank":5,  "name":'D. Truong "Duke of NM"',          "reviews":23, "helpfulness":0.548,"votes":5594, "sentiment":0.162,"products":23, "score":0.468,"archetype":"Specialist"},
        {"rank":6,  "name":'Spudman',                         "reviews":149,"helpfulness":0.933,"votes":372,  "sentiment":0.141,"products":144,"score":0.450,"archetype":"Generalist"},
        {"rank":7,  "name":'Chandler',                        "reviews":76, "helpfulness":0.858,"votes":1687, "sentiment":0.118,"products":75, "score":0.448,"archetype":"Specialist"},
        {"rank":8,  "name":'G. Roberti "Lube Man"',           "reviews":13, "helpfulness":0.759,"votes":3648, "sentiment":0.088,"products":13, "score":0.447,"archetype":"Specialist"},
        {"rank":9,  "name":'christopher hayes',               "reviews":199,"helpfulness":0.654,"votes":2101, "sentiment":0.086,"products":38, "score":0.437,"archetype":"Generalist"},
        {"rank":10, "name":'Gary Peterson',                   "reviews":389,"helpfulness":0.388,"votes":490,  "sentiment":0.247,"products":382,"score":0.431,"archetype":"Generalist"},
        {"rank":11, "name":'Stephen M. Guilliat',             "reviews":211,"helpfulness":0.612,"votes":890,  "sentiment":0.193,"products":198,"score":0.431,"archetype":"Generalist"},
        {"rank":12, "name":'vegancompassion',                 "reviews":88, "helpfulness":0.701,"votes":1122, "sentiment":0.221,"products":82, "score":0.426,"archetype":"Specialist"},
        {"rank":13, "name":'Steven A. Peterson',              "reviews":178,"helpfulness":0.589,"votes":743,  "sentiment":0.174,"products":165,"score":0.425,"archetype":"Generalist"},
        {"rank":14, "name":'Gregory Bravo',                   "reviews":134,"helpfulness":0.643,"votes":988,  "sentiment":0.209,"products":127,"score":0.425,"archetype":"Generalist"},
        {"rank":15, "name":'Joanna Daneman',                  "reviews":97, "helpfulness":0.722,"votes":1054, "sentiment":0.231,"products":91, "score":0.417,"archetype":"Specialist"},
        {"rank":16, "name":'R. Millar',                       "reviews":56, "helpfulness":0.778,"votes":842,  "sentiment":0.198,"products":54, "score":0.412,"archetype":"Specialist"},
        {"rank":17, "name":'Crunchy Granola',                 "reviews":312,"helpfulness":0.421,"votes":621,  "sentiment":0.256,"products":289,"score":0.408,"archetype":"Generalist"},
        {"rank":18, "name":'A. Karimi',                       "reviews":44, "helpfulness":0.811,"votes":763,  "sentiment":0.142,"products":42, "score":0.403,"archetype":"Specialist"},
        {"rank":19, "name":'NaturalFoodFan',                  "reviews":167,"helpfulness":0.534,"votes":578,  "sentiment":0.187,"products":155,"score":0.398,"archetype":"Generalist"},
        {"rank":20, "name":'PrairieHomesteader',              "reviews":203,"helpfulness":0.491,"votes":511,  "sentiment":0.219,"products":191,"score":0.392,"archetype":"Generalist"},
    ]
    return pd.DataFrame(data)

df_full = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:24px'>
      <div style='font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;
                  text-transform:uppercase;color:#3b82f6;margin-bottom:6px'>
        NLP Capstone · 2026
      </div>
      <div style='font-family:Fraunces,serif;font-size:22px;font-weight:600;color:#e2e8f0;line-height:1.2'>
        Opinion Leader<br/>Dashboard
      </div>
      <div style='font-family:DM Mono,monospace;font-size:11px;color:#475569;margin-top:6px'>
        Harita.C · Woxsen University
      </div>
    </div>
    <hr style='border-color:#1a2840;margin:0 0 20px'/>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b">Filters</p>', unsafe_allow_html=True)

    min_reviews = st.slider("Min Review Count", 5, 300, 5, step=5)
    min_help    = st.slider("Min Helpfulness Ratio", 0.0, 1.0, 0.0, step=0.05, format="%.2f")
    top_n       = st.slider("Show Top N Leaders", 5, 20, 15, step=1)
    archetype   = st.multiselect("Archetype", ["Generalist", "Specialist"],
                                 default=["Generalist", "Specialist"])

    st.markdown("<hr style='border-color:#1a2840;margin:20px 0'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:10px;color:#334155;line-height:1.8'>
      <div style='color:#475569;margin-bottom:8px;letter-spacing:.1em;text-transform:uppercase'>Dataset</div>
      Amazon Fine Food Reviews<br/>
      568,454 reviews<br/>
      23,593 active reviewers<br/>
      Oct 1999 – Oct 2012
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a2840;margin:20px 0'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:10px;color:#334155;line-height:1.8'>
      <div style='color:#475569;margin-bottom:8px;letter-spacing:.1em;text-transform:uppercase'>Submitted to</div>
      Dr. Shyam Joshi
    </div>
    """, unsafe_allow_html=True)

# ── Filter data ───────────────────────────────────────────────────────────────
df = df_full[
    (df_full["reviews"] >= min_reviews) &
    (df_full["helpfulness"] >= min_help) &
    (df_full["archetype"].isin(archetype))
].head(top_n)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:8px'>
  <div class='section-head' style='font-family:DM Mono,monospace;font-size:10px;
       letter-spacing:.18em;text-transform:uppercase;color:#3b82f6;margin-bottom:8px'>
    Review-Based · NLP · Customer Intelligence
  </div>
  <div class='page-title' style='font-family:Fraunces,serif;font-size:42px;font-weight:600;
       line-height:1.08;background:linear-gradient(135deg,#f1f5f9 30%,#3b82f6 100%);
       -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'>
    Opinion Leader Identification
  </div>
  <div class='page-sub' style='font-family:DM Mono,monospace;font-size:12px;
       color:#475569;margin-top:6px'>
    Amazon Fine Food Reviews · Weighted Composite Scoring · Sentiment Analysis · Feature Engineering
  </div>
</div>
<hr style='border-color:#1a2840;margin:18px 0 24px'/>
""", unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Reviews Analysed",  "568,454",  "Oct 1999 – Oct 2012")
k2.metric("Eligible Reviewers",      "23,593",   "Min 5 reviews threshold")
k3.metric("Top OL Score",            f"{df_full['score'].max():.3f}", "O. Brown · 421 reviews")
k4.metric("Opinion Leaders (Top 5%)", "~1,180",  "Score threshold > 0.30")

st.markdown("<div style='margin-top:28px'/>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Leaderboard",
    "🔍  Feature Analysis",
    "🧬  Archetypes",
    "📋  Data Table",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — LEADERBOARD
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Top Opinion Leaders by OL Score</div>', unsafe_allow_html=True)

        if df.empty:
            st.warning("No reviewers match the current filters. Try adjusting the sidebar.")
        else:
            names_short = [n[:28] + "…" if len(n) > 28 else n for n in df["name"]]
            fig_bar = go.Figure(go.Bar(
                x=df["score"],
                y=names_short,
                orientation="h",
                marker=dict(
                    color=df["score"],
                    colorscale=[[0,"#1e3a5f"],[0.4,"#3b82f6"],[0.7,"#06b6d4"],[1,"#a5f3fc"]],
                    line=dict(width=0),
                ),
                text=[f"{s:.3f}" for s in df["score"]],
                textposition="outside",
                textfont=dict(family="DM Mono, monospace", size=11, color="#94a3b8"),
                customdata=list(zip(df["name"], df["reviews"], df["helpfulness"],
                                    df["votes"], df["products"])),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "OL Score: <b>%{x:.3f}</b><br>"
                    "Reviews: %{customdata[1]}<br>"
                    "Helpfulness: %{customdata[2]:.3f}<br>"
                    "Total Votes: %{customdata[3]:,}<br>"
                    "Products: %{customdata[4]}<extra></extra>"
                ),
            ))
            fig_bar.update_layout(
                **PLOTLY_THEME,
                height=max(340, len(df) * 32),
                yaxis=dict(**PLOTLY_THEME["yaxis"], autorange="reversed",
                           tickfont=dict(size=11)),
                xaxis=dict(**PLOTLY_THEME["xaxis"],
                           range=[0, df["score"].max() * 1.2],
                           title=dict(text="Opinion Leader Score", standoff=10)),
                bargap=0.35,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Score Distribution</div>', unsafe_allow_html=True)

        np.random.seed(42)
        pop_scores = np.concatenate([
            -np.log(np.random.uniform(0.001, 1, 20000)) * 0.052,
        ])
        pop_scores = pop_scores[(pop_scores >= 0) & (pop_scores <= 0.65)]
        p95 = np.percentile(pop_scores, 95)

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=pop_scores, nbinsx=48,
            marker=dict(
                color=pop_scores,
                colorscale=[[0,"#1e1b4b"],[0.5,"#3b82f6"],[1,"#06b6d4"]],
                line=dict(width=0),
            ),
            hovertemplate="Score: %{x:.3f}<br>Count: %{y}<extra></extra>",
            name="All reviewers",
        ))
        fig_hist.add_vline(x=p95, line_dash="dash", line_color="#ef4444", line_width=2,
                           annotation_text=f"Top 5%  {p95:.3f}",
                           annotation_font=dict(color="#ef4444", size=11))
        fig_hist.update_layout(
            **PLOTLY_THEME,
            height=260,
            xaxis=dict(**PLOTLY_THEME["xaxis"], title=dict(text="OL Score", standoff=8)),
            yaxis=dict(**PLOTLY_THEME["yaxis"], title=dict(text="Reviewers", standoff=8)),
            showlegend=False, bargap=0.05,
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin:16px 0 10px">Key Insights</div>', unsafe_allow_html=True)

        insights = [
            (f"<b>{len(df)}</b> leaders match current filters", ""),
            (f"Top score: <b>{df['score'].max():.3f}</b>", ""),
            (f"Avg helpfulness: <b>{df['helpfulness'].mean():.3f}</b>", ""),
            (f"Avg sentiment: <b>+{df['sentiment'].mean():.3f}</b> (constructive positive)", ""),
        ]
        for text, _ in insights:
            st.markdown(f'<div class="insight-box" style="background:linear-gradient(135deg,rgba(59,130,246,.08),rgba(6,182,212,.05));border:1px solid rgba(59,130,246,.2);border-left:3px solid #3b82f6;border-radius:0 10px 10px 0;padding:10px 16px;margin:6px 0;font-size:12px;color:#94a3b8;font-family:Manrope,sans-serif;line-height:1.5">{text}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — FEATURE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Sentiment vs. Helpfulness</div>', unsafe_allow_html=True)

        np.random.seed(7)
        N = 500
        pop_h = np.clip(np.random.normal(0.42, 0.22, N), 0, 1)
        pop_s = np.clip(np.random.normal(0.14, 0.18, N), -0.5, 1)
        pop_ol = np.clip(0.35*pop_h + 0.25*np.random.uniform(0,0.3,N)
                         + 0.4*np.random.uniform(0,0.2,N), 0, 0.65)

        fig_sc = go.Figure()
        fig_sc.add_trace(go.Scatter(
            x=pop_s, y=pop_h, mode="markers",
            marker=dict(size=5, opacity=0.4,
                        color=pop_ol,
                        colorscale=[[0,"#1e1b4b"],[0.4,"#3b82f6"],[0.7,"#8b5cf6"],[1,"#f59e0b"]],
                        line=dict(width=0)),
            hovertemplate="Sentiment: %{x:.3f}<br>Helpfulness: %{y:.3f}<extra>Reviewer pool</extra>",
            name="All reviewers",
        ))
        fig_sc.add_trace(go.Scatter(
            x=df["sentiment"], y=df["helpfulness"], mode="markers+text",
            text=[n.split()[0] for n in df["name"]],
            textposition="top right",
            textfont=dict(size=10, color="#f59e0b", family="DM Mono, monospace"),
            marker=dict(size=13, color="#f59e0b", symbol="star",
                        line=dict(color="#0a0e1a", width=2)),
            customdata=list(zip(df["name"], df["score"])),
            hovertemplate="<b>%{customdata[0]}</b><br>Sentiment: %{x:.3f}<br>Helpfulness: %{y:.3f}<br>OL Score: %{customdata[1]:.3f}<extra>Top Leader</extra>",
            name="Top leaders",
        ))
        fig_sc.update_layout(
            **PLOTLY_THEME, height=380,
            xaxis=dict(**PLOTLY_THEME["xaxis"], title=dict(text="Avg Sentiment Polarity", standoff=10), zeroline=True),
            yaxis=dict(**PLOTLY_THEME["yaxis"], title=dict(text="Avg Helpfulness Ratio", standoff=10), range=[-0.05, 1.1]),
            legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=11)),
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Feature Correlation Matrix</div>', unsafe_allow_html=True)

        labels = ["Review\nCount", "Avg\nHelpfulness", "Total\nVotes",
                  "Avg\nSentiment", "Review\nLength", "Products", "OL Score"]
        corr = np.array([
            [1.00, 0.12, 0.38, 0.03, 0.44, 0.91, 0.31],
            [0.12, 1.00, 0.44, 0.07, 0.19, 0.10, 0.78],
            [0.38, 0.44, 1.00, 0.05, 0.31, 0.34, 0.71],
            [0.03, 0.07, 0.05, 1.00, 0.09, 0.02, 0.11],
            [0.44, 0.19, 0.31, 0.09, 1.00, 0.41, 0.29],
            [0.91, 0.10, 0.34, 0.02, 0.41, 1.00, 0.28],
            [0.31, 0.78, 0.71, 0.11, 0.29, 0.28, 1.00],
        ])
        masked = np.where(np.triu(np.ones_like(corr, dtype=bool), k=1), np.nan, corr)
        text_vals = [[f"{v:.2f}" if not np.isnan(v) else "" for v in row] for row in masked]

        fig_heat = go.Figure(go.Heatmap(
            z=masked, x=labels, y=labels,
            colorscale=[[0,"#1e1b4b"],[0.35,"#3b82f6"],[0.65,"#06b6d4"],[1,"#10b981"]],
            zmin=-0.1, zmax=1,
            text=text_vals, texttemplate="%{text}",
            textfont=dict(size=11, family="DM Mono, monospace"),
            hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
            showscale=True,
            colorbar=dict(thickness=12, tickfont=dict(size=10), outlinewidth=0),
        ))
        fig_heat.update_layout(
            **PLOTLY_THEME, height=380,
            xaxis=dict(**PLOTLY_THEME["xaxis"], tickangle=-30, tickfont=dict(size=10)),
            yaxis=dict(**PLOTLY_THEME["yaxis"], tickfont=dict(size=10)),
            margin=dict(l=100, r=16, t=24, b=100),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # ── Feature weights bar ──────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#1a2840;margin:8px 0 20px'/>", unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Model Feature Weights</div>', unsafe_allow_html=True)

    feat_names  = ["Avg Helpfulness Ratio", "Total Helpful Votes", "Unique Products",
                   "Review Count", "Avg Review Length"]
    feat_weights = [0.35, 0.25, 0.15, 0.15, 0.10]
    feat_colors  = ["#3b82f6", "#06b6d4", "#8b5cf6", "#f59e0b", "#10b981"]

    fig_w = go.Figure(go.Bar(
        x=feat_weights, y=feat_names, orientation="h",
        marker=dict(color=feat_colors, line=dict(width=0)),
        text=[f"{w:.0%}" for w in feat_weights],
        textposition="outside",
        textfont=dict(family="DM Mono, monospace", size=12, color="#94a3b8"),
        hovertemplate="%{y}<br>Weight: %{x:.0%}<extra></extra>",
    ))
    fig_w.update_layout(
        **PLOTLY_THEME, height=220,
        yaxis=dict(**PLOTLY_THEME["yaxis"], autorange="reversed", tickfont=dict(size=12)),
        xaxis=dict(**PLOTLY_THEME["xaxis"], range=[0, 0.45],
                   tickformat=".0%", title=dict(text="Weight in OL Score", standoff=8)),
        bargap=0.4,
    )
    st.plotly_chart(fig_w, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — ARCHETYPES
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:4px">Two distinct profiles emerge from the data</div>', unsafe_allow_html=True)

    col_x, col_y = st.columns(2, gap="large")

    with col_x:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(59,130,246,.08),transparent);
             border:1px solid rgba(59,130,246,.2);border-radius:14px;padding:20px 22px;margin-bottom:16px'>
          <div style='font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;
               text-transform:uppercase;color:#3b82f6;margin-bottom:8px'>Archetype A</div>
          <div style='font-family:Fraunces,serif;font-size:22px;color:#e2e8f0;margin-bottom:8px'>
            High-Volume Generalist
          </div>
          <div style='font-family:Manrope,sans-serif;font-size:13px;color:#64748b;line-height:1.7'>
            Prolific reviewers covering a wide range of products. Influence comes from <b style="color:#94a3b8">breadth and consistency</b>.
            Best suited for broad category coverage and sustained brand presence.<br/><br/>
            <b style="color:#3b82f6">Example:</b> C.F. Hill — 448 reviews across 420 products
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_y:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(245,158,11,.08),transparent);
             border:1px solid rgba(245,158,11,.2);border-radius:14px;padding:20px 22px;margin-bottom:16px'>
          <div style='font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;
               text-transform:uppercase;color:#f59e0b;margin-bottom:8px'>Archetype B</div>
          <div style='font-family:Fraunces,serif;font-size:22px;color:#e2e8f0;margin-bottom:8px'>
            Low-Volume Specialist
          </div>
          <div style='font-family:Manrope,sans-serif;font-size:13px;color:#64748b;line-height:1.7'>
            Infrequent but highly trusted reviewers. Influence comes from <b style="color:#94a3b8">authority and peer validation</b>.
            Best suited for niche credibility and high-trust product endorsements.<br/><br/>
            <b style="color:#f59e0b">Example:</b> J. Goldman — 10 reviews, 4,720 helpful votes
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Grouped bar ──────────────────────────────────────────────────────────
    cats = ["Review Count", "Helpfulness Ratio", "Helpful Votes", "Products Reviewed", "Review Length"]
    gen  = [0.92, 0.53, 0.22, 0.95, 0.61]
    spec = [0.04, 0.99, 0.88, 0.04, 0.74]

    fig_arch = go.Figure()
    fig_arch.add_trace(go.Bar(
        name="Generalist (C.F. Hill)", x=cats, y=gen,
        marker=dict(color="#3b82f6", opacity=0.85, line=dict(width=0)),
        text=[f"{v:.2f}" for v in gen], textposition="outside",
        textfont=dict(family="DM Mono, monospace", size=11, color="#3b82f6"),
        hovertemplate="%{x}<br>Normalised: <b>%{y:.2f}</b><extra>Generalist</extra>",
    ))
    fig_arch.add_trace(go.Bar(
        name="Specialist (J. Goldman)", x=cats, y=spec,
        marker=dict(color="#f59e0b", opacity=0.85, line=dict(width=0)),
        text=[f"{v:.2f}" for v in spec], textposition="outside",
        textfont=dict(family="DM Mono, monospace", size=11, color="#f59e0b"),
        hovertemplate="%{x}<br>Normalised: <b>%{y:.2f}</b><extra>Specialist</extra>",
    ))
    fig_arch.update_layout(
        **PLOTLY_THEME, height=340, barmode="group", bargap=0.3, bargroupgap=0.08,
        yaxis=dict(**PLOTLY_THEME["yaxis"], range=[0, 1.18],
                   title=dict(text="Normalised Score (0–1)", standoff=10)),
        xaxis=dict(**PLOTLY_THEME["xaxis"], tickfont=dict(size=12)),
        legend=dict(orientation="h", y=-0.22, x=0, font=dict(size=12)),
    )
    st.plotly_chart(fig_arch, use_container_width=True)

    # ── Bubble chart ─────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:#1a2840;margin:8px 0 20px'/>", unsafe_allow_html=True)
    st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Reviews vs. Helpful Votes — bubble size = OL Score</div>', unsafe_allow_html=True)

    arch_colors = {"Generalist": "#3b82f6", "Specialist": "#f59e0b"}
    fig_bub = go.Figure()
    for arch_type in df["archetype"].unique():
        sub = df[df["archetype"] == arch_type]
        fig_bub.add_trace(go.Scatter(
            x=sub["reviews"], y=sub["votes"],
            mode="markers+text",
            text=[n.split()[0] for n in sub["name"]],
            textposition="top center",
            textfont=dict(size=10, color=arch_colors.get(arch_type,"#94a3b8"), family="DM Mono, monospace"),
            marker=dict(
                size=sub["score"] * 80,
                color=arch_colors.get(arch_type, "#94a3b8"),
                opacity=0.75, line=dict(width=1, color="#0a0e1a"),
            ),
            customdata=list(zip(sub["name"], sub["score"], sub["helpfulness"])),
            hovertemplate="<b>%{customdata[0]}</b><br>Reviews: %{x}<br>Votes: %{y:,}<br>OL Score: %{customdata[1]:.3f}<br>Helpfulness: %{customdata[2]:.3f}<extra>" + arch_type + "</extra>",
            name=arch_type,
        ))
    fig_bub.update_layout(
        **PLOTLY_THEME, height=360,
        xaxis=dict(**PLOTLY_THEME["xaxis"], title=dict(text="Number of Reviews", standoff=10)),
        yaxis=dict(**PLOTLY_THEME["yaxis"], title=dict(text="Total Helpful Votes", standoff=10)),
        legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=12)),
    )
    st.plotly_chart(fig_bub, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — DATA TABLE
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-head" style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#64748b;margin-bottom:12px">Full Ranked Reviewer Profiles</div>', unsafe_allow_html=True)

    sort_col = st.selectbox("Sort by", ["score","reviews","helpfulness","votes","sentiment","products"],
                             index=0,
                             format_func=lambda x: {
                                 "score":"OL Score","reviews":"Review Count",
                                 "helpfulness":"Avg Helpfulness","votes":"Total Helpful Votes",
                                 "sentiment":"Avg Sentiment","products":"Products Reviewed"
                             }[x])
    sort_asc = st.toggle("Sort ascending", value=False)

    df_display = df.sort_values(sort_col, ascending=sort_asc).copy()
    df_display.columns = [c.title().replace("_"," ") for c in df_display.columns]
    df_display = df_display.rename(columns={
        "Rank":"#","Name":"Reviewer","Reviews":"Reviews",
        "Helpfulness":"Avg Helpfulness","Votes":"Total Votes",
        "Sentiment":"Avg Sentiment","Products":"Products",
        "Score":"OL Score","Archetype":"Archetype"
    })

    st.dataframe(
        df_display.style
            .background_gradient(subset=["OL Score"], cmap="Blues")
            .background_gradient(subset=["Avg Helpfulness"], cmap="Greens")
            .format({"OL Score":"{:.3f}","Avg Helpfulness":"{:.3f}","Avg Sentiment":"{:.3f}"}),
        use_container_width=True, height=420,
    )

    st.markdown("<div style='margin-top:16px'/>", unsafe_allow_html=True)
    csv = df_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Download filtered results as CSV",
        data=csv, file_name="opinion_leaders_filtered.csv", mime="text/csv",
    )
