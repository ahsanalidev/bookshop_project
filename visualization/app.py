import os
import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Configuration de la page
st.set_page_config(
    page_title='Dashboard des ventes de livres', page_icon='📚', layout='wide'
)

# Initialisation de la session state pour le refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'auto_refresh_delay' not in st.session_state:
    st.session_state.auto_refresh_delay = 300  # 5 minutes par défaut

# Connexion à Snowflake
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
        st.error(f'Erreur de connexion à Snowflake: {e}')
        return None


# Fonctions pour charger les données
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
        st.error(f'Erreur lors de la récupération des données: {e}')
        return pd.DataFrame()


# Fonction pour créer un graphique vide
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
            'text': 'Aucune donnée disponible',
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 16}
        }]
    )
    return fig


# Titre principal
st.title('📚 Dashboard des ventes de livres')

# Affichage du temps depuis le dernier rafraîchissement
time_since_refresh = time.time() - st.session_state.last_refresh
st.caption(f"Dernier rafraîchissement: {datetime.fromtimestamp(st.session_state.last_refresh).strftime('%H:%M:%S')} (il y a {int(time_since_refresh)} secondes)")

# Chargement des données
sales_data = load_sales_data()

# Filtres dans la sidebar
st.sidebar.header('Filtres')

# Sélection de l'année avec valeurs par défaut
years = [datetime.now().year]
if not sales_data.empty:
    available_years = sales_data['annees'].unique().tolist()
    years = list(set(years + available_years))
    years.sort()

selected_year = st.sidebar.selectbox('Année', options=years)

# Paramètres dans la sidebar
st.sidebar.markdown("---")
st.sidebar.header('Paramètres')

auto_refresh_delay = st.sidebar.number_input(
    "Délai de rafraîchissement (secondes)",
    min_value=30,
    max_value=3600,
    value=st.session_state.auto_refresh_delay,
    step=30,
    help="Définissez le délai entre chaque rafraîchissement automatique des données"
)

if st.sidebar.button('**Rafraîchir maintenant**', type='tertiary'):
    st.session_state.last_refresh = time.time()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

if auto_refresh_delay != st.session_state.auto_refresh_delay:
    st.session_state.auto_refresh_delay = auto_refresh_delay
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Vérification du rafraîchissement automatique
if time_since_refresh >= st.session_state.auto_refresh_delay:
    st.session_state.last_refresh = time.time()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Filtrage des données
if not sales_data.empty:
    filtered_data = sales_data[sales_data['annees'] == selected_year]
else:
    filtered_data = pd.DataFrame()

# Section 1: Vue d'ensemble des ventes
st.markdown("### 📊 Vue d'ensemble des ventes")
st.markdown("---")

# Première ligne de graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader(f'📊 Ventes par mois en {selected_year}')
    if not filtered_data.empty:
        monthly_sales = filtered_data.groupby('mois')['qte'].sum().reset_index()
        month_order = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        monthly_sales['mois'] = pd.Categorical(
            monthly_sales['mois'], categories=month_order, ordered=True
        )
        monthly_sales = monthly_sales.sort_values('mois')

        fig = px.bar(
            monthly_sales,
            x='mois',
            y='qte',
            title=f'Quantité vendue par mois en {selected_year}',
            color='qte',
            labels={'qte': 'Quantité vendue', 'mois': 'Mois'},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart(f'Quantité vendue par mois en {selected_year}'))

with col2:
    st.subheader('🥧 Ventes par catégorie')
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
            title='Répartition des ventes par catégorie',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Répartition des ventes par catégorie', 'pie'))

# Section 2: Analyse temporelle
st.markdown("### 📅 Analyse temporelle")
st.markdown("---")

# Deuxième ligne de graphiques
col3, col4 = st.columns(2)

with col3:
    st.subheader('📈 Ventes par jour de la semaine')
    if not filtered_data.empty:
        daily_sales = filtered_data.groupby('jour')['qte'].sum().reset_index()
        day_order = [
            'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
        ]
        daily_sales['jour'] = pd.Categorical(
            daily_sales['jour'], categories=day_order, ordered=True
        )
        daily_sales = daily_sales.sort_values('jour')

        fig = px.line(
            daily_sales,
            x='jour',
            y='qte',
            title='Quantité vendue par jour de la semaine',
            labels={'qte': 'Quantité vendue', 'jour': 'Jour'},
            line_shape='spline',
            markers=True,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Quantité vendue par jour de la semaine', 'line'))

with col4:
    st.subheader('💰 Valeur moyenne des transactions')
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
            title='Valeur moyenne des transactions par mois',
            labels={'total_amount': 'Montant d\'achat', 'mois': 'Mois'},
            line_shape='spline',
            markers=True,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Valeur moyenne des transactions par mois', 'line'))

# Section 3: Analyse des clients
st.markdown("### 👥 Analyse des clients")
st.markdown("---")

# Troisième ligne de graphiques
col5, col6 = st.columns(2)

with col5:
    st.subheader('👥 Top 10 clients')
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
            title="Top 10 clients par montant d'achat",
            labels={'total_amount': 'Montant d\'achat', 'customer_nom': 'Client'},
            color='total_amount',
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart("Top 10 clients par montant d'achat"))

with col6:
    st.subheader('📅 Fréquence d\'achat des clients')
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
            title='Top 10 clients par nombre de factures',
            color='facture_id',
            color_continuous_scale=px.colors.sequential.Plasma,
            labels={'facture_id': 'Nombre de factures', 'customer_nom': 'Client'}
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Top 10 clients par nombre de factures'))

# Section 4: Analyse des produits
st.markdown("### 📚 Analyse des produits")
st.markdown("---")

# Quatrième ligne de graphiques
col7, col8 = st.columns(2)

with col7:
    st.subheader('📚 Top 10 livres les plus vendus')
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
            title='Top 10 des livres les plus vendus',
            color='qte',
            labels={'qte': 'Quantité vendue', 'book_intitule': 'Livre'},
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig)
    else:
        st.plotly_chart(create_empty_chart('Top 10 des livres les plus vendus'))

with col8:
    st.subheader('📊 Ventes par catégorie par mois')
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
            labels={'qte': 'Quantité vendue', 'mois': 'Mois', 'category_intitule': 'Catégorie'},
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        
        fig.update_layout(
            hovermode='x unified',
            legend=dict(
                title='Catégories',
                orientation="h",
                yanchor="bottom",
                y=1.1,
                xanchor="right",
                x=1
            ),
            margin=dict(t=80, b=50, l=50, r=50),  
            height=450,  
            xaxis_title='Mois',
            yaxis_title='Quantité vendue'
        )
        
        fig.update_traces(
            hovertemplate='%{y} livres vendus'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.plotly_chart(create_empty_chart('Ventes par catégorie', 'bar'))

# Section 5: Détails des ventes
st.markdown("### 📝 Détails des ventes")
st.markdown("---")

if not filtered_data.empty:
    # disaply with more user friendly columns names
    st.dataframe(
        filtered_data[
            ['id', 'book_intitule', 'customer_nom', 'qte', 'pu', 'total_amount']
        ],
        use_container_width=True,
        column_config={
            'id': 'ID',
            'book_intitule': 'Livre',
            'customer_nom': 'Client',
            'qte': 'Quantité',
            'pu': 'Prix unitaire',
            'total_amount': 'Montant total'
        }
    )
else:
    st.info('Aucune donnée disponible pour l\'affichage des détails des ventes.')
