from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import pandas as pd
from transformers import pipeline

# Charger les variables d'environnement
load_dotenv()

# Création de l'application FastAPI
app = FastAPI()

# Autoriser les requêtes CORS (évite les erreurs de politique de sécurité)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connexion à MongoDB avec URI sécurisé
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["trends_db"]
collection = db["tweeter_trends"]

@app.get("/api/trends")
def get_trends():
    """
    Récupère les tendances Twitter depuis MongoDB et les retourne sous forme JSON.
    """
    data = list(collection.find({}, {"_id": 0}))  # Exclure _id
    return {"trends": data}

# Section de l'API pour les mots-clés tendances
collection_keyword = db["trending_keywords_trends"]
@app.get("/api/top_keywords")
def get_top_keywords():
    """
    Récupère les top 10 mots-clés par partage depuis MongoDB.
    """
    pipeline = [
        {"$sort": {"share": -1}},  # Sort by share in descending order
        {"$limit": 10},  # Limit to top 10
        {"$project": {"_id": 0, "keyword": 1, "share": 1}}  # Include only keyword and share fields
    ]
    
    top_keywords = list(collection_keyword.aggregate(pipeline))

    return {"top_keywords": top_keywords}
####################

data_keywords = pd.DataFrame(list(collection_keyword.find()))
data_keywords.drop(columns=["_id"], inplace=True)

    # Convertir les colonnes pertinentes en numérique
cols_to_convert = ["like", "impression", "share"]
data_keywords[cols_to_convert] = data_keywords[cols_to_convert].astype(float)

    # Calcul du score de tendance
data_keywords["trending_score"] = (data_keywords["like"] * 0.5) + (data_keywords["share"] * 0.3) + (data_keywords["impression"] * 0.2)

    # Sélectionner les 10 mots-clés les plus tendance
top_trending = data_keywords.sort_values(by="trending_score", ascending=False).head(10)

collection_keyword = db["trending_keywords_trends"]
@app.get("/api/top_keywords/score")
def get_top_keywords():
    """
    Fetches the top 10 trending keywords based on trending score.
    """
    # Retrieve data from MongoDB
    data = list(collection_keyword.find({}, {"_id": 0, "keyword": 1, "like": 1, "impression": 1, "share": 1}))

    # Convert to DataFrame
    df = pd.DataFrame(data)

    if df.empty:
        return {"message": "No data available"}

    # Convert columns to numeric
    cols_to_convert = ["like", "impression", "share"]
    df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Calculate trending score dynamically
    df["trending_score"] = (df["like"] * 0.5) + (df["share"] * 0.3) + (df["impression"] * 0.2)

    # Select the top 10 keywords based on trending score
    top_trending = df.sort_values(by="trending_score", ascending=False).head(10)

    return {"top_keywords": top_trending.to_dict(orient="records")}


# Lancer l'application via uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
