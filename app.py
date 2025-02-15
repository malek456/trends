import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 📌 Configuration de la page Streamlit
st.set_page_config(page_title="Twitter Trends Dashboard", layout='wide')
FASTAPI_URL = "http://127.0.0.1:8000"

# 🔹 Fonction pour récupérer les données via l'API
@st.cache_data  # Utilisation de @st.cache_data au lieu de @st.cache_resource pour Streamlit v1.22+
def get_data():
    try:
        response = requests.get(f"{FASTAPI_URL}/api/trends")
        response.raise_for_status()
        data = response.json()["trends"]
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return pd.DataFrame()

# Charger les données
data = get_data()

# 🔹 Affichage du titre et de la description du dashboard
st.title("📊 Twitter Trends Dashboard")
st.markdown("Ce dashboard analyse les tendances Twitter stockées dans MongoDB.")

# Vérifier si des données sont disponibles
if data.empty:
    st.warning("⚠️ Aucune donnée trouvée dans la base de données.")
else:
    # 🔹 Trier les tendances par `post_count`
    top_trends = data.sort_values(by="post_count", ascending=False).head(10)

    # 🔹 Graphique des tendances
    st.subheader("📈 Top 10 des tendances Twitter")
    fig = px.bar(top_trends, x="name", y="post_count", text_auto=True, color="post_count", title="Tendances Twitter")
    st.plotly_chart(fig, use_container_width=True)

    # 🔹 Génération d'un nuage de mots
    st.subheader("☁️ Nuage de mots des tendances")
    text = " ".join(data["name"].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # 🔹 Affichage des données sous forme de tableau interactif
    st.subheader("📋 Données des tendances")
    st.dataframe(data)

# 🔹 Footer
st.markdown("**📌 Twitter Trends Dashboard - Powered by MongoDB & Streamlit 🚀**")

# 🔹 Second API Call for Top Keywords by Shares
response = requests.get(f"{FASTAPI_URL}/api/top_keywords")
data = response.json()

# Extract the keywords and shares from the response
keywords = [item['keyword'] for item in data['top_keywords']]
shares = [item['share'] for item in data['top_keywords']]

# 🔹 Create the Plotly bar chart
#fig = go.Figure(data=[go.Bar(x=keywords, y=shares, marker_color='skyblue')])

fig = px.bar(top_trends, x=keywords, y=shares, text_auto=True, color="post_count", title="Tendances Twitter")


# Set the title and labels
fig.update_layout(
    title='Top 10 Keywords by Shares',
    xaxis_title='Keywords',
    yaxis_title='Shares',
    xaxis_tickangle=45
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

########################hedha mazel ma5dmchhhh

def get_top_keywords():
    response = requests.get(f"{FASTAPI_URL}/api/top_keywords/score")
    if response.status_code == 200:
        return response.json().get("top_keywords", [])
    else:
        st.error(f"Failed to fetch data. Status Code: {response.status_code}")
        return []
    
    
st.write("Showing the top 10 trending keywords based on engagement metrics.")

# Fetch top keywords
top_keywords = get_top_keywords()

# Display data in a table and plot
if top_keywords:
    df = pd.DataFrame(top_keywords)

    # Display Table
    st.subheader("📌 Top Trending Keywords")
    st.dataframe(df, width=700)

    # Sort by trending score
    df = df.sort_values(by="trending_score", ascending=False)

    # Create a bar chart using Plotly
    st.subheader("📊 Trending Keywords by Score")
    fig = px.bar(
        df,
        x="trending_score",
        y="keyword",
        orientation="h",
        text="trending_score",
        color="trending_score",
        color_continuous_scale="viridis"
    )
    fig.update_layout(xaxis_title="Trending Score", yaxis_title="Keyword", height=500)
    
    # Show Plot
    st.plotly_chart(fig)
    
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    st.write(df.columns)

        # Axe principal pour les impressions
    ax1.set_xlabel("Keyword")
    ax1.set_ylabel("Impressions", color="tab:blue")
    ax1.plot(df["keyword"], df["impression"], marker='o', linestyle='-', color="tab:blue", label="Impressions")
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    plt.xticks(rotation=45)

        # Axe secondaire pour les likes
    ax2 = ax1.twinx()
    ax2.set_ylabel("Likes", color="tab:orange")
    ax2.plot(df["keyword"], df["like"], marker='s', linestyle='--', color="tab:orange", label="Likes")
    ax2.tick_params(axis='y', labelcolor="tab:orange")

    plt.title("Comparaison des Impressions et Likes par Keyword")
    fig.tight_layout()
    st.pyplot(fig)

else:
    st.warning("No trending keywords available.")






















