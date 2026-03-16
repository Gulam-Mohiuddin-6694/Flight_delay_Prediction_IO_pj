import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sns.set_style('whitegrid')

class FlightVisualizer:
    def __init__(self):
        self.figures = []
    
    def plot_delay_distribution(self, df, save_path=None):
        """Plot distribution of delays"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if 'DELAYED' in df.columns:
            delay_counts = df['DELAYED'].value_counts()
            labels = ['On Time', 'Delayed']
            colors = ['#2ecc71', '#e74c3c']
            
            ax.bar(labels, delay_counts.values, color=colors, alpha=0.7)
            ax.set_ylabel('Number of Flights', fontsize=12)
            ax.set_title('Flight Delay Distribution', fontsize=14, fontweight='bold')
            
            for i, v in enumerate(delay_counts.values):
                ax.text(i, v + 100, str(v), ha='center', fontweight='bold')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_delays_by_airline(self, df, save_path=None):
        """Plot delays by airline"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        airline_col = 'OP_CARRIER' if 'OP_CARRIER' in df.columns else 'AIRLINE'
        
        if airline_col in df.columns and 'DELAYED' in df.columns:
            delay_by_airline = df.groupby(airline_col)['DELAYED'].agg(['sum', 'count'])
            delay_by_airline['delay_rate'] = (delay_by_airline['sum'] / delay_by_airline['count'] * 100)
            delay_by_airline = delay_by_airline.sort_values('delay_rate', ascending=False).head(15)
            
            ax.barh(range(len(delay_by_airline)), delay_by_airline['delay_rate'], color='#3498db', alpha=0.7)
            ax.set_yticks(range(len(delay_by_airline)))
            ax.set_yticklabels(delay_by_airline.index)
            ax.set_xlabel('Delay Rate (%)', fontsize=12)
            ax.set_title('Delay Rate by Airline', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_delays_by_airport(self, df, save_path=None):
        """Plot delays by origin airport"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'ORIGIN' in df.columns and 'DELAYED' in df.columns:
            delay_by_airport = df.groupby('ORIGIN')['DELAYED'].agg(['sum', 'count'])
            delay_by_airport['delay_rate'] = (delay_by_airport['sum'] / delay_by_airport['count'] * 100)
            delay_by_airport = delay_by_airport[delay_by_airport['count'] > 100]
            delay_by_airport = delay_by_airport.sort_values('delay_rate', ascending=False).head(15)
            
            ax.barh(range(len(delay_by_airport)), delay_by_airport['delay_rate'], color='#e67e22', alpha=0.7)
            ax.set_yticks(range(len(delay_by_airport)))
            ax.set_yticklabels(delay_by_airport.index)
            ax.set_xlabel('Delay Rate (%)', fontsize=12)
            ax.set_title('Delay Rate by Origin Airport', fontsize=14, fontweight='bold')
            ax.invert_yaxis()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_delays_by_time(self, df, save_path=None):
        """Plot delays by hour of day"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'HOUR' in df.columns and 'DELAYED' in df.columns:
            delay_by_hour = df.groupby('HOUR')['DELAYED'].agg(['sum', 'count'])
            delay_by_hour['delay_rate'] = (delay_by_hour['sum'] / delay_by_hour['count'] * 100)
            
            ax.plot(delay_by_hour.index, delay_by_hour['delay_rate'], marker='o', linewidth=2, color='#9b59b6')
            ax.fill_between(delay_by_hour.index, delay_by_hour['delay_rate'], alpha=0.3, color='#9b59b6')
            ax.set_xlabel('Hour of Day', fontsize=12)
            ax.set_ylabel('Delay Rate (%)', fontsize=12)
            ax.set_title('Delay Rate by Hour of Day', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_delays_by_day(self, df, save_path=None):
        """Plot delays by day of week"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if 'DAY_OF_WEEK' in df.columns and 'DELAYED' in df.columns:
            delay_by_day = df.groupby('DAY_OF_WEEK')['DELAYED'].agg(['sum', 'count'])
            delay_by_day['delay_rate'] = (delay_by_day['sum'] / delay_by_day['count'] * 100)
            
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            colors = ['#3498db' if i < 5 else '#e74c3c' for i in range(7)]
            
            ax.bar(range(7), delay_by_day['delay_rate'], color=colors, alpha=0.7)
            ax.set_xticks(range(7))
            ax.set_xticklabels(days)
            ax.set_ylabel('Delay Rate (%)', fontsize=12)
            ax.set_title('Delay Rate by Day of Week', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_confusion_matrix(self, cm, save_path=None):
        """Plot confusion matrix"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, ax=ax)
        ax.set_xlabel('Predicted', fontsize=12)
        ax.set_ylabel('Actual', fontsize=12)
        ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
        ax.set_xticklabels(['On Time', 'Delayed'])
        ax.set_yticklabels(['On Time', 'Delayed'])
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_feature_importance(self, feature_importance, save_path=None):
        """Plot feature importance"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        features = [f[0] for f in feature_importance[:15]]
        importances = [f[1] for f in feature_importance[:15]]
        
        ax.barh(range(len(features)), importances, color='#16a085', alpha=0.7)
        ax.set_yticks(range(len(features)))
        ax.set_yticklabels(features)
        ax.set_xlabel('Importance', fontsize=12)
        ax.set_title('Top 15 Feature Importances', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def plot_model_comparison(self, results, save_path=None):
        """Plot comparison of model performances"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        models = list(results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1']
        titles = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        
        for idx, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[idx // 2, idx % 2]
            values = [results[model][metric] for model in models]
            
            bars = ax.bar(models, values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'], alpha=0.7)
            ax.set_ylabel(title, fontsize=12)
            ax.set_title(f'Model Comparison - {title}', fontsize=12, fontweight='bold')
            ax.set_ylim([0, 1])
            ax.tick_params(axis='x', rotation=45)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        return fig
    
    def generate_all_visualizations(self, df, results=None, feature_importance=None):
        """Generate all visualizations"""
        print("\nGenerating visualizations...")
        
        self.plot_delay_distribution(df)
        self.plot_delays_by_airline(df)
        self.plot_delays_by_airport(df)
        self.plot_delays_by_time(df)
        self.plot_delays_by_day(df)
        
        if results:
            self.plot_model_comparison(results)
        
        if feature_importance:
            self.plot_feature_importance(feature_importance)
        
        print("Visualizations complete!")
