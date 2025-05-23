from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pandas as pd
import numpy as np

class BasePreprocessor(ABC):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, data: Any) -> 'BasePreprocessor':
        """Ajuste le préprocesseur aux données."""
        self.is_fitted = True
        return self
    
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transforme les données."""
        if not self.is_fitted:
            raise ValueError("Le préprocesseur doit être ajusté avant la transformation.")
    
    def fit_transform(self, data: Any) -> Any:
        """Ajuste et transforme les données en une seule étape."""
        return self.fit(data).transform(data)
    
    def save(self, path: str) -> None:
        """Sauvegarde le préprocesseur."""
        raise NotImplementedError
    
    @classmethod
    def load(cls, path: str) -> 'BasePreprocessor':
        """Charge un préprocesseur sauvegardé."""
        raise NotImplementedError 