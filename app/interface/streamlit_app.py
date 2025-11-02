import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from typing import Dict, Any
import os
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

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
    ["Tableau de bord", "Gestion des modèles", "Entraînement", "Prédictions", "Pipelines", "Datasets", "Annotation", "Export"]
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

elif page == "Pipelines":
    st.header("🧱 Pipelines")
    st.markdown("Exécuter un pipeline et visualiser les étapes.")

    with st.form("run_pipeline_form"):
        kind = st.selectbox("Type de pipeline", [
            "cv_classification",
            "cv_detection",
            "cv_segmentation",
        ])
        dataset_path = st.text_input("Chemin du dataset (dossier)")
        col1, col2, col3 = st.columns(3)
        with col1:
            epochs = st.number_input("Epochs", min_value=1, max_value=100, value=1)
        with col2:
            train_ratio = st.slider("Train ratio", 0.5, 0.95, 0.8)
        with col3:
            lr = st.number_input("Learning rate", min_value=1e-5, max_value=1e-1, value=1e-3, format="%f")

        submitted = st.form_submit_button("Lancer")

    if submitted:
        payload = {
            "kind": kind,
            "config": {
                "dataset_path": dataset_path,
                "epochs": int(epochs),
                "train_ratio": float(train_ratio),
                "lr": float(lr),
            },
        }
        result = call_api("pipelines/run", method="POST", data=payload)
        if result:
            st.success(f"Pipeline: {result.get('name')} - Statut: {result.get('status')}")
            steps = result.get("steps", [])
            for step in steps:
                col1, col2, col3, col4 = st.columns([3, 2, 3, 4])
                col1.write(f"Étape: {step.get('name')}")
                col2.write(f"Statut: {step.get('status')}")
                col3.write(f"Début: {step.get('started_at')}")
                col4.write(f"Fin: {step.get('finished_at')}")
            if result.get("metrics"):
                st.subheader("Métriques")
                st.json(result.get("metrics")) 

elif page == "Datasets":
    st.header("📂 Datasets")
    name = st.text_input("Nom du dataset")
    desc = st.text_input("Description")
    if st.button("Créer") and name:
        resp = call_api("datasets", method="POST", data={"name": name, "description": desc})
        if resp:
            st.success(f"Dataset créé: {resp.get('name')}")
    st.subheader("Liste des datasets")
    ds = call_api("datasets")
    if ds:
        st.dataframe(pd.DataFrame(ds))

elif page == "Annotation":
    st.header("🖊️ Annotation")
    ds = call_api("datasets") or []
    if ds:
        ds_map = {d["name"]: d["id"] for d in ds}
        ds_name = st.selectbox("Dataset", list(ds_map.keys()))
        dataset_id = ds_map[ds_name]
        images = call_api(f"datasets/{dataset_id}/images") or []
        col_up, col_path = st.columns([1, 1])
        with col_up:
            uploaded = st.file_uploader("Ajouter une image (chemin local pour démo)")
        with col_path:
            img_path = st.text_input("Chemin absolu de l'image")
        if (uploaded or img_path) and st.button("Ajouter l'image"):
            path = img_path
            if path:
                resp = call_api("images", method="POST", data={"dataset_id": dataset_id, "path": path})
                if resp:
                    st.success("Image ajoutée")
                    images = call_api(f"datasets/{dataset_id}/images") or []
        if images:
            img_map = {i["path"]: i["id"] for i in images}
            img_sel = st.selectbox("Image", list(img_map.keys()))
            image_id = img_map[img_sel]
            st.write("Dessiner des bounding boxes (rectangles).")
            canvas_result = st_canvas(
                fill_color="rgba(255, 0, 0, 0.2)",
                stroke_width=2,
                stroke_color="#ff0000",
                background_image=None,
                background_color="#eee",
                height=480,
                width=640,
                drawing_mode="rect",
                key="canvas",
            )
            label = st.text_input("Label")
            if st.button("Enregistrer annotations") and canvas_result and canvas_result.json_data:
                for obj in canvas_result.json_data.get("objects", []):
                    if obj.get("type") == "rect" and label:
                        left = float(obj.get("left", 0.0)) / 640.0
                        top = float(obj.get("top", 0.0)) / 480.0
                        width = float(obj.get("width", 0.0)) / 640.0
                        height = float(obj.get("height", 0.0)) / 480.0
                        call_api("annotations", method="POST", data={
                            "image_id": image_id,
                            "label": label,
                            "x": left,
                            "y": top,
                            "w": width,
                            "h": height,
                        })
                st.success("Annotations enregistrées")

elif page == "Export":
    st.header("📦 Export")
    ds = call_api("datasets") or []
    if ds:
        ds_map = {d["name"]: d["id"] for d in ds}
        ds_name = st.selectbox("Dataset", list(ds_map.keys()))
        dataset_id = ds_map[ds_name]
        fmt = st.selectbox("Format", ["COCO", "YOLO"])
        if st.button("Exporter"):
            if fmt == "COCO":
                data = call_api(f"datasets/{dataset_id}/export/coco")
                st.json(data)
            else:
                data = call_api(f"datasets/{dataset_id}/export/yolo")
                st.json(data) 