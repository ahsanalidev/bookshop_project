import os
import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title='Book Sales Dashboard', page_icon='📚', layout='wide'
)

# Initialize session state for refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'auto_refresh_delay' not in st.session_state:
    st.session_state.auto_refresh_delay = 300  # 5 minutes by default

# Snowflake connection
@st.cache_resource(ttl=st.session_state.auto_refresh_delay)
def get_snowflake_connection():
    try:
        return snowflake.connector.connect(
            user=os.environ.get('SNOWFLAKE_USER'),
            password=os.environ.get('SNOWFLAKE_PASSWORD'),
            account=os.environ.get('SNOWFLAKE_ACCOUNT'),
            warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
            database=os.environ.get('SNOWFLAKE_DATABASE'),
            schema='MARTS',
        )
    except Exception as e:
        st.error(f'Connection error to Snowflake: {e}')
        return None


# Functions to load data
@st.cache_data(ttl=st.session_state.auto_refresh_delay)
def load_sales_data():
    try:
        conn = get_snowflake_connection()
        if conn is None:
            return pd.DataFrame()
        
        query = 'SELECT * FROM MARTS."obt_sales"'
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f'Error retrieving data: {e}')
        return pd.DataFrame()


# Function to create an empty chart
def create_empty_chart(title, chart_type='bar'):
    if chart_type == 'bar':
        fig = px.bar(title=title)
    elif chart_type == 'line':
        fig = px.line(title=title)
    elif chart_type == 'pie':
        fig = px.pie(title=title)
    fig.update_layout(
        xaxis={'visible': False},
        yaxis={'visible': False},
        annotations=[{
            'text': 'No data available',
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 16}
        }]
    )
    return fig


# Main title
st.title('📚 Book Sales Dashboard')

# Display time since last refresh
time_since_refresh = time.time() - st.session_state.last_refresh
st.caption(f"Last refresh: {datetime.fromtimestamp(st.session_state.last_refresh).strftime('%H:%M:%S')} ({int(time_since_refresh)} seconds ago)")

# Load data
sales_data = load_sales_data()

# Filters in sidebar
st.sidebar.header('Filters')

# Select year with default values
years = [datetime.now().year]
if not sales_data.empty:
    available_years = sales_data['annees'].unique().tolist()
    years = list(set(years + available_years))
    years.sort()

selected_year = st.sidebar.selectbox('Year', options=years)

# Sidebar parameters
st.sidebar.markdown("---")
st.sidebar.header('Settings')

auto_refresh_delay = st.sidebar.number_input(
    "Refresh delay (seconds)",
    min_value=30,
    max_value=3600,
    value=st.session_state.auto_refresh_delay,
    step=30,
    help="Set the delay between each automatic data refresh"
)

if st.sidebar.button('**Refresh now**', type='tertiary'):
    st.session_state.last_refresh = time.time()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

if auto_refresh_delay != st.session_state.auto_refresh_delay:
    st.session_state.auto_refresh_delay = auto_refresh_delay
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Automatic refresh check
if time_since_refresh >= st.session_state.auto_refresh_delay:
    st.session_state.last_refresh = time.time()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Data filtering
if not sales_data.empty:
    filtered_data = sales_data[sales_data['annees'] == selected_year]
else:
    filtered_data = pd.DataFrame()

# Section 1: Sales Overview
st.markdown("### 📊 Sales Overview")
st.markdown("---")

# First row of charts
col1, col2 = st.columns(2)

with col1:
    st.subheader(f'📊 Sales by Month in {selected_year}')
    if not filtered_data.empty:
        monthly_sales = filtered_data.groupby('mois')['qte'].sum().reset_index()
        month_order = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        # You can translate month names if needed
        monthly_sales['mois'] = pd.Categorical(
            monthly_sales['mois'], categories=month_order, ordered=True
        )
        monthly_sales = monthly_sales.sort_values('mois')

        fig = px.bar(
            monthly_sales,
            x='mois',
            y='qte',
            title=f'Quantity Sold per Month in {selected_year}',
            color='qte',
            labels={'qte': 'Quantity Sold', 'mois': 'Month'},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart(f'Quantity Sold per Month in {selected_year}'))

with col2:
    st.subheader('🥧 Sales by Category')
    if not filtered_data.empty:
        category_sales = (
            filtered_data.groupby('category_intitule')['qte']
            .sum()
            .reset_index()
        )
        fig = px.pie(
            category_sales,
            values='qte',
            names='category_intitule',
            title='Sales Distribution by Category',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Sales Distribution by Category', 'pie'))

# Section 2: Temporal Analysis
st.markdown("### 📅 Temporal Analysis")
st.markdown("---")

# Second row of charts
col3, col4 = st.columns(2)

with col3:
    st.subheader('📈 Sales by Day of the Week')
    if not filtered_data.empty:
        daily_sales = filtered_data.groupby('jour')['qte'].sum().reset_index()
        day_order = [
            'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
        ]
        # You can translate day names if needed
        daily_sales['jour'] = pd.Categorical(
            daily_sales['jour'], categories=day_order, ordered=True
        )
        daily_sales = daily_sales.sort_values('jour')

        fig = px.line(
            daily_sales,
            x='jour',
            y='qte',
            title='Quantity Sold by Day of the Week',
            labels={'qte': 'Quantity Sold', 'jour': 'Day'},
            line_shape='spline',
            markers=True,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Quantity Sold by Day of the Week', 'line'))

with col4:
    st.subheader('💰 Average Transaction Value')
    if not filtered_data.empty:
        avg_transaction = (
            filtered_data.groupby('mois')['total_amount']
            .mean()
            .reset_index()
        )
        month_order = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        avg_transaction['mois'] = pd.Categorical(
            avg_transaction['mois'], categories=month_order, ordered=True
        )
        avg_transaction = avg_transaction.sort_values('mois')

        fig = px.line(
            avg_transaction,
            x='mois',
            y='total_amount',
            title='Average Transaction Value per Month',
            labels={'total_amount': 'Purchase Amount', 'mois': 'Month'},
            line_shape='spline',
            markers=True,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Average Transaction Value per Month', 'line'))

# Section 3: Customer Analysis
st.markdown("### 👥 Customer Analysis")
st.markdown("---")

# Third row of charts
col5, col6 = st.columns(2)

with col5:
    st.subheader('👥 Top 10 Customers')
    if not filtered_data.empty:
        top_customers = (
            filtered_data.groupby('customer_nom')['total_amount']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig = px.bar(
            top_customers,
            x='customer_nom',
            y='total_amount',
            title="Top 10 Customers by Purchase Amount",
            labels={'total_amount': 'Purchase Amount', 'customer_nom': 'Customer'},
            color='total_amount',
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart("Top 10 Customers by Purchase Amount"))

with col6:
    st.subheader('📅 Customer Purchase Frequency')
    if not filtered_data.empty:
        customer_frequency = (
            filtered_data.groupby('customer_nom')['facture_id']
            .nunique()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        
        fig = px.bar(
            customer_frequency,
            x='customer_nom',
            y='facture_id',
            title='Top 10 Customers by Number of Invoices',
            color='facture_id',
            color_continuous_scale=px.colors.sequential.Plasma,
            labels={'facture_id': 'Number of Invoices', 'customer_nom': 'Customer'}
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Top 10 Customers by Number of Invoices'))

# Section 4: Product Analysis
st.markdown("### 📚 Product Analysis")
st.markdown("---")

# Fourth row of charts
col7, col8 = st.columns(2)

with col7:
    st.subheader('📚 Top 10 Best Selling Books')
    if not filtered_data.empty:
        top_books = (
            filtered_data.groupby('book_intitule')['qte']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig = px.bar(
            top_books,
            x='book_intitule',
            y='qte',
            title='Top 10 Best Selling Books',
            color='qte',
            labels={'qte': 'Quantity Sold', 'book_intitule': 'Book'},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Top 10 Best Selling Books'))

with col8:
    st.subheader('📊 Sales by Category per Month')
    if not filtered_data.empty:
        category_monthly = (
            filtered_data.groupby(['mois', 'category_intitule'])['qte']
            .sum()
            .reset_index()
        )
        month_order = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        category_monthly['mois'] = pd.Categorical(
            category_monthly['mois'], categories=month_order, ordered=True
        )
        category_monthly = category_monthly.sort_values('mois')

        fig = px.bar(
            category_monthly,
            x='mois',
            y='qte',
            color='category_intitule',
            barmode='stack',
            labels={'qte': 'Quantity Sold', 'mois': 'Month', 'category_intitule': 'Category'},
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        
        fig.update_layout(
            hovermode='x unified',
            legend=dict(
                title='Categories',
                orientation="h",
                yanchor="bottom",
                y=1.1,
                xanchor="right",
                x=1
            ),
            margin=dict(t=80, b=50, l=50, r=50),  
            height=450,  
            xaxis_title='Month',
            yaxis_title='Quantity Sold'
        )
        
        fig.update_traces(
            hovertemplate='%{y} books sold'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.plotly_chart(create_empty_chart('Sales by Category', 'bar'))

# Section 5: Sales Details
st.markdown("### 📝 Sales Details")
st.markdown("---")

if not filtered_data.empty:
    # display with more user friendly column names
    st.dataframe(
        filtered_data[
            ['id', 'book_intitule', 'customer_nom', 'qte', 'pu', 'total_amount']
        ],
        use_container_width=True,
        column_config={
            'id': 'ID',
            'book_intitule': 'Book',
            'customer_nom': 'Customer',
            'qte': 'Quantity',
            'pu': 'Unit Price',
            'total_amount': 'Total Amount'
        }
    )
else:
    st.info('No data available to display sales details.')