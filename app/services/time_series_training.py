import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from app.models.time_series_models import TimeSeriesModel
from app.db.session import SessionLocal

class TimeSeriesTrainer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        
    def prepare_data(self, data, sequence_length):
        """Prépare les données pour l'entraînement LSTM"""
        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))
        X, y = [], []
        for i in range(len(scaled_data) - sequence_length):
            X.append(scaled_data[i:(i + sequence_length)])
            y.append(scaled_data[i + sequence_length])
        return np.array(X), np.array(y)
    
    def train_arima(self, data, order=(1,1,1)):
        """Entraîne un modèle ARIMA"""
        model = ARIMA(data, order=order)
        results = model.fit()
        return results
    
    def train_sarima(self, data, order=(1,1,1), seasonal_order=(1,1,1,12)):
        """Entraîne un modèle SARIMA"""
        model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
        results = model.fit()
        return results
    
    def train_prophet(self, data, seasonality_mode='additive'):
        """Entraîne un modèle Prophet"""
        df = pd.DataFrame({
            'ds': data.index,
            'y': data.values
        })
        model = Prophet(seasonality_mode=seasonality_mode)
        model.fit(df)
        return model
    
    def train_lstm(self, data, sequence_length=10, epochs=50):
        """Entraîne un modèle LSTM"""
        X, y = self.prepare_data(data, sequence_length)
        
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(sequence_length, 1), return_sequences=True),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=epochs, batch_size=32, verbose=0)
        return model
    
    def evaluate_model(self, model, test_data, model_type):
        """Évalue les performances du modèle"""
        if model_type == 'arima' or model_type == 'sarima':
            predictions = model.forecast(len(test_data))
        elif model_type == 'prophet':
            future = model.make_future_dataframe(periods=len(test_data))
            predictions = model.predict(future)['yhat'][-len(test_data):]
        elif model_type == 'lstm':
            X_test, _ = self.prepare_data(test_data, 10)
            predictions = model.predict(X_test)
            predictions = self.scaler.inverse_transform(predictions)
        
        mse = np.mean((test_data - predictions) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(test_data - predictions))
        mape = np.mean(np.abs((test_data - predictions) / test_data)) * 100
        
        return {
            'rmse': rmse,
            'mae': mae,
            'mape': mape
        }
    
    def save_model(self, model_data):
        """Sauvegarde le modèle dans la base de données"""
        db = SessionLocal()
        try:
            model = TimeSeriesModel(**model_data)
            db.add(model)
            db.commit()
            db.refresh(model)
            return model
        finally:
            db.close() 