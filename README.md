# 🛍️ Proyek Analisis Data: Brazilian E-Commerce Public Dataset

Dashboard interaktif untuk menganalisis data transaksi e-commerce Brasil dari platform Olist.


---

## 📊 Pertanyaan Bisnis

1. Kategori produk apa yang menghasilkan total pendapatan (*revenue*) tertinggi dan terendah?
2. Bagaimana karakteristik segmentasi pelanggan berdasarkan analisis RFM (Recency, Frequency, Monetary)?
3. Bagaimana tren jumlah pesanan dan total pendapatan dari bulan ke bulan?
4. Metode pembayaran apa yang paling dominan digunakan oleh pelanggan?
5. Apakah terdapat korelasi antara lama waktu pengiriman dengan tingkat kepuasan pelanggan (*review score*)?

---

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── dashboard.py                 # File utama Streamlit
│   ├── revenue_by_category.csv      # Data revenue per kategori
│   ├── rfm_df.csv                   # Data segmentasi RFM
│   ├── monthly_trend.csv            # Data tren bulanan
│   ├── payment_freq.csv             # Data metode pembayaran
│   ├── delivery_review.csv          # Data pengiriman & review
│   └── main_df.csv                  # Data utama gabungan
├── E-Commerce_Public_Dataset/
│   ├── customers_dataset.csv
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── order_payments_dataset.csv
│   └── order_reviews_dataset.csv
├── Proyek_Analisis_Data.ipynb       # Notebook analisis lengkap
├── requirements.txt                 # Daftar library
└── README.md
```

---

## 🚀 Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`

---

## 🌐 Live Demo

Akses dashboard secara online:

**[🔗 Klik di sini untuk membuka dashboard]([https://nama-app.streamlit.app](https://project2-brazilian-e-commerce-public-dataset.streamlit.app/))**

---

## 📦 Library yang Digunakan

| Library | Versi | Kegunaan |
|---|---|---|
| `pandas` | 2.2.2 | Manipulasi & analisis data |
| `numpy` | 1.26.4 | Komputasi numerik |
| `matplotlib` | 3.9.2 | Visualisasi grafik |
| `seaborn` | 0.13.2 | Visualisasi statistik |
| `streamlit` | 1.40.1 | Web dashboard interaktif |

---

## 📈 Hasil Analisis

### 1. Revenue per Kategori
Kategori **health_beauty** dan **watches_gifts** menghasilkan revenue tertinggi. Kategori dengan revenue rendah perlu dievaluasi untuk pengembangan atau penghentian.

### 2. Segmentasi Pelanggan (RFM)
Mayoritas pelanggan masuk segmen **Lost**, menunjukkan rendahnya retensi. Segmen **Champions** meskipun kecil memiliki nilai belanja tertinggi dan harus diprioritaskan dengan program loyalitas.

### 3. Tren Bulanan
Tren pertumbuhan **positif** dari 2016 hingga 2018 dengan puncak di **November 2017**, kemungkinan karena event *Black Friday* Brasil.

### 4. Metode Pembayaran
**Credit card** mendominasi lebih dari 70% transaksi. *Boleto* menjadi alternatif populer bagi pelanggan tanpa kartu kredit.

### 5. Pengiriman & Kepuasan
Terdapat korelasi negatif antara lama pengiriman dan review score **(r = -0.35)**. Pengiriman ≤7 hari menghasilkan rata-rata review score tertinggi.

---

## 📋 Sumber Data

Dataset bersumber dari [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) yang tersedia di Kaggle.

Dataset mencakup **100.000+ transaksi** dari tahun 2016–2018 dengan informasi pelanggan, produk, pembayaran, pengiriman, dan ulasan.
