import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# -------------------------------------------------------------
# 1. SAHIFA SOZLAMALARI
# -------------------------------------------------------------
st.set_page_config(
    page_title="Savdo Tahlili va Xarid Bashorati Dashboardi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Maxsus CSS uslublar
st.markdown("""
    <style>
    .metric-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-val {
        font-size: 24px;
        font-weight: bold;
        color: #111;
    }
    .metric-lbl {
        font-size: 14px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# 2. MA'LUMOTLARNI YUKLASH VA TOZALASH
# -------------------------------------------------------------
@st.cache_data
def load_and_clean_data():
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else '.'
    file_path = os.path.join(current_dir, 'dataset.csv')

    if not os.path.exists(file_path):
        file_path = 'dataset.csv'

    df = pd.read_csv(file_path)

    # Missing value tozalash (yangi o'zgaruvchisiz)
    df['promo_active'] = df['promo_active'].fillna(False).astype(bool)
    df['customer_rating'] = df['customer_rating'].fillna(
        df.groupby('category')['customer_rating'].transform('median')
    )
    df['competitor_price_index'] = df['competitor_price_index'].fillna(
        df.groupby('category')['competitor_price_index'].transform('median')
    )

    # Davr ustuni
    df['period'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
    df['net_operating_revenue'] = df['monthly_revenue'] - df['marketing_spend']
    return df


try:
    df = load_and_clean_data()
except Exception as e:
    st.error(f"⚠️ Ma'lumotlarni yuklashda xatolik yuz berdi: {e}")
    st.stop()

# -------------------------------------------------------------
# 3. YON PANEL (FILTRLAR)
# -------------------------------------------------------------
st.sidebar.header("🔍 Filtrlar")

selected_years = st.sidebar.multiselect(
    "Yilni tanlang:",
    options=sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

selected_regions = st.sidebar.multiselect(
    "Hududlarni tanlang:",
    options=sorted(df['region'].unique()),
    default=sorted(df['region'].unique())
)

selected_categories = st.sidebar.multiselect(
    "Mahsulot toifalarini tanlang:",
    options=sorted(df['category'].unique()),
    default=sorted(df['category'].unique())
)

selected_store_types = st.sidebar.multiselect(
    "Savdo kanalini tanlang:",
    options=sorted(df['store_type'].unique()),
    default=sorted(df['store_type'].unique())
)

# Filtrlash
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['category'].isin(selected_categories)) &
    (df['store_type'].isin(selected_store_types))
    ]

if filtered_df.empty:
    st.warning("Tanlangan filtrlar bo'yicha hech qanday ma'lumot topilmadi!")
    st.stop()

# -------------------------------------------------------------
# 4. ASOSIY METRIKALAR (KPIs)
# -------------------------------------------------------------
st.title("📊 Elektronika Savdosi va Ta'minot Tahlili")
st.markdown("Hududlar, toifalar va savdo kanallari kesimidagi real ko'rsatkichlar va xarid bashorati")

total_rev = filtered_df['monthly_revenue'].sum()
total_net = filtered_df['net_operating_revenue'].sum()
total_units = filtered_df['units_sold'].sum()
total_mktg = filtered_df['marketing_spend'].sum()
avg_rating = filtered_df['customer_rating'].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-lbl">Umumiy Tushum</div>
            <div class="metric-val">${total_rev / 1e6:,.2f} Mln</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-lbl">Sof Operatsion Tushum</div>
            <div class="metric-val">${total_net / 1e6:,.2f} Mln</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-lbl">Sotilgan Tovarlar Soni</div>
            <div class="metric-val">{total_units:,.0f} dona</div>
        </div>
    """, unsafe_allow_html=True)
with c4:
    roas = total_rev / total_mktg if total_mktg > 0 else 0
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-lbl">Marketing ROAS</div>
            <div class="metric-val">{roas:,.1f}x</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------------
# 5. GRAFIKLAR: DINAMIKA VA TAHLIL
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Savdo Dinamikasi", "💰 Marja va Sof Daromad", "📦 Xarid Bashorati & Byudjet"])

with tab1:
    col_t1, col_t2 = st.columns([7, 5])

    with col_t1:
        st.subheader("Do'kon turlari bo'yicha oylik tushum dinamikasi")
        trend_df = filtered_df.pivot_table(
            index='period',
            columns='store_type',
            values='monthly_revenue',
            aggfunc='sum'
        ).reset_index()

        fig_trend = px.line(
            trend_df,
            x='period',
            y=[col for col in trend_df.columns if col != 'period'],
            labels={'value': 'Tushum ($)', 'period': 'Davr', 'variable': "Do'kon turi"},
            markers=True
        )
        fig_trend.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_t2:
        st.subheader("Hududlar bo'yicha tushum ulushi")
        reg_pie = filtered_df.groupby('region')['monthly_revenue'].sum().reset_index()
        fig_pie = px.pie(
            reg_pie,
            names='region',
            values='monthly_revenue',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Hududlar va toifalar kesimida tushum (Issiqlik xaritasi)")
    pivot_heat = (filtered_df.pivot_table(
        index='region',
        columns='category',
        values='monthly_revenue',
        aggfunc='sum'
    ) / 1e6).fillna(0)

    fig_heat = px.imshow(
        pivot_heat,
        text_auto=".2f",
        labels=dict(x="Mahsulot toifasi", y="Hudud", color="Mln USD"),
        color_continuous_scale="YlGnBu",
        aspect="auto"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with tab2:
    st.subheader("Mahsulot toifalari bo'yicha daromad va 1 dona mahsulot marjasi")

    cat_summary = filtered_df.groupby('category').agg(
        total_rev=('monthly_revenue', 'sum'),
        total_mktg=('marketing_spend', 'sum'),
        total_units=('units_sold', 'sum')
    ).reset_index()

    cat_summary['net_rev'] = cat_summary['total_rev'] - cat_summary['total_mktg']
    cat_summary['per_unit_net'] = cat_summary['net_rev'] / cat_summary['total_units']
    cat_summary = cat_summary.sort_values(by='net_rev', ascending=False)

    fig_margin = go.Figure()
    fig_margin.add_trace(go.Bar(
        x=cat_summary['category'],
        y=cat_summary['net_rev'] / 1e6,
        name='Sof tushum (Mln $)',
        marker_color='steelblue',
        yaxis='y1'
    ))
    fig_margin.add_trace(go.Scatter(
        x=cat_summary['category'],
        y=cat_summary['per_unit_net'],
        name='1 dona sof marja ($)',
        mode='lines+markers',
        line=dict(color='firebrick', width=3),
        yaxis='y2'
    ))
    fig_margin.update_layout(
        yaxis=dict(title='Sof tushum (Mln USD)'),
        yaxis2=dict(title='Birlik tushum ($/dona)', overlaying='y', side='right'),
        legend=dict(x=0.8, y=1.1),
        height=450
    )
    st.plotly_chart(fig_margin, use_container_width=True)

    st.dataframe(
        cat_summary.rename(columns={
            'category': 'Toifa',
            'total_rev': 'Jami tushum ($)',
            'total_mktg': 'Marketing xarajati ($)',
            'total_units': 'Sotilgan dona',
            'net_rev': 'Sof tushum ($)',
            'per_unit_net': '1 donadan tushum ($)'
        }).style.format({
            'Jami tushum ($)': "${:,.2f}",
            'Marketing xarajati ($)': "${:,.2f}",
            'Sotilgan dona': "{:,.0f}",
            'Sof tushum ($)': "${:,.2f}",
            '1 donadan tushum ($)': "${:,.2f}"
        }),
        use_container_width=True
    )

with tab3:
    st.subheader("Keyingi oy uchun tavsiya etilgan xarid hajmi va aylanma byudjet")

    c_calc1, c_calc2 = st.columns(2)
    with c_calc1:
        cost_ratio = st.slider("Xarid tannarxi ulushi (Chakana narxga nisbatan % da):", 50, 95, 75, step=5)
    with c_calc2:
        service_level = st.selectbox("Xizmat ko'rsatish darajasi (Zaxira ishonchliligi):", [
            ("95% (Z=1.65) - Standart xavfsizlik", 1.65),
            ("99% (Z=2.33) - Maksimal kafolat", 2.33),
            ("90% (Z=1.28) - Tejamkor zaxira", 1.28)
        ], index=0)

    # 2024 yil talabi asosida xarid hisobi
    df_recent = df[df['year'] == 2024]

    proc_calc = df_recent.groupby('category')['units_sold'].agg(
        monthly_avg=lambda x: x.sum() / 12,
        std_monthly=lambda x: (x.groupby(df_recent['month']).sum()).std()
    ).reset_index()

    proc_calc['safety_stock'] = np.round(service_level[1] * proc_calc['std_monthly']).astype(int)
    proc_calc['recommended_order'] = np.ceil(proc_calc['monthly_avg'] + proc_calc['safety_stock']).astype(int)

    prices_2024 = df_recent.groupby('category')['avg_unit_price'].mean().reset_index()
    proc_calc = pd.merge(proc_calc, prices_2024, on='category')

    proc_calc['retail_value'] = proc_calc['recommended_order'] * proc_calc['avg_unit_price']
    proc_calc['budget_needed'] = proc_calc['retail_value'] * (cost_ratio / 100.0)

    total_order_units = proc_calc['recommended_order'].sum()
    total_budget_needed = proc_calc['budget_needed'].sum()

    b1, b2 = st.columns(2)
    with b1:
        st.info(f"📦 **Jami xarid qilinadigan hajm:** `{total_order_units:,.0f} dona`")
    with b2:
        st.success(f"💵 **Talab etiladigan aylanma mablag' ({cost_ratio}%):** `${total_budget_needed:,.2f}`")

    st.dataframe(
        proc_calc[['category', 'monthly_avg', 'safety_stock', 'recommended_order', 'avg_unit_price', 'budget_needed']]
        .rename(columns={
            'category': 'Mahsulot toifasi',
            'monthly_avg': "O'rtacha oylik talab",
            'safety_stock': "Xavfsizlik zaxirasi",
            'recommended_order': "Tavsiya etilgan buyurtma (dona)",
            'avg_unit_price': "Chakana narx ($)",
            'budget_needed': f"Xarid byudjeti ({cost_ratio}%) ($)"
        })
        .style.format({
            "O'rtacha oylik talab": "{:,.1f}",
            "Xavfsizlik zaxirasi": "{:,.0f}",
            "Tavsiya etilgan buyurtma (dona)": "{:,.0f}",
            "Chakana narx ($)": "${:,.2f}",
            f"Xarid byudjeti ({cost_ratio}%) ($)": "${:,.2f}"
        }),
        use_container_width=True
    )