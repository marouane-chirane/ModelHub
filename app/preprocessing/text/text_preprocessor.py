from typing import List, Optional, Dict, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from app.preprocessing.base import BasePreprocessor

class TextPreprocessor(BasePreprocessor):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Télécharger les ressources NLTK nécessaires
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
    
    def _clean_text(self, text: str) -> str:
        """Nettoie le texte en enlevant les caractères spéciaux et la ponctuation."""
        # Convertir en minuscules
        text = text.lower()
        # Enlever les caractères spéciaux et les chiffres
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Enlever les espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenise le texte."""
        return word_tokenize(text)
    
    def _remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Enlève les mots vides."""
        return [token for token in tokens if token not in self.stop_words]
    
    def _lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatise les tokens."""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def fit(self, data: List[str]) -> 'TextPreprocessor':
        """Ajuste le préprocesseur aux données."""
        # Dans ce cas, il n'y a pas besoin d'ajustement spécifique
        return super().fit(data)
    
    def transform(self, data: List[str]) -> List[str]:
        """Transforme les données textuelles."""
        if not self.is_fitted:
            raise ValueError("Le préprocesseur doit être ajusté avant la transformation.")
        
        processed_texts = []
        for text in data:
            # Nettoyer le texte
            cleaned_text = self._clean_text(text)
            # Tokeniser
            tokens = self._tokenize(cleaned_text)
            # Enlever les mots vides
            tokens = self._remove_stopwords(tokens)
            # Lemmatiser
            tokens = self._lemmatize(tokens)
            # Rejoindre les tokens
            processed_text = ' '.join(tokens)
            processed_texts.append(processed_text)
        
        return processed_texts
    
    def save(self, path: str) -> None:
        """Sauvegarde le préprocesseur."""
        import pickle
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, path: str) -> 'TextPreprocessor':
        """Charge un préprocesseur sauvegardé."""
        import pickle
        with open(path, 'rb') as f:
            return pickle.load(f) 