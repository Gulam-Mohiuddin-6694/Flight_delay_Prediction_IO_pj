import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import xgboost as xgb

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_names = None
    
    def train_logistic_regression(self, X_train, y_train):
        """Train Logistic Regression model"""
        print("\nTraining Logistic Regression...")
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        return model
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest model"""
        print("\nTraining Random Forest...")
        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        return model
    
    def train_gradient_boosting(self, X_train, y_train):
        """Train Gradient Boosting model"""
        print("\nTraining Gradient Boosting...")
        model = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        return model
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost model"""
        print("\nTraining XGBoost...")
        model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
        model.fit(X_train, y_train)
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"\n{'='*50}")
        print(f"{model_name} Results")
        print(f"{'='*50}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"\nConfusion Matrix:")
        print(cm)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'confusion_matrix': cm
        }
    
    def train_all_models(self, X_train, y_train, X_test, y_test, feature_names):
        """Train and evaluate all models"""
        self.feature_names = feature_names
        results = {}
        
        # Logistic Regression
        lr_model = self.train_logistic_regression(X_train, y_train)
        self.models['Logistic Regression'] = lr_model
        results['Logistic Regression'] = self.evaluate_model(lr_model, X_test, y_test, 'Logistic Regression')
        
        # Random Forest
        rf_model = self.train_random_forest(X_train, y_train)
        self.models['Random Forest'] = rf_model
        results['Random Forest'] = self.evaluate_model(rf_model, X_test, y_test, 'Random Forest')
        
        # Gradient Boosting
        gb_model = self.train_gradient_boosting(X_train, y_train)
        self.models['Gradient Boosting'] = gb_model
        results['Gradient Boosting'] = self.evaluate_model(gb_model, X_test, y_test, 'Gradient Boosting')
        
        # XGBoost
        xgb_model = self.train_xgboost(X_train, y_train)
        self.models['XGBoost'] = xgb_model
        results['XGBoost'] = self.evaluate_model(xgb_model, X_test, y_test, 'XGBoost')
        
        # Select best model based on F1 score
        best_f1 = 0
        for name, metrics in results.items():
            if metrics['f1'] > best_f1:
                best_f1 = metrics['f1']
                self.best_model_name = name
                self.best_model = self.models[name]
        
        print(f"\n{'='*50}")
        print(f"BEST MODEL: {self.best_model_name}")
        print(f"F1 Score: {best_f1:.4f}")
        print(f"{'='*50}\n")
        
        return results
    
    def save_model(self, filepath, preprocessor=None):
        """Save the best model and preprocessor"""
        if self.best_model is None:
            print("No model to save. Train models first.")
            return
        
        model_data = {
            'model': self.best_model,
            'model_name': self.best_model_name,
            'feature_names': self.feature_names,
            'preprocessor': preprocessor
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a saved model"""
        try:
            model_data = joblib.load(filepath)
            self.best_model = model_data['model']
            self.best_model_name = model_data['model_name']
            self.feature_names = model_data['feature_names']
            print(f"Model loaded: {self.best_model_name}")
            return model_data
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def get_feature_importance(self):
        """Get feature importance from the best model"""
        if self.best_model is None:
            return None
        
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            feature_importance = list(zip(self.feature_names, importances))
            feature_importance.sort(key=lambda x: x[1], reverse=True)
            return feature_importance
        
        return None
