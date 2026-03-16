import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

class FlightDataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_data(self, filepath):
        """Load flight data from CSV"""
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} records")
        return df
    
    def clean_data(self, df):
        """Remove missing values and outliers"""
        initial_rows = len(df)
        df = df.dropna()
        print(f"Removed {initial_rows - len(df)} rows with missing values")
        return df
    
    def create_features(self, df):
        """Create additional features"""
        # Peak hour feature (6-9 AM and 4-7 PM)
        if 'CRS_DEP_TIME' in df.columns:
            df['HOUR'] = (df['CRS_DEP_TIME'] // 100).astype(int)
            df['IS_PEAK_HOUR'] = df['HOUR'].apply(lambda x: 1 if (6 <= x <= 9) or (16 <= x <= 19) else 0)
        
        # Weekend feature
        if 'DAY_OF_WEEK' in df.columns:
            df['IS_WEEKEND'] = df['DAY_OF_WEEK'].apply(lambda x: 1 if x in [6, 7] else 0)
        
        return df
    
    def encode_categorical(self, df, categorical_cols, fit=True):
        """Encode categorical variables"""
        for col in categorical_cols:
            if col in df.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    if col in self.label_encoders:
                        df[col] = self.label_encoders[col].transform(df[col].astype(str))
        return df
    
    def create_target(self, df, delay_threshold=15):
        """Create binary target: 1 if delayed, 0 otherwise"""
        if 'DEP_DELAY' in df.columns:
            df['IS_DELAYED'] = (df['DEP_DELAY'] > delay_threshold).astype(int)
        elif 'DEPARTURE_DELAY' in df.columns:
            df['IS_DELAYED'] = (df['DEPARTURE_DELAY'] > delay_threshold).astype(int)
        elif 'ARR_DELAY' in df.columns:
            df['IS_DELAYED'] = (df['ARR_DELAY'] > delay_threshold).astype(int)
        return df
    
    def prepare_features(self, df, feature_cols, fit=True):
        """Scale numerical features"""
        if fit:
            self.feature_columns = feature_cols
            scaled_features = self.scaler.fit_transform(df[feature_cols])
        else:
            scaled_features = self.scaler.transform(df[feature_cols])
        return pd.DataFrame(scaled_features, columns=feature_cols, index=df.index)
    
    def save_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Save preprocessor objects"""
        joblib.dump({
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, filepath)
        print(f"Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Load preprocessor objects"""
        data = joblib.load(filepath)
        self.label_encoders = data['label_encoders']
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']
        print(f"Preprocessor loaded from {filepath}")
