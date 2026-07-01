import os
import streamlit as st
import pandas as pd
from html import escape
import plotly.express as px
import datetime
import streamlit.components.v1 as components
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 1. Page Configuration
st.set_page_config(page_title="Sales & Audit Dashboard", page_icon="📊", layout="wide")

# 2. Premium Glassmorphism CSS Override (Inspired by css.glass)
st.markdown("""
    <style>
        /* Global Background - Rich Mesh Gradient to emphasize glass transparency */
        .stApp {
            background-color: #dfedd6 !important;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%), 
                radial-gradient(at 0% 100%, hsla(339,49%,21%,1) 0, transparent 50%), 
                radial-gradient(at 100% 100%, hsla(253,16%,7%,1) 0, transparent 50%) !important;
            background-attachment: fixed !important;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            color: #ffffff !important;
        }
        
        /* Typography overrides for dark mesh background visibility */
        .main-title {
            font-size: 42px;
            font-weight: 800;
            letter-spacing: -1.5px;
            color: #ffffff;
            margin-bottom: 2px;
            text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 16px;
            color: #cbd5e1;
            font-weight: 400;
            margin-bottom: 28px;
        }
        .section-title {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #ffffff;
            font-weight: 700;
            margin-bottom: 14px;
            margin-top: 10px;
        }
        h3 {
            color: #ffffff !important;
        }
            
        /* Authentic Glassmorphism Cards (Exact styling logic from css.glass) */
        .metric-card_Customer {
            background: #00000061 !important;
            box-shadow: 0 8px 32px 0 rgb(0 0 0 / 47%) !important;
            backdrop-filter: blur(13.5px) !important;
            -webkit-backdrop-filter: blur(13.5px) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            padding: 22px;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            min-height: 165px;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
        }
            
        .metric-card_Customer:hover {
            background: #0000008c !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45) !important;
            transform: translateY(-5px);
        }
        
        /* Update your existing metric-card class to this */
        .metric-card {
            background: #00000061 !important;
            box-shadow: 0 8px 32px 0 rgb(0 0 0 / 47%) !important;
            backdrop-filter: blur(13.5px) !important;
            -webkit-backdrop-filter: blur(13.5px) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            padding: 22px;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            min-height: 165px;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important; 
            align-items: center !important;     
        }
            
        .metric-card:hover {
            background: #0000008c !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45) !important;
            transform: translateY(-5px);
        }
        
        /* Update your existing metric-label class to this */
        .metric-label {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #ffffff;
            font-weight: 600;
            margin-bottom: 8px;
            text-align: center !important; 
        }
            
        .metric-value {
            font-size: 25px;
            color: #ffffff;
            font-weight: 800;
            letter-spacing: -0.5px;
            line-height: 1.1;
        }
        
        /* Vibrant neon glass accents for indicators */
        .accent-collected { color: #34d399 !important; text-shadow: 0 0 10px rgba(52,211,153,0.3); }
        .accent-alert { color: #f87171 !important; text-shadow: 0 0 10px rgba(248,113,113,0.3); }
        .accent-warn { color: #fbbf24 !important; text-shadow: 0 0 10px rgba(251,191,36,0.3); }
        .accent-Invoice { color: #60a5fa !important; text-shadow: 0 0 10px rgba(96,165,250,0.3); }
        
        /* Sub-layouts divider and fonts */
        .card-divider {
            margin: 12px 0 8px 0; 
            border: 0; 
            border-top: 1px solid rgba(255, 255, 255, 0.15);
        }
        .sub-grid {
            display: flex; 
            justify-content: space-between;
        }
        .sub-label {
            font-size: 10px; 
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #ffffff; 
            font-weight: 600;
        }
        .sub-val-green {
            font-weight: 700; 
            font-size: 20px; 
            color: #34d399;
        }
        .sub-val-red {
            font-weight: 700; 
            font-size: 20px; 
            color: #f87171;
        }
        
        /* Native Streamlit UI Form Inputs Glassmorphism Override */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            color: white !important;
        }
        div[data-testid="stSelectbox"] svg {
            fill: white !important;
        }
        div[data-testid="stSelectbox"] span {
            color: white !important;
        }

        div[data-testid="stDateInput"] > div {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }
        div[data-testid="stDateInput"] input {
            color: #000000 !important;
            background: transparent !important;
        }
        div[data-testid="stDateInput"] svg {
            fill: white !important;
        }

        .audit-note-card {
            background-color: rgb(255, 255, 255) !important;
            color: #111827 !important;
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 10px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
        }

        .chart-card {
            background: #00000061 !important;
            box-shadow: 0 8px 32px 0 rgb(0 0 0 / 47%) !important;
            backdrop-filter: blur(13.5px) !important;
            -webkit-backdrop-filter: blur(13.5px) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            margin-bottom: 10px;
        }

        .chart-card .stPlotlyChart {
            background: #00000061 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        .chart-title {
            text-align: center !important;
            color: #ffffff !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            padding: 10px !important;
        }

        /* Sidebar Navigation Glassmorphism Layout */
        [data-testid="stSidebar"] {
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #ffffff !important;
        }

        /* EXACT TEMPLATE LAYOUT CUSTOM DESIGN CLASSES */
        .template-report-container {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 4px solid #a4898982 !important;
            border-radius: 12px !important;
            padding: 40px !important;
            margin-bottom: 30px !important;
            font-family: 'Arial', sans-serif !important;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .template-field {
            font-size: 16px !important;
            font-weight: bold !important;
            color: #000000 !important;
            margin-bottom: 24px !important;
            line-height: 1.5 !important;
        }
        .template-value {
            font-weight: normal !important;
            color: #222222 !important;
            margin-left: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Load Data
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, 'sample.xlsx')
    
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Invoice Amount'] = pd.to_numeric(df['Invoice Amount'], errors='coerce').fillna(0)
    df['Amount Collected'] = pd.to_numeric(df['Amount Collected'], errors='coerce').fillna(0)
    df['Difference'] = pd.to_numeric(df['Difference'], errors='coerce').fillna(0)
    
    if 'Customer Yes/No' not in df.columns:
        df['Customer Yes/No'] = "Yes" 
        
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not find or parse 'sample.xlsx'. Please ensure it's in the root folder.")
    st.stop()

# ==========================================
# 4. Multi-Page Navigation Configuration
# ==========================================
st.sidebar.markdown("### 🗺️ Navigation Panel")
page = st.sidebar.selectbox("Go to Page:", ["📊 QA Dashboard", "🔍 Investigated Report"])
st.sidebar.markdown("---")

# 5. Top Controls (Identical Shared Filter Scope across both pages)
st.markdown("<div class='section-title'>🔍 Filter Scope</div>", unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    carriers = ["All Carriers"] + sorted(list(df['Carrier'].dropna().unique()))
    selected_carrier = st.selectbox("Carrier", carriers, label_visibility="collapsed")

with nav_col2:
    stores = ["All Stores"] + sorted(list(df['Store Name'].dropna().unique()))
    selected_store = st.selectbox("Store", stores, label_visibility="collapsed")

with nav_col3:
    invoices = ["All Invoices"] + sorted(list(df['Invoice'].dropna().unique()))
    selected_invoice = st.selectbox("Invoice", invoices, label_visibility="collapsed")

with nav_col4:
    sales_reps = ["All Sales Reps"] + sorted(list(df['Sales Rep'].dropna().unique()))
    selected_sales_rep = st.selectbox("Sales Rep", sales_reps, label_visibility="collapsed")

with nav_col5:
    if 'Date' in df.columns:
        date_source = pd.to_datetime(df['Date'].dropna(), errors='coerce').dt.normalize()
        valid_dates = sorted(date_source.dropna().dt.date.unique())

        if valid_dates:
            today = datetime.date.today()
            min_d = min(valid_dates)
            max_d = max(valid_dates)
            default_date = today if min_d <= today <= max_d else max_d

            selected_range = st.date_input(
                "Date Range",
                value=(default_date, default_date),
                min_value=min_d,
                max_value=max_d,
                format="MM-DD-YYYY",
                label_visibility="collapsed"
            )
            
            if isinstance(selected_range, tuple) and len(selected_range) == 2:
                start_date, end_date = selected_range
                selected_date_range = "Range selected"
            elif isinstance(selected_range, tuple) and len(selected_range) == 1:
                start_date = selected_range[0]
                end_date = selected_range[0]
                selected_date_range = "Range selected"
            else:
                start_date, end_date = default_date, default_date
                selected_date_range = "Range selected"
        else:
            selected_date_range = "Date Ranges"
            start_date, end_date = None, None
    else:
        selected_date_range = "Date Ranges"
        start_date, end_date = None, None

with nav_col6:
    if 'Case Category' in df.columns:
        case_categories = ["Cases / Activities"] + sorted(list(df['Case Category'].dropna().astype(str).unique()))
        selected_case_category = st.selectbox("Case Category", case_categories, label_visibility="collapsed")
    else:
        selected_case_category = "Cases / Activities"

# Apply global filter logic
filtered_df = df.copy()
if selected_carrier != "All Carriers":
    filtered_df = filtered_df[filtered_df['Carrier'] == selected_carrier]
if selected_store != "All Stores":
    filtered_df = filtered_df[filtered_df['Store Name'] == selected_store]
if selected_invoice != "All Invoices":
    filtered_df = filtered_df[filtered_df['Invoice'] == selected_invoice]
if selected_sales_rep != "All Sales Reps":
    filtered_df = filtered_df[filtered_df['Sales Rep'] == selected_sales_rep]

if 'Date' in df.columns and selected_date_range == "Range selected" and start_date and end_date:
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= start_date) & 
        (filtered_df['Date'].dt.date <= end_date)
    ]

if 'Case Category' in df.columns and selected_case_category != "Cases / Activities":
    filtered_df = filtered_df[filtered_df['Case Category'].astype(str).str.strip() == selected_case_category]

st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# PAGE 1: QA DASHBOARD 
# ==========================================
if page == "📊 QA Dashboard":
    st.markdown("<div class='main-title'>QA ANALYSIS REPORT</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>A premium glassmorphic interface tracking daily transactions, discrepancies, and audit notes.</div>", unsafe_allow_html=True)

    # KPI Calculations
    total_invoice = filtered_df['Invoice Amount'].sum()
    total_collected = filtered_df['Amount Collected'].sum()
    total_diff = filtered_df['Difference'].sum()
    total_store = filtered_df['Store Name'].nunique()
    total_employee = filtered_df['Sales Rep'].nunique()

    customer_status = filtered_df['Customer Yes/No'].astype(str).str.strip().str.lower()
    buying_customers = filtered_df[customer_status == 'yes']['Invoice'].nunique()
    non_buying_customers = filtered_df[customer_status == 'no']['Invoice'].nunique()
    total_customers = buying_customers + non_buying_customers

    # 6-Column KPI Grid
    col2, col1, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-label">Total Invoiced</div>
                    <div class="metric-value accent-collected" style="text-align: center;">${total_invoice:,.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card_Customer" style="justify-content: flex-start; padding: 16px 22px;">
                <div>
                    <div class="metric-label" style="margin-bottom: 4px;">Total Customers</div>
                    <div class="metric-value" style="text-align: center; font-size: 26px;">{total_customers:,}</div>
                </div>
                <div style="margin-top: auto;">
                    <hr class="card-divider" style="margin: 8px 0 6px 0;">
                    <div class="sub-grid">
                        <div style="text-align: center; flex: 1;">
                            <div class="sub-label">Buying</div>
                            <div class="sub-val-green">{buying_customers:,}</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="sub-label">Non-Buying</div>
                            <div class="sub-val-red">{non_buying_customers:,}</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-label">Amount Collected</div>
                    <div class="metric-value accent-Invoice" style="text-align: center;">${total_collected:,.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        diff_color = "accent-alert" if total_diff < 0 else "accent-collected"
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-label">Total Discrepancies</div>
                    <div class="metric-value {diff_color}" style="text-align: center;">${total_diff:,.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-label">Total Stores</div>
                    <div class="metric-value accent-warn" style="text-align: center;">{total_store}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-label">Total Employees</div>
                    <div class="metric-value" style="text-align: center; color: #a5b4fc; text-shadow: 0 0 10px rgba(165,180,252,0.3);">{total_employee}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Detailed Transaction Report
    st.markdown("<h3 style='text-align: center;'>📄 DETAILED TRANSACTION REPORT</h3>", unsafe_allow_html=True)

    display_df = filtered_df.copy()
    if not display_df.empty:
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d %H:%M')

    ledger_columns = [
        'Date', 'Carrier', 'Store Name', 'Sales Rep', 'Invoice',
        'Product Desc', 'Invoice Amount', 'Amount Collected', 'Difference',
        'Payment Method', 'Case Category', 'Customer Yes/No', 'General Notes', 'Video Link'
    ]
    display_df = display_df[[c for c in ledger_columns if c in display_df.columns]].copy()
    if 'General Notes' in display_df.columns: display_df['General Notes'] = display_df['General Notes'].fillna('')
    if 'Video Link' in display_df.columns: display_df['Video Link'] = display_df['Video Link'].fillna('')

    def highlight_rows(row):
        has_notes = str(row.get('General Notes', '')).strip() != ''
        has_footage = str(row.get('Video Link', '')).strip() != ''
        if has_notes or has_footage:
            return ['background-color: rgba(239, 68, 68, 0.15)' for _ in row.index]
        return ['' for _ in row.index]

    st.dataframe(
        display_df.style.apply(highlight_rows, axis=1),
        column_config={
            "Invoice Amount": st.column_config.NumberColumn("Invoiced", format="$%.2f"),
            "Amount Collected": st.column_config.NumberColumn("Collected", format="$%.2f"),
            "Difference": st.column_config.NumberColumn("Diff", format="$%.2f"),
            "Customer Yes/No": st.column_config.TextColumn("Customer?"),
            "Video Link": st.column_config.LinkColumn("🎬 CCTV Footage"),
        },
        use_container_width=True,
        hide_index=True
    )

    # Charts Rendering Layout
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if 'Case Category' in filtered_df.columns and not filtered_df.empty:
            case_category_counts = filtered_df['Case Category'].fillna('Uncategorized').astype(str).value_counts().reset_index()
            case_category_counts.columns = ['Case Category', 'Count']

            st.markdown("<div class='chart-card'><div class='chart-title'>📊 Case Activity (Fraud/Theft)</div></div>", unsafe_allow_html=True)
            fig = px.pie(case_category_counts, values='Count', names='Case Category')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0.23)', margin=dict(l=10, r=10, t=10, b=10), showlegend=True, font=dict(color='#ffffff'))
            fig.update_traces(textfont=dict(color='#ffffff'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No Case Category data available.")

    with chart_col2:
        if 'Customer Yes/No' in filtered_df.columns and not filtered_df.empty:
            customer_status = filtered_df['Customer Yes/No'].astype(str).str.strip().str.lower()
            buying_count = int((customer_status == 'yes').sum())
            non_buying_count = int((customer_status == 'no').sum())
            total_customers = buying_count + non_buying_count

            customer_counts = pd.DataFrame({
                'Customer': ['Total Customers', 'Buying', 'Non-Buying'],
                'Count': [total_customers, buying_count, non_buying_count]
            })

            st.markdown("<div class='chart-card'><div class='chart-title'>👥 Customer Status (Buying vs. Non-Buying)</div></div>", unsafe_allow_html=True)
            customer_fig = px.bar(customer_counts, x='Customer', y='Count', color='Customer', text='Count')
            customer_fig.update_traces(textposition='outside', textfont=dict(color='#ffffff'), marker_cornerradius=15)
            customer_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0.23)', margin=dict(l=10, r=10, t=10, b=10), showlegend=False, font=dict(color='#ffffff'))
            st.plotly_chart(customer_fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No customer status data available.")

    # Audit Inspector Canvas
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>🔍 Quick Audit Notes Inspector</h3>", unsafe_allow_html=True)
    if 'General Notes' in filtered_df.columns:
        flagged_notes = filtered_df[filtered_df['General Notes'].notna() & (filtered_df['General Notes'] != "")]
        if not flagged_notes.empty:
            for _, row in flagged_notes.iterrows():
                invoice_num = escape(str(row['Invoice']))
                sales_rep = escape(str(row['Sales Rep']))
                note_text = escape(str(row['General Notes']))
                st.markdown(f"<div class='audit-note-card'><strong>Invoice #{invoice_num} ({sales_rep}):</strong> {note_text}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='audit-note-card' style='text-align: center; color: #166534;'>No critical general notes found for this view!</div>", unsafe_allow_html=True)


# ==========================================
# PAGE 2: INVESTIGATED REPORT
# ==========================================
elif page == "🔍 Investigated Report":

    st.markdown("""
    <style>
    .main-title{
        font-size:48px;
        font-weight:800;
        color:white;
        margin-bottom:10px;
    }

    .subtitle{
        color:#cbd5e1;
        font-size:16px;
        margin-bottom:30px;
    }

    div.stDownloadButton > button {
        background: linear-gradient(135deg, #00084c99, #1f7cd5) !important;
        color:#ffffff !important;
        border:1px solid #ffffff !important;
        border-radius:8px !important;
        font-weight:600 !important;
        width:100% !important;
        min-height:45px !important;
        font-size:14px !important;
        padding:8px 14px !important;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1f7cd5, #00084c99) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>INVESTIGATED AUDIT REPORT</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Targeted ledger tracking security logs, operational variations, and linked CCTV footage assets.</div>", unsafe_allow_html=True)

    investigated_df = filtered_df.copy()

    if not investigated_df.empty:

        investigated_df["Formatted Date"] = investigated_df["Date"].dt.strftime("%Y-%m-%d %H:%M")

        # ==========================================
        # PREPARE EXPORT DATA FIRST
        # ==========================================
        export_rows = []

        for _, row in investigated_df.iterrows():
            export_rows.append({
                "Invoice": row.get("Invoice", ""),
                "Date": row.get("Formatted Date", ""),
                "Store Name": row.get("Store Name", ""),
                "Employee Name": row.get("Sales Rep", ""),
                "Invoice Amount": row.get("Invoice Amount", 0),
                "Amount Collected": row.get("Amount Collected", 0),
                "Difference": row.get("Difference", 0),
                "General Notes": row.get("General Notes", ""),
                "Video Link": row.get("Video Link", "")
            })

        export_df = pd.DataFrame(export_rows)

        # ==========================================
        # PDF GENERATOR
        # ==========================================
        def generate_pdf(df):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph("Investigated Audit Report", styles["Title"]))
            story.append(Spacer(1, 15))

            for _, r in df.iterrows():
                for col in df.columns:
                    story.append(
                        Paragraph(f"<b>{col}:</b> {r[col]}", styles["Normal"])
                    )
                story.append(Spacer(1, 15))

            doc.build(story)
            buffer.seek(0)
            return buffer

        pdf_file = generate_pdf(export_df)

        # ==========================================
        # EXCEL GENERATOR
        # ==========================================
        excel_buffer = BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            export_df.to_excel(
                writer,
                index=False,
                sheet_name="Investigated Report"
            )

        excel_buffer.seek(0)

        # ==========================================
        # DOWNLOAD BUTTONS (CENTERED - COMPACT)
        # ==========================================
        left_space, center_col, right_space = st.columns([3, 4, 3])

        with center_col:
            btn1, btn2 = st.columns([1, 1], gap="small")

            with btn1:
                st.download_button(
                    "📄 DOWNLOAD PDF",
                    data=pdf_file,
                    file_name="Investigated_Audit_Report.pdf",
                    mime="application/pdf"
                )

            with btn2:
                st.download_button(
                    "📊 DOWNLOAD Excel",
                    data=excel_buffer,
                    file_name="Investigated_Audit_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        # ==========================================
        # REPORT CARDS
        # ==========================================
        for _, row in investigated_df.iterrows():

            inv_no = escape(str(row.get("Invoice", "")))
            date_val = escape(str(row.get("Formatted Date", "")))
            store_val = escape(str(row.get("Store Name", "")))
            emp_name = escape(str(row.get("Sales Rep", "")))

            inv_amount = f"${row.get('Invoice Amount', 0):,.2f}"
            amt_collected = f"${row.get('Amount Collected', 0):,.2f}"
            total_discrepancies = f"${row.get('Difference', 0):,.2f}"

            gen_notes = row.get("General Notes")
            gen_notes = (
                escape(str(gen_notes).strip())
                if gen_notes is not None and str(gen_notes).strip() and str(gen_notes).lower() != "nan"
                else "None"
            )

            cctv_url = row.get("Video Link")

            if cctv_url and str(cctv_url).strip().lower() != "nan":
                cctv_html = f"""
                <a href="{cctv_url}" target="_blank"
                style="color:#2563eb;text-decoration:underline;font-weight:600;">
                    View Footage Asset
                </a>
                """
            else:
                cctv_html = "None"

            dynamic_height = max(480, 350 + (len(gen_notes) // 50 * 35))

            card_html = f"""
            <style>
            body {{
                margin:0;
                padding:10px;
                font-family:Arial,sans-serif;
                background:transparent;
                overflow-x:hidden;
            }}

            .template-report-container {{
                width:calc(100% - 20px);
                background:#ffffff;
                color:#000000;
                border:4px solid rgba(164,137,137,0.51);
                border-radius:12px;
                padding:25px;
                margin:10px auto;
                box-sizing:border-box;
                box-shadow:0 4px 15px rgba(0,0,0,0.15);
            }}

            .report-header {{
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:20px;
                padding-bottom:15px;
                border-bottom:1px solid #e2e8f0;
            }}

            .report-title {{
                font-size:22px;
                font-weight:700;
                color:#0f172a;
            }}

            .report-id {{
                background:#eff6ff;
                padding:8px 14px;
                border-radius:8px;
                font-weight:600;
                color:#2563eb;
            }}

            .report-grid {{
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
                gap:15px;
            }}

            .report-item {{
                background:#f8fafc;
                padding:14px;
                border-radius:8px;
            }}

            .report-item label,
            .report-notes label,
            .report-footer label {{
                display:block;
                font-size:14px;
                font-weight:600;
                margin-bottom:6px;
                color:#64748b;
                text-transform:uppercase;
            }}

            .report-item span,
            .report-notes p {{
                font-size:15px;
                color:#0f172a;
                word-break:break-word;
                line-height:1.6;
            }}

            .report-notes {{
                margin-top:18px;
                background:#f8fafc;
                padding:14px;
                border-radius:8px;
            }}

            .report-footer {{
                margin-top:14px;
                padding-top:14px;
                border-top:1px solid #e2e8f0;
            }}
            </style>

            <div class="template-report-container">
                <div class="report-header">
                    <div class="report-title">Audit Investigation Report</div>
                    <div class="report-id">{inv_no}</div>
                </div>

                <div class="report-grid">
                    <div class="report-item"><label>Date</label><span>{date_val}</span></div>
                    <div class="report-item"><label>Store</label><span>{store_val}</span></div>
                    <div class="report-item"><label>Employee Name</label><span>{emp_name}</span></div>
                    <div class="report-item"><label>Invoice Amount</label><span>{inv_amount}</span></div>
                    <div class="report-item"><label>Collected Amount</label><span>{amt_collected}</span></div>
                    <div class="report-item"><label>Total Discrepancies</label><span>{total_discrepancies}</span></div>
                </div>

                <div class="report-notes">
                    <label>General Notes</label>
                    <p>{gen_notes}</p>
                </div>

                <div class="report-footer">
                    <label>Camera Footage</label>
                    {cctv_html}
                </div>
            </div>
            """

            components.html(card_html, height=dynamic_height + 40, scrolling=False)

        # Summary
        investigated_diff = investigated_df["Difference"].sum()

        st.markdown(f"""
        <div style="
            background:#1e293b;
            padding:20px;
            border-radius:12px;
            margin-top:20px;
            color:white;
        ">
            <h4>Scope Log Summary</h4>
            <p>Flagged Cases: {(investigated_df['Difference'] != 0).sum()}</p>
            <p>Net Segment Impact: ${investigated_diff:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("No data entries match the selected filters.")