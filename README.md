# ModelHub - Machine Learning API

ModelHub est une API REST complète pour la gestion, l'entraînement et le déploiement de modèles de machine learning et deep learning.

## Fonctionnalités Principales

- **Gestion des Modèles**
  - CRUD complet pour les modèles ML et DL
  - Sauvegarde et versioning des modèles
  - Comparaison de modèles

- **Entraînement**
  - Entraînement de modèles ML (Scikit-learn)
  - Entraînement de modèles DL (PyTorch)
  - Entraînement de séries temporelles (ARIMA, SARIMA, Prophet, LSTM)

- **Prédictions**
  - API de prédiction en temps réel
  - Batch predictions
  - Évaluation des performances

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/your-username/modelhub.git
cd modelhub
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Initialiser la base de données :
```bash
python init_db.py
```

5. Lancer l'API :
```bash
python run.py
```

## Utilisation de l'API

L'API sera accessible aux adresses suivantes :
- **API Root** : http://localhost:8000
- **Documentation interactive** : http://localhost:8000/docs
- **Documentation alternative** : http://localhost:8000/redoc

### Endpoints Principaux

#### Modèles
- `GET /api/v1/models` - Lister tous les modèles
- `POST /api/v1/models` - Créer un nouveau modèle
- `GET /api/v1/models/{id}` - Récupérer un modèle
- `PUT /api/v1/models/{id}` - Mettre à jour un modèle
- `DELETE /api/v1/models/{id}` - Supprimer un modèle
- `POST /api/v1/models/{id}/train` - Entraîner un modèle
- `POST /api/v1/models/{id}/predict` - Faire des prédictions

#### Séries Temporelles
- `POST /api/v1/time-series/upload` - Uploader des données
- `POST /api/v1/time-series/train` - Entraîner un modèle de séries temporelles
- `GET /api/v1/time-series/models` - Lister les modèles de séries temporelles

## Technologies Utilisées

- **Backend** : FastAPI
- **Base de données** : SQLAlchemy + SQLite/PostgreSQL
- **ML/DL** : Scikit-learn, PyTorch, TensorFlow
- **Séries temporelles** : Statsmodels, Prophet
- **Tests** : Pytest

## Structure du Projet

```
modelhub/
├── app/
│   ├── api/
│   │   └── endpoints/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── requirements.txt
└── run.py
```

## Tests

```bash
# Exécuter tous les tests
pytest

# Exécuter les tests avec couverture
pytest --cov=app
```

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
