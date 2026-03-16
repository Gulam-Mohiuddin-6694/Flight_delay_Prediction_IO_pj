import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def load_data(self, filepath):
        """Load flight data from CSV"""
        try:
            df = pd.read_csv(filepath)
            print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self, df):
        """Clean missing values and remove irrelevant columns"""
        print("Cleaning data...")
        
        # Drop rows with critical missing values
        df = df.dropna(subset=['DEP_DELAY', 'ARR_DELAY'], how='any')
        
        # Fill numeric columns with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        print(f"Data after cleaning: {df.shape[0]} rows")
        return df
    
    def create_target(self, df, delay_threshold=15):
        """Create binary target: 1 if delayed, 0 if on time"""
        if 'ARR_DELAY' in df.columns:
            df['DELAYED'] = (df['ARR_DELAY'] > delay_threshold).astype(int)
        elif 'DEP_DELAY' in df.columns:
            df['DELAYED'] = (df['DEP_DELAY'] > delay_threshold).astype(int)
        return df
    
    def engineer_features(self, df):
        """Create new features"""
        print("Engineering features...")
        
        # Peak hour indicator (6-9 AM, 4-7 PM)
        if 'CRS_DEP_TIME' in df.columns:
            df['HOUR'] = (df['CRS_DEP_TIME'] // 100).astype(int)
            df['PEAK_HOUR'] = df['HOUR'].apply(lambda x: 1 if (6 <= x <= 9) or (16 <= x <= 19) else 0)
        
        # Day of week (if DATE column exists)
        if 'FL_DATE' in df.columns:
            df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
            df['DAY_OF_WEEK'] = df['FL_DATE'].dt.dayofweek
            df['MONTH'] = df['FL_DATE'].dt.month
        
        # Weekend indicator
        if 'DAY_OF_WEEK' in df.columns:
            df['IS_WEEKEND'] = df['DAY_OF_WEEK'].apply(lambda x: 1 if x >= 5 else 0)
        
        return df
    
    def encode_categorical(self, df, categorical_cols):
        """Encode categorical variables"""
        print("Encoding categorical variables...")
        
        for col in categorical_cols:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def select_features(self, df):
        """Select relevant features for modeling"""
        # Common feature names across different datasets
        possible_features = [
            'MONTH', 'DAY_OF_WEEK', 'OP_CARRIER', 'ORIGIN', 'DEST',
            'CRS_DEP_TIME', 'DISTANCE', 'HOUR', 'PEAK_HOUR', 'IS_WEEKEND',
            'AIRLINE', 'DEP_TIME', 'ARR_TIME', 'FLIGHT_NUMBER'
        ]
        
        available_features = [f for f in possible_features if f in df.columns]
        
        if 'DELAYED' in df.columns:
            return df[available_features + ['DELAYED']]
        return df[available_features]
    
    def normalize_features(self, X_train, X_test):
        """Normalize numerical features"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def prepare_data(self, df, test_size=0.2, random_state=42):
        """Complete preprocessing pipeline"""
        df = self.clean_data(df)
        df = self.create_target(df)
        df = self.engineer_features(df)
        
        # Identify categorical columns
        categorical_cols = ['OP_CARRIER', 'ORIGIN', 'DEST', 'AIRLINE']
        df = self.encode_categorical(df, categorical_cols)
        
        # Select features
        df = self.select_features(df)
        
        # Split features and target
        X = df.drop('DELAYED', axis=1)
        y = df['DELAYED']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Normalize
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)
        
        print(f"Training set: {X_train_scaled.shape[0]} samples")
        print(f"Testing set: {X_test_scaled.shape[0]} samples")
        print(f"Delay rate: {y.mean():.2%}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test, X.columns.tolist()
