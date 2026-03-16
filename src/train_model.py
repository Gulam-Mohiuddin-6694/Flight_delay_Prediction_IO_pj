import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import FlightDataPreprocessor

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and compare performance"""
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        print(f"{name} Results:")
        print(f"Accuracy: {results[name]['accuracy']:.4f}")
        print(f"Precision: {results[name]['precision']:.4f}")
        print(f"Recall: {results[name]['recall']:.4f}")
        print(f"F1 Score: {results[name]['f1']:.4f}")
    
    return results

def select_best_model(results):
    """Select best model based on F1 score"""
    best_model_name = max(results, key=lambda x: results[x]['f1'])
    print(f"\nBest Model: {best_model_name}")
    return best_model_name, results[best_model_name]['model']

def plot_confusion_matrix(cm, model_name):
    """Plot confusion matrix"""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(f'../static/confusion_matrix_{model_name.replace(" ", "_")}.png')
    plt.close()

def main():
    # Initialize preprocessor
    preprocessor = FlightDataPreprocessor()
    
    # Load data
    print("Loading dataset...")
    df = preprocessor.load_data('../data/flights.csv')
    
    # Clean data
    df = preprocessor.clean_data(df)
    
    # Create features
    df = preprocessor.create_features(df)
    
    # Create target variable
    df = preprocessor.create_target(df)
    
    # Define feature columns (adjust based on your dataset)
    categorical_cols = ['OP_CARRIER', 'ORIGIN', 'DEST']
    numerical_cols = ['DISTANCE', 'MONTH', 'DAY_OF_WEEK', 'HOUR', 'IS_PEAK_HOUR', 'IS_WEEKEND']
    
    # Check which columns exist
    categorical_cols = [col for col in categorical_cols if col in df.columns]
    numerical_cols = [col for col in numerical_cols if col in df.columns]
    
    # Encode categorical variables
    df = preprocessor.encode_categorical(df, categorical_cols, fit=True)
    
    # Prepare features
    feature_cols = categorical_cols + numerical_cols
    X = df[feature_cols]
    y = df['IS_DELAYED']
    
    # Scale features
    X_scaled = preprocessor.prepare_features(X, feature_cols, fit=True)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train models
    results = train_models(X_train, X_test, y_train, y_test)
    
    # Select best model
    best_model_name, best_model = select_best_model(results)
    
    # Plot confusion matrix for best model
    plot_confusion_matrix(results[best_model_name]['confusion_matrix'], best_model_name)
    
    # Save best model
    joblib.dump(best_model, '../models/delay_model.pkl')
    print(f"\nBest model saved to models/delay_model.pkl")
    
    # Save preprocessor
    preprocessor.save_preprocessor('../models/preprocessor.pkl')
    
    # Save feature columns
    joblib.dump(feature_cols, '../models/feature_columns.pkl')
    print("Feature columns saved")

if __name__ == "__main__":
    main()
