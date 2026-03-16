"""
Dataset Setup Guide
===================

This script helps you prepare the flight delay dataset for training.

STEP 1: Download Dataset from Kaggle
-------------------------------------
Visit one of these Kaggle datasets:

Option 1 (Recommended):
https://www.kaggle.com/datasets/usdot/flight-delays
- Download: flights.csv

Option 2:
https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018
- Download any year's CSV file

STEP 2: Place Dataset
----------------------
1. Place the downloaded CSV file in the 'data/' folder
2. Rename it to 'flights.csv'

STEP 3: Verify Dataset
----------------------
Run this script to verify your dataset has the required columns.
"""

import pandas as pd
import os

def verify_dataset():
    """Verify the dataset has required columns"""
    
    dataset_path = 'data/flights.csv'
    
    if not os.path.exists(dataset_path):
        print("❌ ERROR: Dataset not found!")
        print(f"   Please place your dataset at: {dataset_path}")
        print("\n📥 Download from:")
        print("   https://www.kaggle.com/datasets/usdot/flight-delays")
        return False
    
    print("✅ Dataset file found!")
    print(f"   Location: {dataset_path}")
    
    try:
        # Load first few rows
        df = pd.read_csv(dataset_path, nrows=5)
        print(f"\n✅ Dataset loaded successfully!")
        print(f"   Columns found: {len(df.columns)}")
        print(f"\n📋 Available columns:")
        for col in df.columns:
            print(f"   - {col}")
        
        # Check for required columns
        required_cols = {
            'airline': ['OP_CARRIER', 'AIRLINE', 'CARRIER'],
            'origin': ['ORIGIN', 'ORIGIN_AIRPORT'],
            'destination': ['DEST', 'DESTINATION_AIRPORT'],
            'distance': ['DISTANCE'],
            'delay': ['DEP_DELAY', 'DEPARTURE_DELAY', 'ARR_DELAY']
        }
        
        print("\n🔍 Checking required columns:")
        all_found = True
        for category, possible_names in required_cols.items():
            found = any(col in df.columns for col in possible_names)
            status = "✅" if found else "❌"
            print(f"   {status} {category.upper()}: {', '.join(possible_names)}")
            if not found:
                all_found = False
        
        if all_found:
            print("\n✅ All required columns found!")
            print("   You can now run: python src/train_model.py")
        else:
            print("\n⚠️  Some required columns are missing.")
            print("   You may need to adjust column names in train_model.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error reading dataset: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Flight Delay Dataset Verification")
    print("=" * 60)
    print()
    verify_dataset()
    print("\n" + "=" * 60)
