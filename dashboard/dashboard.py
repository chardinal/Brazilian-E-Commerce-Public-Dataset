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
    page_title="Olist E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Color Palette ────────────────────────────────────────────
C = {
    "bg":       "#F8FAFC", # Sedikit dicerahkan ke nuansa Slate
    "white":    "#FFFFFF",
    "text":     "#1E293B", # Sedikit ditegaskan ke nuansa Slate gelap
    "muted":    "#64748B",
    "border":   "#E2E8F0",
    "primary":  "#2563EB",
    "green":    "#059669",
    "red":      "#DC2626",
    "amber":    "#D97706",
    "purple":   "#7C3AED",
    "teal":     "#0891B2",
    "chart":    ["#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED", "#0891B2"],
}

# ─── Chart defaults ───────────────────────────────────────────
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
    "grid.alpha":        0.8, # Dibuat sedikit transparan agar elegan
    "grid.linestyle":    "--", # Garis grid putus-putus
    "xtick.color":       C["muted"],
    "ytick.color":       C["muted"],
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "text.color":        C["text"],
    "legend.frameon":    False,
    "legend.fontsize":   9,
    "font.family":       "sans-serif",
    "figure.dpi":        300, # INI PENTING: Bikin grafik resolusi tinggi & tajam
})

# ─── Global CSS ───────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    background-color: {C['bg']};
    color: {C['text']};
}}
.stApp {{ background-color: {C['bg']}; }}

/* Fix Material Icons */
[data-testid="stIconMaterial"] {{
    font-size: 0 !important;
    visibility: hidden;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {C['white']};
    border-right: 1px solid {C['border']};
    box-shadow: 2px 0 10px rgba(0,0,0,0.02); /* Bayangan halus sidebar */
}}
[data-testid="stSidebar"] * {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}

/* Page title */
.page-title {{
    font-size: 1.65rem;
    font-weight: 700;
    color: {C['text']};
    margin-bottom: 0.15rem;
    line-height: 1.3;
    letter-spacing: -0.02em;
}}
.page-sub {{
    font-size: 0.9rem;
    color: {C['muted']};
    margin-bottom: 2rem;
}}

/* KPI card */
.kpi {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 12px; /* Sudut lebih membulat */
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Bayangan default */
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}
.kpi:hover {{
    transform: translateY(-3px); /* Efek naik saat di-hover */
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    border-color: #93C5FD;
}}
.kpi-label {{
    font-size: 0.75rem;
    font-weight: 700;
    color: {C['muted']};
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
}}
.kpi-value {{
    font-size: 1.7rem;
    font-weight: 700;
    color: {C['text']};
    line-height: 1.1;
}}
.kpi-note {{
    font-size: 0.75rem;
    color: {C['muted']};
    margin-top: 0.4rem;
    font-weight: 500;
}}

/* Chart card */
.chart-card {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}}
.chart-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {C['text']};
    margin-bottom: 0.15rem;
}}
.chart-sub {{
    font-size: 0.8rem;
    color: {C['muted']};
    margin-bottom: 1rem;
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

/* Insight */
.insight {{
    background: linear-gradient(145deg, #F0F9FF 0%, #FFFFFF 100%);
    border-left: 4px solid {C['primary']};
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    font-size: 0.9rem;
    color: {C['text']};
    line-height: 1.6;
    margin-top: 1.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
}}
.insight b {{ color: {C['primary']}; font-weight: 600; }}

/* Segment badge */
.seg-badge {{
    display: inline-block;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    text-align: center;
    min-width: 100px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    transition: transform 0.2s;
}}
.seg-badge:hover {{ transform: scale(1.03); }}
.seg-badge .val {{
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.1;
}}
.seg-badge .lbl {{
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.2rem;
}}

/* Custom Box untuk Pertanyaan Bisnis */
.qa-box {{
    background: {C['white']}; 
    border: 1px solid {C['border']};
    border-radius: 10px; 
    padding: 1.25rem; 
    height: 100%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    transition: all 0.2s ease;
}}
.qa-box:hover {{
    box-shadow: 0 8px 12px rgba(0,0,0,0.08);
    transform: translateY(-2px);
    border-color: #BFDBFE;
}}

/* Divider */
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
    # Menambahkan icon bohlam agar terkesan lebih profesional
    st.markdown(f'<div class="insight">💡 <b>Business Insight:</b><br>{text}</div>', unsafe_allow_html=True)

def fig_clean(w=10, h=4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(C["white"])
    ax.set_facecolor(C["white"])
    return fig, ax

def fig_row(ncols, w=14, h=4.5):
    fig, axes = plt.subplots(1, ncols, figsize=(w, h))
    fig.patch.set_facecolor(C["white"])
    for ax in (axes if ncols > 1 else [axes]):
        ax.set_facecolor(C["white"])
    return fig, axes


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
        st.error(f"File tidak ditemukan: {e}\nJalankan notebook terlebih dahulu.")
        st.stop()

rev_df, rfm_df, mo_df, pay_df, del_df, main_df = load()

# ─── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem;">
        <div style="font-size:1.2rem; font-weight:800; color:#1E293B;">📊 Olist Dashboard</div>
        <div style="font-size:0.8rem; font-weight:500; color:#2563EB; margin-top:0.3rem;">Brazilian E-Commerce · Dicoding</div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    page = st.radio("Halaman", [
        "Overview",
        "Revenue per Kategori",
        "Segmentasi Pelanggan (RFM)",
        "Tren Bulanan",
        "Metode Pembayaran",
        "Pengiriman & Kepuasan",
    ], label_visibility="collapsed")

    st.divider()

    if "order_purchase_timestamp" in main_df.columns:
        st.markdown('<div style="font-size:0.8rem; font-weight:600; margin-bottom:0.5rem; color:#64748B;">FILTER TANGGAL TRANSAKSI</div>', unsafe_allow_html=True)
        mn = main_df["order_purchase_timestamp"].min().date()
        mx = main_df["order_purchase_timestamp"].max().date()
        dr = st.date_input("Pilih Tanggal", [mn, mx], min_value=mn, max_value=mx, label_visibility="collapsed")
    else:
        dr = None

    st.divider()
    st.markdown(f"""
    <div style="font-size:0.75rem; color:#64748B; line-height:1.7; text-align:center;">
        <b style="color:#1E293B;">Sumber Data</b><br>
        Olist Brazilian E-Commerce<br>
        Kaggle Public Dataset
    </div>""", unsafe_allow_html=True)

# Date filter
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
if page == "Overview":
    st.markdown('<div class="page-title">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Ringkasan performa bisnis Olist E-Commerce</div>', unsafe_allow_html=True)

    total_rev   = mf["revenue"].sum()
    total_ord   = mf["order_id"].nunique()
    total_cust  = mf["customer_unique_id"].nunique() if "customer_unique_id" in mf.columns else 0
    avg_score   = mf["review_score"].mean() if "review_score" in mf.columns else 0
    avg_del     = mf["delivery_days"].mean() if "delivery_days" in mf.columns else 0
    avg_ticket  = total_rev / total_ord if total_ord else 0

    section("RINGKASAN UTAMA")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Total Revenue",       f"R${total_rev/1e6:.2f}M")
    with c2: kpi("Total Orders",        f"{total_ord:,}")
    with c3: kpi("Unique Customers",    f"{total_cust:,}")
    with c4: kpi("Avg Review Score",    f"{avg_score:.2f} / 5")
    with c5: kpi("Avg Delivery",        f"{avg_del:.1f} hari")

    st.markdown("<br>", unsafe_allow_html=True)
    section("TREN & DISTRIBUSI PEMBAYARAN")

    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown('<div class="chart-title">Tren Orders Bulanan</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Jumlah pesanan unik per bulan beserta 3-month moving average</div>', unsafe_allow_html=True)
        if "year_month_str" in mo_df.columns:
            fig, ax = fig_clean(9, 3.5)
            x = np.arange(len(mo_df))
            ax.bar(x, mo_df["total_orders"], color=C["primary"], alpha=0.25, width=0.7)
            ax.plot(x, mo_df["total_orders"], color=C["primary"], linewidth=1.5, marker='o', markersize=3, label="Orders")
            if "orders_MA3" in mo_df.columns:
                ax.plot(x, mo_df["orders_MA3"], color=C["amber"], linewidth=1.8,
                        linestyle="--", label="3-Month MA")
            step = max(1, len(mo_df) // 8)
            ax.set_xticks(x[::step])
            ax.set_xticklabels(mo_df["year_month_str"].iloc[::step], rotation=35)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1e3:.0f}K" if v >= 1000 else f"{v:.0f}"))
            ax.set_ylabel("Orders")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig); plt.close()

    with col_r:
        st.markdown('<div class="chart-title">Metode Pembayaran</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Proporsi berdasarkan jumlah transaksi</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(5, 3.5)
        wedges, _, autotexts = ax.pie(
            pay_df["count"], labels=None,
            autopct="%1.1f%%",
            colors=C["chart"][:len(pay_df)],
            startangle=90, pctdistance=0.75,
            wedgeprops=dict(width=0.55, edgecolor="white", linewidth=1.5),
        )
        for at in autotexts:
            at.set_color('white')
            at.set_weight('bold')
            at.set_fontsize(8.5)
        ax.legend(wedges, pay_df["payment_type"].str.replace("_", " ").str.title(),
                  loc="lower center", bbox_to_anchor=(0.5, -0.15),
                  ncol=2, fontsize=8, frameon=False)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    section("PERTANYAAN BISNIS")
    questions = [
        ("📦", "Revenue per Kategori",
         "Kategori produk mana yang menghasilkan pendapatan tertinggi dan terendah?"),
        ("👥", "Segmentasi RFM",
         "Bagaimana karakteristik pelanggan berdasarkan Recency, Frequency, dan Monetary?"),
        ("📈", "Tren Bulanan",
         "Bagaimana tren jumlah pesanan dan revenue dari bulan ke bulan?"),
        ("💳", "Metode Pembayaran",
         "Metode pembayaran apa yang paling dominan digunakan pelanggan?"),
        ("🚚", "Pengiriman & Kepuasan",
         "Apakah lama pengiriman berkorelasi dengan review score pelanggan?"),
    ]
    q_cols = st.columns(5, gap="small")
    for col, (icon, title, desc) in zip(q_cols, questions):
        with col:
            st.markdown(f"""
            <div class="qa-box">
                <div style="font-size:1.6rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-size:0.85rem; font-weight:700; color:{C['text']};
                            margin-bottom:0.4rem; line-height:1.2;">{title}</div>
                <div style="font-size:0.75rem; color:{C['muted']}; line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# REVENUE PER KATEGORI
# ══════════════════════════════════════════════════════════════
elif page == "Revenue per Kategori":
    st.markdown('<div class="page-title">Revenue per Kategori Produk</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pertanyaan 1 — Kategori mana yang menghasilkan revenue tertinggi dan terendah?</div>', unsafe_allow_html=True)

    top1 = rev_df.iloc[0]
    bot1 = rev_df.iloc[-1]
    avg_rev_per_order = rev_df["avg_revenue_per_order"].mean()

    section("RINGKASAN")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Total Kategori",        f"{len(rev_df)}")
    with c2: kpi("Revenue Tertinggi",     f"R${top1['total_revenue']/1e6:.2f}M",
                                           top1["product_category_name_english"])
    with c3: kpi("Revenue Terendah",      f"R${bot1['total_revenue']:.0f}",
                                           bot1["product_category_name_english"])
    with c4: kpi("Avg Revenue per Order", f"R${avg_rev_per_order:.0f}")

    section("GRAFIK REVENUE")
    n = st.slider("Jumlah kategori yang ditampilkan", 5, 20, 10)

    top_n = rev_df.head(n).copy()
    bot_n = rev_df.tail(n).iloc[::-1].copy()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="chart-title">Top Kategori — Revenue Tertinggi</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(7, max(4, n * 0.45))
        colors = [C["primary"] if i == 0 else "#93C5FD" for i in range(n)]
        bars = ax.barh(top_n["product_category_name_english"],
                       top_n["total_revenue"], color=colors, height=0.6)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v/1e6:.1f}M"))
        ax.set_xlabel("Total Revenue")
        ax.invert_yaxis()
        ax.grid(axis="x"); ax.grid(axis="y", alpha=0)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + w * 0.01, bar.get_y() + bar.get_height() / 2,
                    f"R${w/1e6:.2f}M", va="center", fontsize=8.5, fontweight='500', color=C["text"])
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="chart-title">Bottom Kategori — Revenue Terendah</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(7, max(4, n * 0.45))
        colors = [C["red"] if i == 0 else "#FCA5A5" for i in range(n)]
        bars = ax.barh(bot_n["product_category_name_english"],
                       bot_n["total_revenue"], color=colors, height=0.6)
        ax.set_xlabel("Total Revenue")
        ax.invert_yaxis()
        ax.grid(axis="x"); ax.grid(axis="y", alpha=0)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + max(w * 0.02, 3), bar.get_y() + bar.get_height() / 2,
                    f"R${w:.0f}", va="center", fontsize=8.5, fontweight='500', color=C["text"])
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    section("VOLUME ORDER VS REVENUE")
    st.markdown('<div class="chart-title">Perbandingan Total Orders dan Revenue per Kategori (Top 15)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Membantu membedakan kategori yang populer vs kategori bernilai tinggi</div>', unsafe_allow_html=True)

    top15 = rev_df.head(15).copy()
    fig, ax1 = fig_clean(12, 4.5)
    ax2 = ax1.twinx()
    x = np.arange(len(top15))
    w = 0.4
    ax1.bar(x - w/2, top15["total_orders"], width=w, color=C["primary"],
            alpha=0.8, label="Total Orders")
    ax2.bar(x + w/2, top15["total_revenue"], width=w, color=C["green"],
            alpha=0.8, label="Total Revenue")
    ax1.set_xticks(x)
    ax1.set_xticklabels(top15["product_category_name_english"], rotation=35, ha="right", fontsize=8)
    ax1.set_ylabel("Jumlah Orders", color=C["primary"])
    ax2.set_ylabel("Total Revenue (BRL)", color=C["green"])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v/1e6:.1f}M"))
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    ax1.grid(axis="y", alpha=0.5); ax2.grid(False)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    with st.expander("Lihat tabel lengkap"):
        st.dataframe(
            rev_df.rename(columns={
                "product_category_name_english": "Kategori",
                "total_revenue":     "Total Revenue (BRL)",
                "total_orders":      "Total Orders",
                "avg_revenue_per_order": "Avg Rev/Order (BRL)",
            }).style
            .format({"Total Revenue (BRL)": "R${:,.0f}", "Avg Rev/Order (BRL)": "R${:,.0f}"})
            .background_gradient(subset=["Total Revenue (BRL)"], cmap="Blues"),
            use_container_width=True, height=320,
        )

    insight(
        "Kategori <b>health_beauty</b> dan <b>watches_gifts</b> memimpin dari sisi revenue. "
        "Grafik dual-axis menunjukkan bahwa kategori dengan order terbanyak belum tentu menghasilkan revenue tertinggi — "
        "beberapa kategori memiliki volume rendah namun nilai transaksi tinggi, mengindikasikan produk premium. "
        "Kategori dengan revenue terendah perlu dievaluasi: apakah kurang dipromosikan atau memang niche market yang sempit."
    )


# ══════════════════════════════════════════════════════════════
# SEGMENTASI RFM
# ══════════════════════════════════════════════════════════════
elif page == "Segmentasi Pelanggan (RFM)":
    st.markdown('<div class="page-title">Segmentasi Pelanggan (RFM)</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pertanyaan 2 — Karakteristik pelanggan berdasarkan Recency, Frequency, dan Monetary</div>', unsafe_allow_html=True)

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

    section("JUMLAH PELANGGAN PER SEGMEN")
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
                <div style="font-size:0.75rem; margin-top:0.15rem; opacity:0.85; font-weight:500;">{pct:.1f}%</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        section("DISTRIBUSI SEGMEN")
        st.markdown('<div class="chart-title">Proporsi Pelanggan per Segmen</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(6, 5)
        seg_colors = [SEG_COLOR.get(s, C["muted"]) for s in seg_df["segment"]]
        bars = ax.barh(seg_df["segment"], seg_df["Pelanggan"],
                       color=seg_colors, height=0.6)
        ax.invert_yaxis()
        ax.grid(axis="x"); ax.grid(axis="y", alpha=0)
        ax.set_xlabel("Jumlah Pelanggan")
        for bar, (_, row) in zip(bars, seg_df.iterrows()):
            pct = row["Pelanggan"] / total_cust_rfm * 100
            ax.text(bar.get_width() + total_cust_rfm * 0.005,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(row['Pelanggan']):,}  ({pct:.1f}%)",
                    va="center", fontsize=8.5, fontweight='500', color=C["text"])
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col2:
        section("NILAI RATA-RATA")
        st.markdown('<div class="chart-title">Avg Monetary Value per Segmen</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(6, 5)
        sorted_seg = seg_df.sort_values("Monetary")
        seg_colors_sorted = [SEG_COLOR.get(s, C["muted"]) for s in sorted_seg["segment"]]
        bars = ax.barh(sorted_seg["segment"], sorted_seg["Monetary"],
                       color=seg_colors_sorted, height=0.6)
        ax.set_xlabel("Avg Monetary Value (BRL)")
        ax.grid(axis="x"); ax.grid(axis="y", alpha=0)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + w * 0.01, bar.get_y() + bar.get_height() / 2,
                    f"R${w:.0f}", va="center", fontsize=8.5, fontweight='500', color=C["text"])
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    section("PERBANDINGAN DIMENSI RFM")
    st.markdown('<div class="chart-title">Rata-rata R, F, M per Segmen — Normalized (0–1)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Nilai dinormalisasi agar dapat dibandingkan antar dimensi yang berbeda skala</div>', unsafe_allow_html=True)

    rfm_norm = seg_df[["segment", "Recency", "Frequency", "Monetary"]].copy()
    for col in ["Recency", "Frequency", "Monetary"]:
        mi, mx = rfm_norm[col].min(), rfm_norm[col].max()
        rfm_norm[col] = (rfm_norm[col] - mi) / (mx - mi + 1e-9)
    rfm_norm["Recency"] = 1 - rfm_norm["Recency"]  # Invert: lower recency = better

    x = np.arange(len(rfm_norm))
    w = 0.25
    fig, ax = fig_clean(11, 4)
    seg_clr = [SEG_COLOR.get(s, C["muted"]) for s in rfm_norm["segment"]]
    ax.bar(x - w,   rfm_norm["Recency"],   width=w, color=C["primary"], alpha=0.9, label="Recency (inv.)")
    ax.bar(x,       rfm_norm["Frequency"], width=w, color=C["green"],   alpha=0.9, label="Frequency")
    ax.bar(x + w,   rfm_norm["Monetary"],  width=w, color=C["amber"],   alpha=0.9, label="Monetary")
    ax.set_xticks(x)
    ax.set_xticklabels(rfm_norm["segment"], rotation=20)
    ax.set_ylabel("Normalized Score (0–1)")
    ax.set_ylim(0, 1.15)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    with st.expander("Lihat tabel ringkasan segmen"):
        st.dataframe(
            seg_df.rename(columns={
                "segment": "Segmen", "Pelanggan": "Jumlah Pelanggan",
                "Recency": "Avg Recency (hari)", "Frequency": "Avg Frequency",
                "Monetary": "Avg Monetary (BRL)",
            }).style.format({"Avg Monetary (BRL)": "R${:,.2f}"}),
            use_container_width=True,
        )

    insight(
        "Segmen <b>Champions</b> memiliki nilai belanja tertinggi dan frekuensi pembelian terbaik — "
        "prioritaskan dengan program loyalitas eksklusif. "
        "Segmen <b>At Risk</b> pernah aktif namun sudah lama tidak bertransaksi — lakukan kampanye <i>win-back</i> sebelum mereka benar-benar pergi. "
        "Tingginya proporsi segmen <b>Lost</b> mengindikasikan rendahnya retensi pelanggan secara keseluruhan, "
        "yang umum terjadi pada e-commerce yang belum memiliki program loyalitas yang kuat."
    )


# ══════════════════════════════════════════════════════════════
# TREN BULANAN
# ══════════════════════════════════════════════════════════════
elif page == "Tren Bulanan":
    st.markdown('<div class="page-title">Tren Bulanan</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pertanyaan 3 — Tren jumlah pesanan dan total revenue dari bulan ke bulan</div>', unsafe_allow_html=True)

    best_ord_idx = mo_df["total_orders"].idxmax()
    best_rev_idx = mo_df["total_revenue"].idxmax()
    growth_rev   = (mo_df["total_revenue"].iloc[-1] - mo_df["total_revenue"].iloc[0]) / mo_df["total_revenue"].iloc[0] * 100

    section("RINGKASAN")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Total Revenue",       f"R${mo_df['total_revenue'].sum()/1e6:.2f}M")
    with c2: kpi("Total Orders",        f"{int(mo_df['total_orders'].sum()):,}")
    with c3: kpi("Bulan Terbaik",       mo_df.loc[best_rev_idx, 'year_month_str'],
                                         f"R${mo_df.loc[best_rev_idx,'total_revenue']/1e6:.2f}M revenue")
    with c4: kpi("Pertumbuhan",         f"{growth_rev:+.0f}%", "First vs Last Month")

    mo_df["rev_growth"] = mo_df["total_revenue"].pct_change() * 100

    show_ma = st.checkbox("Tampilkan 3-Month Moving Average", value=True)

    section("TREN ORDERS & REVENUE")

    # Orders trend
    st.markdown('<div class="chart-title">Jumlah Pesanan per Bulan</div>', unsafe_allow_html=True)
    fig, ax = fig_clean(13, 3.8)
    x = np.arange(len(mo_df))
    ax.bar(x, mo_df["total_orders"], color=C["primary"], alpha=0.25, width=0.7)
    ax.plot(x, mo_df["total_orders"], color=C["primary"], linewidth=2, marker='o', markersize=4, label="Jumlah Orders")
    if show_ma and "orders_MA3" in mo_df.columns:
        ax.plot(x, mo_df["orders_MA3"], color=C["amber"], linewidth=2,
                linestyle="--", label="3-Month MA")

    # Annotate peak
    peak_x = mo_df["total_orders"].idxmax()
    ax.annotate(
        f"Peak\n{int(mo_df['total_orders'].max()):,}",
        xy=(peak_x, mo_df["total_orders"].max()),
        xytext=(peak_x + 1.5, mo_df["total_orders"].max() * 1.05),
        fontsize=8.5, color=C["text"], fontweight='bold',
        arrowprops=dict(arrowstyle="->", color=C["text"], lw=1.2),
    )

    step = max(1, len(mo_df) // 10)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(mo_df["year_month_str"].iloc[::step], rotation=35)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1e3:.0f}K" if v >= 1000 else f"{v:.0f}"))
    ax.set_ylabel("Jumlah Orders")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    # Revenue trend
    st.markdown('<div class="chart-title">Total Revenue per Bulan</div>', unsafe_allow_html=True)
    fig, ax = fig_clean(13, 3.8)
    ax.bar(x, mo_df["total_revenue"], color=C["green"], alpha=0.25, width=0.7)
    ax.plot(x, mo_df["total_revenue"], color=C["green"], linewidth=2, marker='o', markersize=4, label="Total Revenue")
    if show_ma and "revenue_MA3" in mo_df.columns:
        ax.plot(x, mo_df["revenue_MA3"], color=C["amber"], linewidth=2,
                linestyle="--", label="3-Month MA")
    ax.set_xticks(x[::step])
    ax.set_xticklabels(mo_df["year_month_str"].iloc[::step], rotation=35)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v/1e6:.1f}M"))
    ax.set_ylabel("Revenue (BRL)")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    section("GROWTH RATE BULANAN")
    st.markdown('<div class="chart-title">Month-over-Month Revenue Growth (%)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Batang hijau = pertumbuhan positif, merah = pertumbuhan negatif</div>', unsafe_allow_html=True)

    fig, ax = fig_clean(13, 3.2)
    growth_vals = mo_df["rev_growth"].iloc[1:].values
    bar_colors  = [C["green"] if v >= 0 else C["red"] for v in growth_vals]
    ax.bar(range(len(growth_vals)), growth_vals, color=bar_colors, width=0.7, alpha=0.9)
    ax.axhline(0, color=C["text"], linewidth=1, linestyle="-")
    ax.set_xticks(range(0, len(growth_vals), step))
    ax.set_xticklabels(mo_df["year_month_str"].iloc[1::step], rotation=35)
    ax.set_ylabel("Growth Rate (%)")
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    with st.expander("Lihat data tren bulanan"):
        st.dataframe(
            mo_df[["year_month_str", "total_orders", "total_revenue", "rev_growth"]].rename(columns={
                "year_month_str": "Bulan",
                "total_orders":  "Orders",
                "total_revenue": "Revenue (BRL)",
                "rev_growth":    "MoM Growth (%)",
            }).style.format({
                "Revenue (BRL)":   "R${:,.0f}",
                "MoM Growth (%)":  "{:+.1f}%",
            }),
            use_container_width=True, height=300,
        )

    insight(
        "Tren pertumbuhan secara keseluruhan <b>positif</b> dari 2016 hingga pertengahan 2018. "
        "Lonjakan signifikan pada <b>November 2017</b> kemungkinan besar disebabkan oleh event <i>Black Friday</i> Brasil. "
        "Moving average menunjukkan bahwa pertumbuhan tersebut bersifat struktural, bukan sekadar anomali sesaat. "
        "Growth rate MoM yang berfluktuasi besar di awal 2016 mencerminkan fase <i>early growth</i>, "
        "sementara fase 2017–2018 memperlihatkan pertumbuhan yang lebih stabil dan matang."
    )


# ══════════════════════════════════════════════════════════════
# METODE PEMBAYARAN
# ══════════════════════════════════════════════════════════════
elif page == "Metode Pembayaran":
    st.markdown('<div class="page-title">Metode Pembayaran</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pertanyaan 4 — Metode pembayaran dominan dan rata-rata nilai transaksi per metode</div>', unsafe_allow_html=True)

    dom = pay_df.loc[pay_df["count"].idxmax()]
    hi_avg = pay_df.loc[pay_df["avg_value"].idxmax()]

    section("RINGKASAN")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Metode Dominan",        dom["payment_type"].replace("_", " ").title(),
                                           f"{dom['pct']:.1f}% dari total transaksi")
    with c2: kpi("Total Transaksi",        f"{int(pay_df['count'].sum()):,}")
    with c3: kpi("Avg Value Tertinggi",    f"R${hi_avg['avg_value']:.0f}",
                                           hi_avg["payment_type"].replace("_", " ").title())
    with c4: kpi("Total Nilai Transaksi",  f"R${pay_df['total_value'].sum()/1e6:.2f}M")

    section("ANALISIS PEMBAYARAN")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="chart-title">Jumlah Transaksi per Metode Pembayaran</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(6.5, 4.5)
        sorted_count = pay_df.sort_values("count")
        colors_count = [C["primary"] if i == len(sorted_count) - 1 else "#93C5FD"
                        for i in range(len(sorted_count))]
        bars = ax.barh(
            sorted_count["payment_type"].str.replace("_", " ").str.title(),
            sorted_count["count"],
            color=colors_count, height=0.55,
        )
        ax.set_xlabel("Jumlah Transaksi")
        ax.grid(axis="x"); ax.grid(axis="y", alpha=0)
        for bar, (_, row) in zip(bars, sorted_count.iterrows()):
            w = bar.get_width()
            ax.text(w + pay_df["count"].max() * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(w):,}  ({row['pct']:.1f}%)",
                    va="center", fontsize=9, fontweight='500', color=C["text"])
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="chart-title">Rata-rata Nilai Transaksi per Metode</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(6.5, 4.5)
        sorted_avg = pay_df.sort_values("avg_value")
        colors_avg = [C["green"] if i == len(sorted_avg) - 1 else "#6EE7B7"
                      for i in range(len(sorted_avg))]
        bars = ax.barh(
            sorted_avg["payment_type"].str.replace("_", " ").str.title(),
            sorted_avg["avg_value"],
            color=colors_avg, height=0.55,
        )
        ax.set_xlabel("Avg Transaction Value (BRL)")
        ax.grid(axis="x"); ax.grid(axis="y", alpha=0)
        for bar, (_, row) in zip(bars, sorted_avg.iterrows()):
            w = bar.get_width()
            ax.text(w + pay_df["avg_value"].max() * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"R${w:.0f}", va="center", fontsize=9, fontweight='500', color=C["text"])
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    section("TOTAL NILAI PER METODE")
    st.markdown('<div class="chart-title">Total Nilai Seluruh Transaksi per Metode Pembayaran</div>', unsafe_allow_html=True)
    fig, ax = fig_clean(10, 3.5)
    sorted_total = pay_df.sort_values("total_value", ascending=False)
    colors_total = [C["primary"], "#93C5FD", "#BFDBFE", "#DBEAFE"][:len(sorted_total)]
    bars = ax.bar(
        sorted_total["payment_type"].str.replace("_", " ").str.title(),
        sorted_total["total_value"],
        color=colors_total, width=0.5,
    )
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v/1e6:.1f}M"))
    ax.set_ylabel("Total Value (BRL)")
    ax.grid(axis="y"); ax.grid(axis="x", alpha=0)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + pay_df["total_value"].max() * 0.01,
                f"R${h/1e6:.2f}M", ha="center", fontsize=9.5,
                fontweight="bold", color=C["text"])
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    with st.expander("Lihat tabel detail"):
        st.dataframe(
            pay_df.rename(columns={
                "payment_type":  "Metode",
                "count":         "Jumlah Transaksi",
                "avg_value":     "Avg Value (BRL)",
                "total_value":   "Total Value (BRL)",
                "pct":           "Share (%)",
            }).style.format({
                "Avg Value (BRL)":   "R${:,.2f}",
                "Total Value (BRL)": "R${:,.2f}",
                "Share (%)":         "{:.1f}%",
            }),
            use_container_width=True,
        )

    insight(
        "<b>Credit card</b> mendominasi lebih dari 70% transaksi dengan nilai total terbesar. "
        "Ini konsisten dengan kebiasaan konsumen Brasil yang memanfaatkan fitur cicilan kartu kredit untuk pembelian besar. "
        "<b>Boleto</b> menjadi alternatif populer bagi segmen tanpa akses kartu kredit. "
        "Meski <b>voucher</b> jarang digunakan, rata-rata nilainya rendah karena berfungsi sebagai instrumen diskon, bukan pembayaran penuh."
    )


# ══════════════════════════════════════════════════════════════
# PENGIRIMAN & KEPUASAN
# ══════════════════════════════════════════════════════════════
elif page == "Pengiriman & Kepuasan":
    st.markdown('<div class="page-title">Pengiriman & Kepuasan Pelanggan</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Pertanyaan 5 — Apakah lama waktu pengiriman berkorelasi dengan review score pelanggan?</div>', unsafe_allow_html=True)

    corr_val = del_df["delivery_days"].corr(del_df["review_score"])
    fast_pct = (del_df["delivery_days"] <= 7).mean() * 100

    section("RINGKASAN")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Pearson Correlation",     f"{corr_val:.3f}",
                                             "Negatif = makin lama → makin rendah skor")
    with c2: kpi("Avg Lama Pengiriman",      f"{del_df['delivery_days'].mean():.1f} hari")
    with c3: kpi("Avg Review Score",         f"{del_df['review_score'].mean():.2f} / 5")
    with c4: kpi("Order Terkirim ≤7 Hari",   f"{fast_pct:.1f}%")

    order_cat   = ["1-Fast (≤7 days)", "2-Normal (8-14 days)", "3-Slow (15-21 days)", "4-Very Slow (>21 days)"]
    short_lbl   = ["≤7 hari\n(Cepat)", "8–14 hari\n(Normal)", "15–21 hari\n(Lambat)", ">21 hari\n(Sangat Lambat)"]
    cat_colors  = [C["green"], C["teal"], C["amber"], C["red"]]
    plot_data   = del_df[del_df["delivery_category"].isin(order_cat)].copy()

    section("ANALISIS KECEPATAN PENGIRIMAN")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="chart-title">Rata-rata Review Score per Kategori Pengiriman</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Semakin cepat pengiriman, semakin tinggi skor kepuasan</div>', unsafe_allow_html=True)
        stats = plot_data.groupby("delivery_category").agg(
            avg=("review_score", "mean"),
            n=("order_id", "count"),
        ).reindex(order_cat).reset_index()

        fig, ax = fig_clean(6.5, 4.5)
        bars = ax.bar(range(4), stats["avg"], color=cat_colors, width=0.55)
        avg_global = del_df["review_score"].mean()
        ax.axhline(avg_global, color=C["text"], linewidth=1.5, linestyle="--",
                   label=f"Rata-rata keseluruhan ({avg_global:.2f})")
        ax.set_xticks(range(4))
        ax.set_xticklabels(short_lbl, fontsize=9, fontweight='500')
        ax.set_ylabel("Avg Review Score")
        ax.set_ylim(1, 5.2)
        ax.legend(loc="upper right")
        ax.grid(axis="y"); ax.grid(axis="x", alpha=0)
        for i, (bar, row) in enumerate(zip(bars, stats.itertuples())):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    f"{row.avg:.2f}", ha="center", fontsize=11,
                    fontweight="bold", color=cat_colors[i])
            ax.text(bar.get_x() + bar.get_width() / 2, 0.5,
                    f"n={row.n:,}", ha="center", fontsize=8, color="white", fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="chart-title">Distribusi Review Score per Kategori (Box Plot)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Menunjukkan sebaran dan variasi skor kepuasan</div>', unsafe_allow_html=True)
        fig, ax = fig_clean(6.5, 4.5)
        box_data = [
            plot_data[plot_data["delivery_category"] == c]["review_score"].dropna().values
            for c in order_cat
        ]
        bp = ax.boxplot(
            box_data, patch_artist=True, notch=False,
            medianprops=dict(color=C["text"], linewidth=2),
            whiskerprops=dict(color=C["muted"], linewidth=1.5),
            capprops=dict(color=C["muted"], linewidth=1.5),
            flierprops=dict(marker="o", markerfacecolor=C["border"],
                            markersize=3, alpha=0.5, markeredgecolor="none"),
        )
        for patch, color in zip(bp["boxes"], cat_colors):
            patch.set_facecolor(color + "40")
            patch.set_edgecolor(color)
            patch.set_linewidth(1.8)
        ax.set_xticklabels(short_lbl, fontsize=9, fontweight='500')
        ax.set_ylabel("Review Score")
        ax.set_ylim(0.5, 5.8)
        ax.grid(axis="y"); ax.grid(axis="x", alpha=0)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    section("KORELASI: LAMA PENGIRIMAN vs REVIEW SCORE")
    st.markdown('<div class="chart-title">Scatter Plot — Setiap Titik Mewakili Satu Order</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Garis putus-putus menunjukkan arah tren linear keseluruhan</div>', unsafe_allow_html=True)

    sample = del_df.sample(min(6000, len(del_df)), random_state=42)
    cat_map = {c: i for i, c in enumerate(order_cat)}
    dot_colors = [
        cat_colors[cat_map[c]] if c in cat_map else C["muted"]
        for c in sample["delivery_category"]
    ]

    fig, ax = fig_clean(12, 4.5)
    ax.scatter(sample["delivery_days"], sample["review_score"],
               c=dot_colors, alpha=0.25, s=12, edgecolors="none")

    # Regression line
    z = np.polyfit(sample["delivery_days"], sample["review_score"], 1)
    xl = np.linspace(0, del_df["delivery_days"].quantile(0.99), 200)
    ax.plot(xl, np.poly1d(z)(xl), color=C["text"], linewidth=2.5,
            linestyle="--", label=f"Tren linear  (r = {corr_val:.3f})")

    # Legend
    import matplotlib.patches as mpatches
    legend_patches = [
        mpatches.Patch(color=cat_colors[i], label=short_lbl[i].replace("\n", " "))
        for i in range(4)
    ]
    ax.legend(handles=legend_patches + [
        plt.Line2D([0], [0], color=C["text"], linewidth=2.5,
                   linestyle="--", label=f"Tren (r={corr_val:.3f})")
    ], fontsize=9, ncol=5, loc="upper right")

    ax.set_xlabel("Lama Pengiriman (Hari)")
    ax.set_ylabel("Review Score")
    ax.set_xlim(-1, del_df["delivery_days"].quantile(0.99) + 2)
    ax.set_ylim(0.5, 5.5)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    insight(
        f"Terdapat korelasi negatif antara lama pengiriman dan kepuasan pelanggan (<b>r = {corr_val:.3f}</b>). "
        "Meskipun korelasinya tergolong lemah secara statistik, pola yang terlihat konsisten: "
        "pengiriman <b>≤7 hari</b> menghasilkan rata-rata review score tertinggi, "
        "sementara pengiriman <b>>21 hari</b> secara konsisten mendapatkan skor di bawah rata-rata. "
        "Ini mengindikasikan bahwa mempercepat pengiriman adalah salah satu lever paling efektif "
        "untuk meningkatkan kepuasan pelanggan secara langsung."
    )


# ─── Footer ───────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top: 1px solid {C['border']}; padding-top: 1rem; margin-top: 1rem;
            font-size: 0.8rem; color: {C['muted']}; text-align: center; font-weight:500;">
    Dashboard Analisis Data · Olist Brazilian E-Commerce ·
    Chardinal Martin Butarbutar · Dicoding Data Analysis Project
</div>""", unsafe_allow_html=True)
