import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import yfinance as yf
from datetime import datetime, timedelta

class StockTradingML:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
    def prepare_features(self, data):
        """Calculate technical indicators as features"""
        df = data.copy()
        
        # Calculate moving averages
        df['SMA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
        df['SMA50'] = df['Close'].rolling(window=50, min_periods=1).mean()
        
        # Calculate price momentum
        df['Price_Change'] = df['Close'].pct_change().fillna(0)
        df['Price_Change_5'] = df['Close'].pct_change(periods=5).fillna(0)
        
        # Calculate RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['RSI'] = df['RSI'].fillna(50)  # Fill NaN with neutral RSI value
        
        # Create features array
        features = ['SMA20', 'SMA50', 'Price_Change', 'Price_Change_5', 'RSI']
        X = df[features]
        
        return X
    
    def create_labels(self, data, threshold=0.02):
        """Create trading signals (0: Hold, 1: Buy, 2: Sell)"""
        returns = data['Close'].pct_change()
        labels = np.zeros(len(returns))
        
        # Buy signal if return > threshold
        labels[returns > threshold] = 1
        # Sell signal if return < -threshold
        labels[returns < -threshold] = 2
        
        return labels[1:]  # Shift labels by 1 to align with future returns
    
    def train(self, historical_data):
        """Train the model"""
        X = self.prepare_features(historical_data)
        y = self.create_labels(historical_data)
        
        # Align X with y by removing the first row of X
        X = X.iloc[1:]
        
        # Remove any rows with NaN values
        valid_data = ~np.isnan(y)
        X = X[valid_data]
        y = y[valid_data]
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
        return self.model.score(X_test_scaled, y_test)
    
    def predict(self, current_data):
        """Make trading decision for current data"""
        X = self.prepare_features(current_data)
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)
        return prediction[-1]  # Return the most recent prediction

# Example usage:
if __name__ == "__main__":
    # Fetch real historical data for Tesla (TSLA)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Get 1 year of data
    
    stock = yf.Ticker("TSLA")
    historical_data = stock.history(start=start_date, end=end_date)
    
    # Initialize and train the model
    trader = StockTradingML()
    accuracy = trader.train(historical_data)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Make prediction for the most recent data
    decision = trader.predict(historical_data)
    latest_price = historical_data['Close'].iloc[-1]
    print(f"Latest stock price: ${latest_price:.2f}")
    print(f"Trading decision: {['Hold', 'Buy', 'Sell'][int(decision)]}")
    