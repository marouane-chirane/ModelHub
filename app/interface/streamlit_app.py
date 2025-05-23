import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from typing import Dict, Any
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="ModelHub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre et description
st.title("🤖 ModelHub")
st.markdown("""
    Plateforme de Machine Learning et Deep Learning pour gérer, entraîner et déployer vos modèles.
""")

# Configuration de l'API
API_URL = "http://localhost:8000/api/v1"

# Fonction pour appeler l'API
def call_api(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    url = f"{API_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API: {str(e)}")
        return None

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisir une section",
    ["Tableau de bord", "Gestion des modèles", "Entraînement", "Prédictions"]
)

# Tableau de bord
if page == "Tableau de bord":
    st.header("📊 Tableau de bord")
    
    # Statistiques générales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Modèles disponibles", "0")
    with col2:
        st.metric("Modèles entraînés", "0")
    with col3:
        st.metric("Prédictions effectuées", "0")
    
    # Graphique des performances
    st.subheader("Performances des modèles")
    # TODO: Ajouter un graphique des performances

# Gestion des modèles
elif page == "Gestion des modèles":
    st.header("📁 Gestion des modèles")
    
    # Onglets pour différentes actions
    tab1, tab2, tab3 = st.tabs(["Liste des modèles", "Créer un modèle", "Supprimer un modèle"])
    
    with tab1:
        st.subheader("Liste des modèles")
        models = call_api("models")
        if models:
            df = pd.DataFrame(models)
            st.dataframe(df)
    
    with tab2:
        st.subheader("Créer un nouveau modèle")
        with st.form("create_model_form"):
            name = st.text_input("Nom du modèle")
            model_type = st.selectbox("Type de modèle", ["Classification", "Régression", "Clustering"])
            framework = st.selectbox("Framework", ["sklearn", "pytorch"])
            description = st.text_area("Description")
            hyperparameters = st.text_area("Hyperparamètres (JSON)", "{}")
            
            submitted = st.form_submit_button("Créer")
            if submitted:
                try:
                    hyperparams = json.loads(hyperparameters)
                    data = {
                        "name": name,
                        "type": model_type,
                        "framework": framework,
                        "description": description,
                        "hyperparameters": hyperparams
                    }
                    response = call_api("models", "POST", data)
                    if response:
                        st.success("Modèle créé avec succès!")
                except json.JSONDecodeError:
                    st.error("Format JSON invalide pour les hyperparamètres")
    
    with tab3:
        st.subheader("Supprimer un modèle")
        if models:
            model_to_delete = st.selectbox(
                "Sélectionner un modèle à supprimer",
                options=[m["name"] for m in models],
                format_func=lambda x: f"{x} (ID: {next(m['id'] for m in models if m['name'] == x)})"
            )
            if st.button("Supprimer"):
                model_id = next(m["id"] for m in models if m["name"] == model_to_delete)
                response = call_api(f"models/{model_id}", "DELETE")
                if response:
                    st.success("Modèle supprimé avec succès!")

# Entraînement
elif page == "Entraînement":
    st.header("🎯 Entraînement")
    
    # Sélection du modèle
    models = call_api("models")
    if models:
        model_to_train = st.selectbox(
            "Sélectionner un modèle à entraîner",
            options=[m["name"] for m in models],
            format_func=lambda x: f"{x} (ID: {next(m['id'] for m in models if m['name'] == x)})"
        )
        
        # Upload des données
        uploaded_file = st.file_uploader("Charger les données d'entraînement", type=["csv", "json"])
        
        if uploaded_file and st.button("Démarrer l'entraînement"):
            model_id = next(m["id"] for m in models if m["name"] == model_to_train)
            # TODO: Implémenter l'envoi des données et l'entraînement
            st.info("L'entraînement est en cours...")
            
            # Simulation de l'entraînement
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                st.empty()
            
            st.success("Entraînement terminé!")

# Prédictions
elif page == "Prédictions":
    st.header("🔮 Prédictions")
    
    # Sélection du modèle
    models = call_api("models")
    if models:
        model_to_use = st.selectbox(
            "Sélectionner un modèle pour les prédictions",
            options=[m["name"] for m in models],
            format_func=lambda x: f"{x} (ID: {next(m['id'] for m in models if m['name'] == x)})"
        )
        
        # Upload des données
        uploaded_file = st.file_uploader("Charger les données pour la prédiction", type=["csv", "json"])
        
        if uploaded_file and st.button("Faire des prédictions"):
            model_id = next(m["id"] for m in models if m["name"] == model_to_use)
            # TODO: Implémenter l'envoi des données et les prédictions
            st.info("Calcul des prédictions en cours...")
            
            # Simulation des prédictions
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                st.empty()
            
            st.success("Prédictions terminées!")
            
            # Affichage des résultats
            st.subheader("Résultats")
            # TODO: Afficher les résultats des prédictions 