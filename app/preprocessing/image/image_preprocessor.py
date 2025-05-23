from typing import List, Optional, Dict, Any, Tuple
import cv2
import numpy as np
from PIL import Image
from app.preprocessing.base import BasePreprocessor

class ImagePreprocessor(BasePreprocessor):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.target_size = config.get('target_size', (224, 224))
        self.normalize = config.get('normalize', True)
        self.mean = config.get('mean', [0.485, 0.456, 0.406])
        self.std = config.get('std', [0.229, 0.224, 0.225])
    
    def _resize_image(self, image: np.ndarray) -> np.ndarray:
        """Redimensionne l'image à la taille cible."""
        return cv2.resize(image, self.target_size)
    
    def _normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalise l'image."""
        if not self.normalize:
            return image
        
        # Convertir en float32
        image = image.astype(np.float32)
        
        # Normaliser
        image = image / 255.0
        
        # Appliquer la normalisation par canal
        for i in range(3):
            image[:, :, i] = (image[:, :, i] - self.mean[i]) / self.std[i]
        
        return image
    
    def _preprocess_single_image(self, image: np.ndarray) -> np.ndarray:
        """Prétraite une seule image."""
        # Redimensionner
        image = self._resize_image(image)
        
        # Normaliser
        image = self._normalize_image(image)
        
        return image
    
    def fit(self, data: List[np.ndarray]) -> 'ImagePreprocessor':
        """Ajuste le préprocesseur aux données."""
        # Dans ce cas, il n'y a pas besoin d'ajustement spécifique
        return super().fit(data)
    
    def transform(self, data: List[np.ndarray]) -> np.ndarray:
        """Transforme les données d'images."""
        if not self.is_fitted:
            raise ValueError("Le préprocesseur doit être ajusté avant la transformation.")
        
        processed_images = []
        for image in data:
            # Convertir en RGB si nécessaire
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            
            # Prétraiter l'image
            processed_image = self._preprocess_single_image(image)
            processed_images.append(processed_image)
        
        return np.array(processed_images)
    
    def save(self, path: str) -> None:
        """Sauvegarde le préprocesseur."""
        import pickle
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, path: str) -> 'ImagePreprocessor':
        """Charge un préprocesseur sauvegardé."""
        import pickle
        with open(path, 'rb') as f:
            return pickle.load(f) 