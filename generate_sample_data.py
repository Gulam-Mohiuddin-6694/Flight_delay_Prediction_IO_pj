"""
Sample Dataset Generator
=========================

This script generates a sample flight delay dataset for testing purposes.
Use this if you want to test the application without downloading from Kaggle.

Note: For production use, download real data from Kaggle for better accuracy.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_dataset(n_samples=50000):
    """Generate synthetic flight delay dataset"""
    
    print(f"Generating {n_samples} sample flight records...")
    
    np.random.seed(42)
    
    # Airlines
    airlines = ['AA', 'DL', 'UA', 'WN', 'B6', 'AS', 'NK', 'F9', 'AI', '6E', 'SG', 'UK', 'G8', 'EK', 'SQ', 'BA', 'LH', 'QR']
    
    # Airports
    airports = ['ATL', 'ORD', 'DFW', 'DEN', 'LAX', 'JFK', 'SFO', 'LAS', 'SEA', 'MCO', 
                'BOS', 'MIA', 'DEL', 'BOM', 'BLR', 'MAA', 'HYD', 'CCU', 'AMD', 'PNQ', 
                'GOI', 'COK', 'DXB', 'SIN', 'LHR', 'CDG', 'FRA', 'HKG', 'NRT', 'ICN', 
                'BKK', 'KUL', 'SYD', 'MEL']
    
    # Generate data
    data = {
        'OP_CARRIER': np.random.choice(airlines, n_samples),
        'ORIGIN': np.random.choice(airports, n_samples),
        'DEST': np.random.choice(airports, n_samples),
        'MONTH': np.random.randint(1, 13, n_samples),
        'DAY_OF_WEEK': np.random.randint(1, 8, n_samples),
        'CRS_DEP_TIME': np.random.randint(0, 2400, n_samples),
        'DISTANCE': np.random.randint(100, 3000, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Remove same origin-destination
    df = df[df['ORIGIN'] != df['DEST']]
    
    # Generate delays based on realistic factors
    base_delay = np.random.normal(0, 20, len(df))
    
    # Add delay factors
    # Peak hours (6-9 AM, 4-7 PM)
    df['HOUR'] = (df['CRS_DEP_TIME'] // 100).astype(int)
    peak_hours = ((df['HOUR'] >= 6) & (df['HOUR'] <= 9)) | ((df['HOUR'] >= 16) & (df['HOUR'] <= 19))
    base_delay += peak_hours * np.random.normal(10, 5, len(df))
    
    # Weekend effect
    weekend = df['DAY_OF_WEEK'].isin([6, 7])
    base_delay += weekend * np.random.normal(-5, 3, len(df))
    
    # Winter months (Dec, Jan, Feb)
    winter = df['MONTH'].isin([12, 1, 2])
    base_delay += winter * np.random.normal(15, 8, len(df))
    
    # Distance effect (longer flights slightly more delays)
    base_delay += (df['DISTANCE'] / 1000) * np.random.normal(2, 1, len(df))
    
    # Airline effect (some airlines more reliable)
    airline_factors = {'AA': 0, 'DL': -5, 'UA': 2, 'WN': -3, 'B6': 5, 'AS': -4, 'NK': 8, 'F9': 7,
                      'AI': 3, '6E': -2, 'SG': 4, 'UK': -3, 'G8': 5,
                      'EK': -6, 'SQ': -7, 'BA': -2, 'LH': -4, 'QR': -5}
    for airline, factor in airline_factors.items():
        mask = df['OP_CARRIER'] == airline
        base_delay[mask] += np.random.normal(factor, 3, mask.sum())
    
    # Add some random extreme delays
    extreme_delays = np.random.choice([0, 1], len(df), p=[0.95, 0.05])
    base_delay += extreme_delays * np.random.uniform(60, 180, len(df))
    
    df['DEP_DELAY'] = base_delay
    
    # Remove negative delays (early departures) for simplicity
    df['DEP_DELAY'] = df['DEP_DELAY'].clip(lower=-15)
    
    # Add arrival delay (correlated with departure delay)
    df['ARR_DELAY'] = df['DEP_DELAY'] + np.random.normal(0, 10, len(df))
    
    # Select final columns
    final_df = df[['OP_CARRIER', 'ORIGIN', 'DEST', 'MONTH', 'DAY_OF_WEEK', 
                    'CRS_DEP_TIME', 'DISTANCE', 'DEP_DELAY', 'ARR_DELAY']]
    
    return final_df

def main():
    print("=" * 60)
    print("Sample Flight Delay Dataset Generator")
    print("=" * 60)
    print()
    
    # Generate dataset
    df = generate_sample_dataset(50000)
    
    # Save to CSV
    output_path = 'data/flights.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset generated successfully!")
    print(f"   Location: {output_path}")
    print(f"   Records: {len(df):,}")
    print(f"   Columns: {', '.join(df.columns)}")
    
    # Show statistics
    print(f"\nDataset Statistics:")
    print(f"   Average Delay: {df['DEP_DELAY'].mean():.2f} minutes")
    print(f"   Median Delay: {df['DEP_DELAY'].median():.2f} minutes")
    print(f"   Delayed Flights (>15 min): {(df['DEP_DELAY'] > 15).sum():,} ({(df['DEP_DELAY'] > 15).mean()*100:.1f}%)")
    
    print(f"\n   Airlines: {', '.join(df['OP_CARRIER'].unique())}")
    print(f"   Airports: {', '.join(sorted(df['ORIGIN'].unique()))}")
    
    print("\nNext Step: Run 'python src/train_model.py' to train the model")
    print("=" * 60)

if __name__ == "__main__":
    main()
