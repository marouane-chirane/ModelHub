// Configuration de l'API
const API_URL = 'http://localhost:8000/api/v1';

// Gestionnaire d'événements pour le chargement du document
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Chargement initial des données
    loadDashboard();
    loadModels();

    // Gestionnaires d'événements pour les formulaires
    setupFormHandlers();
});

// Fonction pour charger le tableau de bord
async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/models`);
        const models = await response.json();
        
        // Mise à jour des statistiques
        document.getElementById('total-models').textContent = models.length;
        document.getElementById('trained-models').textContent = 
            models.filter(m => m.metrics).length;
        
        // Mise à jour du graphique de performance
        updatePerformanceChart(models);
    } catch (error) {
        showAlert('Erreur lors du chargement du tableau de bord', 'danger');
    }
}

// Fonction pour charger la liste des modèles
async function loadModels() {
    try {
        const response = await fetch(`${API_URL}/models`);
        const models = await response.json();
        
        const modelsContainer = document.getElementById('models-container');
        modelsContainer.innerHTML = '';
        
        models.forEach(model => {
            const modelCard = createModelCard(model);
            modelsContainer.appendChild(modelCard);
        });
    } catch (error) {
        showAlert('Erreur lors du chargement des modèles', 'danger');
    }
}

// Fonction pour créer une carte de modèle
function createModelCard(model) {
    const card = document.createElement('div');
    card.className = 'col-md-4 mb-4';
    card.innerHTML = `
        <div class="card model-card">
            <div class="card-body">
                <h5 class="card-title">${model.name}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${model.framework}</h6>
                <p class="card-text">${model.description || 'Aucune description'}</p>
                <div class="d-flex justify-content-between">
                    <button class="btn btn-primary btn-sm" onclick="trainModel(${model.id})">
                        Entraîner
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteModel(${model.id})">
                        Supprimer
                    </button>
                </div>
            </div>
        </div>
    `;
    return card;
}

// Fonction pour créer un nouveau modèle
async function createModel(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const modelData = {
        name: formData.get('name'),
        type: formData.get('type'),
        framework: formData.get('framework'),
        description: formData.get('description'),
        hyperparameters: JSON.parse(formData.get('hyperparameters'))
    };
    
    try {
        const response = await fetch(`${API_URL}/models`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(modelData)
        });
        
        if (response.ok) {
            showAlert('Modèle créé avec succès', 'success');
            loadModels();
            event.target.reset();
        } else {
            throw new Error('Erreur lors de la création du modèle');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// Fonction pour entraîner un modèle
async function trainModel(modelId) {
    const fileInput = document.getElementById('training-file');
    if (!fileInput.files.length) {
        showAlert('Veuillez sélectionner un fichier de données', 'warning');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/models/${modelId}/train`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showAlert('Entraînement terminé avec succès', 'success');
            loadDashboard();
        } else {
            throw new Error('Erreur lors de l\'entraînement');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        showLoading(false);
    }
}

// Fonction pour supprimer un modèle
async function deleteModel(modelId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce modèle ?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/models/${modelId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Modèle supprimé avec succès', 'success');
            loadModels();
            loadDashboard();
        } else {
            throw new Error('Erreur lors de la suppression');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// Fonction pour afficher une alerte
function showAlert(message, type) {
    const alert = document.getElementById('alert');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alert.style.display = 'block';
    
    setTimeout(() => {
        alert.style.display = 'none';
    }, 5000);
}

// Fonction pour afficher/masquer le spinner de chargement
function showLoading(show) {
    document.getElementById('loading-spinner').style.display = show ? 'block' : 'none';
}

// Fonction pour mettre à jour le graphique de performance
function updatePerformanceChart(models) {
    const ctx = document.getElementById('performance-chart').getContext('2d');
    
    const data = {
        labels: models.map(m => m.name),
        datasets: [{
            label: 'Précision',
            data: models.map(m => m.metrics?.accuracy || 0),
            backgroundColor: 'rgba(52, 152, 219, 0.5)',
            borderColor: 'rgba(52, 152, 219, 1)',
            borderWidth: 1
        }]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

// Configuration des gestionnaires de formulaires
function setupFormHandlers() {
    const createModelForm = document.getElementById('create-model-form');
    if (createModelForm) {
        createModelForm.addEventListener('submit', createModel);
    }
} 