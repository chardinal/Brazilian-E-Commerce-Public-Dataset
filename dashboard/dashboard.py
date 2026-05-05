"""
Dashboard Analisis: Brazilian E-Commerce Public Dataset
Jalankan: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings

warnings.filterwarnings("ignore")

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Color Palette & Theming ──────────────────────────────────
C = {
    "bg":       "#F8FAFC", # Slate 50
    "white":    "#FFFFFF",
    "text":     "#0F172A", # Slate 900
    "muted":    "#64748B", # Slate 500
    "border":   "#E2E8F0", # Slate 200
    "primary":  "#2563EB", # Blue 600
    "primary_light": "#DBEAFE", # Blue 100
    "green":    "#10B981", # Emerald 500
    "red":      "#EF4444", # Red 500
    "amber":    "#F59E0B", # Amber 500
    "teal":     "#14B8A6", # Teal 500
    "chart":    ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"],
}

# ─── Chart defaults (High-Res & Clean) ────────────────────────
plt.rcParams.update({
    "figure.facecolor":  C["white"],
    "axes.facecolor":    C["white"],
    "axes.edgecolor":    C["border"],
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.labelcolor":   C["muted"],
    "axes.labelsize":    10,
    "axes.titlesize":    12,
    "axes.titleweight":  "bold",
    "axes.titlecolor":   C["text"],
    "axes.grid":         True,
    "grid.color":        C["border"],
    "grid.linewidth":    0.6,
    "grid.linestyle":    "--",
    "grid.alpha":        0.7,
    "xtick.color":       C["muted"],
    "ytick.color":       C["muted"],
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "text.color":        C["text"],
    "legend.frameon":    False,
    "legend.fontsize":   9,
    "font.family":       "sans-serif",
    "figure.dpi":        300, # Bikin grafik sangat tajam
})

# ─── Global CSS ───────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: {C['bg']};
    color: {C['text']};
}}
.stApp {{ background-color: {C['bg']}; }}

/* Sidebar Enhancement */
[data-testid="stSidebar"] {{
    background-color: {C['white']};
    border-right: 1px solid {C['border']};
    box-shadow: 2px 0 10px rgba(0,0,0,0.02);
}}

/* Typography */
.page-title {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {C['text']};
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}}
.page-sub {{
    font-size: 0.95rem;
    color: {C['muted']};
    margin-bottom: 2rem;
}}

/* KPI Cards with Hover Effect */
.kpi {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}
.kpi:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
    border-color: {C['primary_light']};
}}
.kpi-label {{
    font-size: 0.75rem;
    font-weight: 600;
    color: {C['muted']};
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}
.kpi-value {{
    font-size: 1.75rem;
    font-weight: 700;
    color: {C['text']};
    line-height: 1.1;
}}
.kpi-note {{
    font-size: 0.8rem;
    color: {C['muted']};
    margin-top: 0.5rem;
    font-weight: 500;
}}

/* Section label */
.section-label {{
    font-size: 0.8rem;
    font-weight: 700;
    color: {C['text']};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 2rem 0 1rem;
    border-bottom: 2px solid {C['border']};
    padding-bottom: 0.5rem;
}}

/* Insight Callout */
.insight {{
    background: linear-gradient(145deg, #EFF6FF 0%, #FFFFFF 100%);
    border-left: 4px solid {C['primary']};
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.9rem;
    color: {C['text']};
    line-height: 1.6;
    margin-top: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}}
.insight b {{ color: {C['primary']}; font-weight: 600; }}

/* Segment badge */
.seg-badge {{
    display: inline-block;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    text-align: center;
    min-width: 100px;
    transition: transform 0.2s;
}}
.seg-badge:hover {{ transform: scale(1.02); }}
.seg-badge .val {{
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.2;
}}
.seg-badge .lbl {{
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.2rem;
}}

/* Clean up elements */
hr {{ border: none; border-top: 1px solid {C['border']}; margin: 1.5rem 0; }}
</style>
""", unsafe_allow_html=True)

# ─── Helpers ──────────────────────────────────────────────────
def kpi(label, value, note=""):
    note_html = f'<div class="kpi-note">{note}</div>' if note else ""
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {note_html}
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight">💡 <b>Business Insight:</b><br>{text}</div>', unsafe_allow_html=True)

def fig_clean(w=10, h=4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(C["white"])
    ax.set_facecolor(C["white"])
    return fig, ax

# ─── Data Loading ─────────────────────────────────────────────
@st.cache_data
def load():
    try:
        return (
            pd.read_csv("dashboard/revenue_by_category.csv"), 
            pd.read_csv("dashboard/rfm_df.csv"),              
            pd.read_csv("dashboard/monthly_trend.csv"),       
            pd.read_csv("dashboard/payment_freq.csv"),        
            pd.read_csv("dashboard/delivery_review.csv"),     
            pd.read_csv("dashboard/main_df.csv", parse_dates=["order_purchase_timestamp"]) 
        )
    except FileNotFoundError as e:
        st.error(f"⚠️ Dataset tidak ditemukan: {e}\nPastikan file CSV berada di dalam folder 'dashboard/'.")
        st.stop()

rev_df, rfm_df, mo_df, pay_df, del_df, main_df = load()

# ─── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0; text-align: center;">
        <div style="font-size:1.5rem; font-weight:800; color:#0F172A; letter-spacing:-1px;">🛍️ Olist Analytics</div>
        <div style="font-size:0.85rem; font-weight:500; color:#2563EB; margin-top:0.3rem;">Executive Dashboard</div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    page = st.radio("Navigasi", [
        "Executive Overview",
        "Kinerja Produk & Kategori",
        "Analisis Kohort & RFM",
        "Tren Pertumbuhan",
        "Infrastruktur Pembayaran",
        "Logistik & Kepuasan",
    ], label_visibility="collapsed")

    st.divider()

    if "order_purchase_timestamp" in main_df.columns:
        st.markdown('<div style="font-size:0.8rem; font-weight:600; margin-bottom:0.5rem; color:#64748B;">FILTER TANGGAL TRANSAKSI</div>', unsafe_allow_html=True)
        mn = main_df["order_purchase_timestamp"].min().date()
        mx = main_df["order_purchase_timestamp"].max().date()
        dr = st.date_input("Filter", [mn, mx], min_value=mn, max_value=mx, label_visibility="collapsed")
    else:
        dr = None

    st.divider()
    st.markdown(f"""
    <div style="font-size:0.75rem; color:#64748B; line-height:1.6; text-align: center;">
        Dicoding Data Analysis Project<br>
        <b>Chardinal Martin Butarbutar</b>
    </div>""", unsafe_allow_html=True)

if dr and len(dr) == 2:
    mf = main_df[
        (main_df["order_purchase_timestamp"] >= pd.Timestamp(dr[0])) &
        (main_df["order_purchase_timestamp"] <= pd.Timestamp(dr[1]))
    ]
else:
    mf = main_df

# ══════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "Executive Overview":
    st.markdown('<div class="page-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Ringkasan performa makro Olist E-Commerce (Dataset Publik Brasil)</div>', unsafe_allow_html=True)

    total_rev   = mf["revenue"].sum()
    total_ord   = mf["order_id"].nunique()
    total_cust  = mf["customer_unique_id"].nunique() if "customer_unique_id" in mf.columns else 0
    avg_score   = mf["review_score"].mean() if "review_score" in mf.columns else 0
    avg_del     = mf["delivery_days"].mean() if "delivery_days" in mf.columns else 0
    
    section("METRIK UTAMA")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Total Revenue",       f"R${total_rev/1e6:.2f}M")
    with c2: kpi("Total Orders",        f"{total_ord:,}")
    with c3: kpi("Active Customers",    f"{total_cust:,}")
    with c4: kpi("Customer Satisfaction",f"{avg_score:.2f} / 5")
    with c5: kpi("Avg. Delivery Time",  f"{avg_del:.1f} Hari")

    section("TREN PERTUMBUHAN & METODE PEMBAYARAN")
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown('**Tren Pemesanan Bulanan**')
        if "year_month_str" in mo_df.columns:
            fig, ax = fig_clean(9, 4.5)
            x = np.arange(len(mo_df))
            ax.bar(x, mo_df["total_orders"], color=C["primary_light"], width=0.6)
            ax.plot(x, mo_df["total_orders"], color=C["primary"], marker='o', markersize=4, linewidth=2, label="Orders")
            
            if "orders_MA3" in mo_df.columns:
                ax.plot(x, mo_df["orders_MA3"], color=C["amber"], linewidth=2, linestyle="--", label="3-Mo MA")
            
            step = max(1, len(mo_df) // 8)
            ax.set_xticks(x[::step])
            ax.set_xticklabels(mo_df["year_month_str"].iloc[::step], rotation=30, ha="right")
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1e3:.1f}K" if v >= 1000 else f"{v:.0f}"))
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True); plt.close(fig)

    with col_r:
        st.markdown('**Metode Pembayaran Dominan**')
        fig, ax = fig_clean(5, 4.5)
        wedges, texts, autotexts = ax.pie(
            pay_df["count"], labels=pay_df["payment_type"].str.replace("_", " ").str.title(),
            autopct="%1.1f%%", colors=C["chart"], startangle=90, pctdistance=0.75,
            wedgeprops=dict(width=0.6, edgecolor="white", linewidth=2),
            textprops={'fontsize': 9, 'color': C['text']}
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

# ══════════════════════════════════════════════════════════════
# REVENUE PER KATEGORI
# ══════════════════════════════════════════════════════════════
elif page == "Kinerja Produk & Kategori":
    st.markdown('<div class="page-title">Kinerja Produk & Kategori</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Analisis kontribusi revenue dan volume pemesanan berdasarkan kategori produk.</div>', unsafe_allow_html=True)

    top1 = rev_df.iloc[0]
    bot1 = rev_df.iloc[-1]
    avg_rev_per_order = rev_df["avg_revenue_per_order"].mean()

    section("RINGKASAN KINERJA KATEGORI")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Kategori Aktif",        f"{len(rev_df)}")
    with c2: kpi("Top Revenue",           f"R${top1['total_revenue']/1e6:.2f}M", top1["product_category_name_english"].replace("_", " ").title())
    with c3: kpi("Bottom Revenue",        f"R${bot1['total_revenue']:.0f}", bot1["product_category_name_english"].replace("_", " ").title())
    with c4: kpi("AOV (Avg Order Value)", f"R${avg_rev_per_order:.0f}")

    section("DISTRIBUSI REVENUE (TOP & BOTTOM)")
    n = st.slider("Atur jumlah kategori yang dianalisis:", 5, 20, 10)
    top_n = rev_df.head(n).copy()
    bot_n = rev_df.tail(n).iloc[::-1].copy()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('**Top Kategori — Revenue Tertinggi**')
        fig, ax = fig_clean(7, max(4.5, n * 0.5))
        colors = [C["primary"] if i == 0 else C["primary_light"] for i in range(n)]
        bars = ax.barh(top_n["product_category_name_english"].str.replace("_", " ").str.title(),
                       top_n["total_revenue"], color=colors, height=0.6, edgecolor="none")
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v/1e6:.1f}M"))
        ax.invert_yaxis()
        for bar in bars:
            w = bar.get_width()
            ax.text(w + w * 0.02, bar.get_y() + bar.get_height() / 2, f"R${w/1e6:.2f}M", 
                    va="center", fontsize=9, color=C["text"], fontweight='bold' if bar == bars[0] else 'normal')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    with col2:
        st.markdown('**Bottom Kategori — Revenue Terendah**')
        fig, ax = fig_clean(7, max(4.5, n * 0.5))
        colors = [C["red"] if i == 0 else "#FCA5A5" for i in range(n)]
        bars = ax.barh(bot_n["product_category_name_english"].str.replace("_", " ").str.title(),
                       bot_n["total_revenue"], color=colors, height=0.6, edgecolor="none")
        ax.invert_yaxis()
        for bar in bars:
            w = bar.get_width()
            ax.text(w + max(w * 0.05, 5), bar.get_y() + bar.get_height() / 2, f"R${w:.0f}", 
                    va="center", fontsize=9, color=C["text"])
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    insight(
        "Kategori <b>Health & Beauty</b> dan <b>Watches & Gifts</b> menjadi *cash cow* utama bagi platform. "
        "Menariknya, terdapat kategori dengan volume order yang moderate namun memiliki AOV (Average Order Value) tinggi, "
        "mengindikasikan bahwa kategori tersebut memuat barang premium. Rekomendasi strategis: alokasikan budget *marketing* "
        "yang lebih besar untuk *retargeting* pelanggan di Top 5 kategori ini."
    )

# ══════════════════════════════════════════════════════════════
# SEGMENTASI RFM
# ══════════════════════════════════════════════════════════════
elif page == "Analisis Kohort & RFM":
    st.markdown('<div class="page-title">Analisis RFM (Recency, Frequency, Monetary)</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pemetaan perilaku pelanggan menggunakan algoritma clustering RFM untuk penentuan strategi retensi.</div>', unsafe_allow_html=True)

    seg_df = rfm_df.groupby("segment").agg(
        Pelanggan=("customer_unique_id", "count"),
        Recency=("recency", "mean"),
        Frequency=("frequency", "mean"),
        Monetary=("monetary", "mean"),
    ).round(1).reset_index().sort_values("Pelanggan", ascending=False)

    SEG_COLOR = {
        "Champions":       C["green"],
        "Loyal Customers": C["teal"],
        "Promising":       C["primary"],
        "Needs Attention": C["amber"],
        "At Risk":         "#EA580C",
        "Lost":            C["red"],
    }

    section("DISTRIBUSI POPULASI SEGMEN")
    total_cust_rfm = seg_df["Pelanggan"].sum()
    cols = st.columns(len(seg_df))
    for col, (_, row) in zip(cols, seg_df.iterrows()):
        pct = row["Pelanggan"] / total_cust_rfm * 100
        c = SEG_COLOR.get(row["segment"], C["muted"])
        with col:
            st.markdown(f"""
            <div class="seg-badge" style="background:{c}15; border:1px solid {c}55; color:{c}; width:100%;">
                <div class="val">{int(row['Pelanggan']):,}</div>
                <div class="lbl">{row['segment']}</div>
                <div style="font-size:0.75rem; margin-top:0.2rem; font-weight:500;">{pct:.1f}%</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('**Volume Pelanggan per Segmen RFM**')
        fig, ax = fig_clean(6, 4.5)
        seg_colors = [SEG_COLOR.get(s, C["muted"]) for s in seg_df["segment"]]
        bars = ax.barh(seg_df["segment"], seg_df["Pelanggan"], color=seg_colors, height=0.6)
        ax.invert_yaxis()
        for bar, (_, row) in zip(bars, seg_df.iterrows()):
            pct = row["Pelanggan"] / total_cust_rfm * 100
            ax.text(bar.get_width() + total_cust_rfm * 0.02, bar.get_y() + bar.get_height() / 2,
                    f"{int(row['Pelanggan']):,} ({pct:.1f}%)", va="center", fontsize=9, fontweight='500')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    with col2:
        st.markdown('**Skor Relatif: Recency vs Frequency vs Monetary**')
        rfm_norm = seg_df[["segment", "Recency", "Frequency", "Monetary"]].copy()
        for col in ["Recency", "Frequency", "Monetary"]:
            mi, mx = rfm_norm[col].min(), rfm_norm[col].max()
            rfm_norm[col] = (rfm_norm[col] - mi) / (mx - mi + 1e-9)
        rfm_norm["Recency"] = 1 - rfm_norm["Recency"] # Invert for graph logic

        x = np.arange(len(rfm_norm))
        w = 0.25
        fig, ax = fig_clean(6, 4.5)
        ax.bar(x - w, rfm_norm["Recency"], width=w, color=C["primary"], label="Recency (Inv.)")
        ax.bar(x, rfm_norm["Frequency"], width=w, color=C["green"], label="Frequency")
        ax.bar(x + w, rfm_norm["Monetary"], width=w, color=C["amber"], label="Monetary")
        ax.set_xticks(x)
        ax.set_xticklabels(rfm_norm["segment"], rotation=25, ha="right")
        ax.set_ylabel("Normalized Score (0-1)")
        ax.legend(loc='upper right')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    insight(
        "Pendekatan segmentasi ini menunjukkan bahwa infrastruktur *customer retention* platform perlu dibenahi. "
        "Populasi segmen <b>Lost</b> dan <b>At Risk</b> yang tinggi menunjukkan adanya potensi <i>churn rate</i> yang tidak tertangani. "
        "Namun, keberadaan kelompok <b>Champions</b> dengan metrik *Monetary* dan *Frequency* tinggi membuka peluang implementasi sistem *loyalty reward* "
        "yang dapat memicu *Customer Lifetime Value (CLV)* jangka panjang."
    )

# ══════════════════════════════════════════════════════════════
# TREN BULANAN
# ══════════════════════════════════════════════════════════════
elif page == "Tren Pertumbuhan":
    st.markdown('<div class="page-title">Tren Pertumbuhan & MoM Growth</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Evaluasi volatilitas transaksi dan revenue (Month-over-Month).</div>', unsafe_allow_html=True)

    best_rev_idx = mo_df["total_revenue"].idxmax()
    growth_rev   = (mo_df["total_revenue"].iloc[-1] - mo_df["total_revenue"].iloc[0]) / mo_df["total_revenue"].iloc[0] * 100
    mo_df["rev_growth"] = mo_df["total_revenue"].pct_change() * 100

    section("METRIK PERTUMBUHAN")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Total Akumulasi Revenue",  f"R${mo_df['total_revenue'].sum()/1e6:.2f}M")
    with c2: kpi("Puncak Transaksi",         mo_df.loc[best_rev_idx, 'year_month_str'], f"R${mo_df.loc[best_rev_idx,'total_revenue']/1e6:.2f}M")
    with c3: kpi("Net Growth (Awal-Akhir)",  f"{growth_rev:+.1f}%")
    with c4: kpi("Rata-rata MoM Growth",     f"{mo_df['rev_growth'].mean():+.2f}%")

    section("VISUALISASI PERTUMBUHAN")
    st.markdown('**Month-over-Month Revenue Growth (%)**')
    fig, ax = fig_clean(14, 4)
    growth_vals = mo_df["rev_growth"].iloc[1:].values
    bar_colors  = [C["green"] if v >= 0 else C["red"] for v in growth_vals]
    ax.bar(range(len(growth_vals)), growth_vals, color=bar_colors, width=0.6, alpha=0.9)
    ax.axhline(0, color=C["text"], linewidth=1, linestyle="-")
    
    step = max(1, len(mo_df) // 12)
    ax.set_xticks(range(0, len(growth_vals), step))
    ax.set_xticklabels(mo_df["year_month_str"].iloc[1::step], rotation=0)
    ax.set_ylabel("Growth Rate (%)")
    
    for i, v in enumerate(growth_vals):
        if abs(v) > 20: # Anotasi fluktuasi besar
            ax.text(i, v + (2 if v >= 0 else -6), f"{v:+.0f}%", ha='center', fontsize=7.5, color=bar_colors[i], fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True); plt.close(fig)

    insight(
        "Pertumbuhan awal platform menunjukkan ciri khas fase <i>early-stage startup</i> dengan fluktuasi MoM yang agresif. "
        "Memasuki akhir 2017 hingga 2018, laju pertumbuhan cenderung menstabil. Lonjakan esktrem di Q4 2017 berkorelasi kuat "
        "dengan musim diskon besar (*Black Friday* / *Cyber Monday*), mengindikasikan bahwa konsumen sangat sensitif terhadap promosi harga."
    )

# ══════════════════════════════════════════════════════════════
# METODE PEMBAYARAN
# ══════════════════════════════════════════════════════════════
elif page == "Infrastruktur Pembayaran":
    st.markdown('<div class="page-title">Infrastruktur & Preferensi Pembayaran</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Analisis instrumentasi finansial yang digunakan pelanggan.</div>', unsafe_allow_html=True)

    dom = pay_df.loc[pay_df["count"].idxmax()]
    hi_avg = pay_df.loc[pay_df["avg_value"].idxmax()]

    section("METRIK PEMBAYARAN")
    c1, c2, c3 = st.columns(3)
    with c1: kpi("Instrumen Dominan", dom["payment_type"].replace("_", " ").title(), f"{dom['pct']:.1f}% dari keseluruhan")
    with c2: kpi("AOV Tertinggi Berdasarkan Instrumen", f"R${hi_avg['avg_value']:.0f}", hi_avg["payment_type"].replace("_", " ").title())
    with c3: kpi("Total Gross Merchandise Value", f"R${pay_df['total_value'].sum()/1e6:.2f}M")

    section("KOMPARASI INSTRUMEN")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('**Volume Transaksi per Instrumen**')
        fig, ax = fig_clean(6.5, 4.5)
        sorted_count = pay_df.sort_values("count")
        colors = [C["primary"] if i == len(sorted_count)-1 else C["primary_light"] for i in range(len(sorted_count))]
        bars = ax.barh(sorted_count["payment_type"].str.replace("_", " ").str.title(), sorted_count["count"], color=colors, height=0.6)
        ax.grid(axis='y', alpha=0)
        for bar, (_, row) in zip(bars, sorted_count.iterrows()):
            w = bar.get_width()
            ax.text(w + pay_df["count"].max() * 0.02, bar.get_y() + bar.get_height() / 2, f"{int(w):,} ({row['pct']:.1f}%)", va="center", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    with col2:
        st.markdown('**Rata-Rata Nilai Transaksi (AOV) per Instrumen**')
        fig, ax = fig_clean(6.5, 4.5)
        sorted_avg = pay_df.sort_values("avg_value")
        colors = [C["green"] if i == len(sorted_avg)-1 else "#D1FAE5" for i in range(len(sorted_avg))]
        bars = ax.barh(sorted_avg["payment_type"].str.replace("_", " ").str.title(), sorted_avg["avg_value"], color=colors, height=0.6)
        ax.grid(axis='y', alpha=0)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + pay_df["avg_value"].max() * 0.02, bar.get_y() + bar.get_height() / 2, f"R${w:.0f}", va="center", fontsize=9, fontweight='bold' if bar == bars[-1] else 'normal')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    insight(
        "Ketergantungan platform pada <b>Credit Card</b> (>70%) memvalidasi lanskap e-commerce Brasil di mana fasilitas *installments* (cicilan) "
        "merupakan pendorong utama konversi. Keberadaan <b>Boleto</b> (sistem pembayaran tunai bank) tetap krusial untuk melayani demografi *unbanked* "
        "yang masih mendominasi pasar Amerika Latin."
    )

# ══════════════════════════════════════════════════════════════
# PENGIRIMAN & KEPUASAN
# ══════════════════════════════════════════════════════════════
elif page == "Logistik & Kepuasan":
    st.markdown('<div class="page-title">Analisis SLA Logistik & Kepuasan Pelanggan</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Mengukur korelasi antara performa *Supply Chain* dengan *Review Score*.</div>', unsafe_allow_html=True)

    corr_val = del_df["delivery_days"].corr(del_df["review_score"])
    fast_pct = (del_df["delivery_days"] <= 7).mean() * 100

    section("METRIK LOGISTIK")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Korelasi (Pearson)", f"{corr_val:.2f}", "Negatif = SLA Lama → Skor Turun")
    with c2: kpi("SLA Pengiriman Rata-rata", f"{del_df['delivery_days'].mean():.1f} Hari")
    with c3: kpi("Global Review Score", f"{del_df['review_score'].mean():.2f} / 5")
    with c4: kpi("On-Time / Fast Delivery (≤7 Hari)", f"{fast_pct:.1f}%")

    order_cat   = ["1-Fast (≤7 days)", "2-Normal (8-14 days)", "3-Slow (15-21 days)", "4-Very Slow (>21 days)"]
    short_lbl   = ["Cepat\n(≤7 hari)", "Normal\n(8–14 hari)", "Lambat\n(15–21 hari)", "Sangat Lambat\n(>21 hari)"]
    cat_colors  = [C["green"], C["teal"], C["amber"], C["red"]]
    plot_data   = del_df[del_df["delivery_category"].isin(order_cat)].copy()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('**Dampak SLA Terhadap Skor Ulasan Rata-rata**')
        stats = plot_data.groupby("delivery_category").agg(avg=("review_score", "mean"), n=("order_id", "count")).reindex(order_cat).reset_index()
        fig, ax = fig_clean(6.5, 5)
        bars = ax.bar(range(4), stats["avg"], color=cat_colors, width=0.6, edgecolor='none')
        avg_global = del_df["review_score"].mean()
        ax.axhline(avg_global, color=C["text"], linewidth=1.5, linestyle="--", label=f"Rata-rata Platform ({avg_global:.2f})")
        
        ax.set_xticks(range(4))
        ax.set_xticklabels(short_lbl, fontsize=9)
        ax.set_ylim(1, 5.2)
        ax.legend(loc="upper right")
        ax.grid(axis='x', alpha=0)
        
        for i, (bar, row) in enumerate(zip(bars, stats.itertuples())):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f"{row.avg:.2f}", ha="center", fontsize=11, fontweight="bold", color=cat_colors[i])
            ax.text(bar.get_x() + bar.get_width()/2, 0.5, f"n={row.n:,}", ha="center", fontsize=8, color="white", fontweight="bold")
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    with col2:
        st.markdown('**Distribusi Review Score (Box Plot)**')
        fig, ax = fig_clean(6.5, 5)
        box_data = [plot_data[plot_data["delivery_category"] == c]["review_score"].dropna().values for c in order_cat]
        
        bp = ax.boxplot(box_data, patch_artist=True, notch=False,
                        medianprops=dict(color=C["text"], linewidth=2),
                        whiskerprops=dict(color=C["muted"], linewidth=1.5),
                        capprops=dict(color=C["muted"], linewidth=1.5),
                        flierprops=dict(marker="o", markerfacecolor=C["border"], markersize=3, alpha=0.3, markeredgecolor="none"))
        
        for patch, color in zip(bp["boxes"], cat_colors):
            patch.set_facecolor(color + "40")
            patch.set_edgecolor(color)
            patch.set_linewidth(2)
            
        ax.set_xticklabels(short_lbl, fontsize=9)
        ax.set_ylim(0.5, 5.5)
        ax.grid(axis='x', alpha=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True); plt.close(fig)

    insight(
        f"Analisis regresi menunjukkan korelasi negatif yang valid (<b>r = {corr_val:.2f}</b>) antara Lead Time pengiriman dengan CSAT (Customer Satisfaction). "
        "Distribusi box-plot secara jelas menunjukkan bahwa SLA di atas 15 hari memicu lonjakan ekstrem pada *rating* bintang 1. "
        "Memperbaiki *bottleneck* logistik *last-mile* adalah investasi langsung ke arah peningkatan kepuasan dan retensi."
    )
