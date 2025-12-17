"""
Machine Learning Model Training dengan MLflow Tracking
Dataset: Heart Disease
Author: Raifal Bagus Afdiansah
Python: 3.12.7
MLflow: 2.19.0
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import warnings
import os
import argparse
import sys

warnings.filterwarnings('ignore')

def load_preprocessed_data(file_path):
    """
    Memuat dataset yang sudah dipreprocessing
    
    Parameters:
    -----------
    file_path : str
        Path ke file CSV dataset yang sudah dipreprocessing
    
    Returns:
    --------
    X_train, X_test, y_train, y_test : tuple
        Data training dan testing yang sudah dipreprocess
    """
    print("="*70)
    print("📊 LOADING PREPROCESSED DATA")
    print("="*70)
    
    # Load preprocessed dataset
    df = pd.read_csv(file_path)
    print(f"✅ Dataset loaded: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Split berdasarkan kolom 'split'
    train_data = df[df['split'] == 'train'].copy()
    test_data = df[df['split'] == 'test'].copy()
    
    # Drop kolom 'split'
    train_data = train_data.drop('split', axis=1)
    test_data = test_data.drop('split', axis=1)
    
    # Pisahkan features dan target
    target_col = 'Heart Disease'
    X_train = train_data.drop(target_col, axis=1)
    y_train = train_data[target_col]
    X_test = test_data.drop(target_col, axis=1)
    y_test = test_data[target_col]
    
    print(f"\n✅ Training set: {X_train.shape}")
    print(f"✅ Testing set: {X_test.shape}")
    print(f"\n🎯 Training target distribution:\n{y_train.value_counts()}")
    print(f"\n🎯 Testing target distribution:\n{y_test.value_counts()}")
    print("="*70)
    
    return X_train, X_test, y_train, y_test

def evaluate_model(model, X_test, y_test, model_name):
    """
    Evaluasi performa model
    
    Parameters:
    -----------
    model : sklearn model
        Model yang sudah dilatih
    X_test : DataFrame
        Data testing features
    y_test : Series
        Data testing target
    model_name : str
        Nama model
    
    Returns:
    --------
    metrics : dict
        Dictionary berisi metrics evaluasi
    """
    # Prediksi
    y_pred = model.predict(X_test)
    
    # Hitung metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    metrics = {
        'test_accuracy': accuracy,
        'test_precision': precision,
        'test_recall': recall,
        'test_f1_score': f1
    }
    
    # Print results
    print(f"\n{'='*70}")
    print(f"📊 EVALUATION RESULTS - {model_name}")
    print(f"{'='*70}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    print(f"{'='*70}")
    
    return metrics

def train_model_with_mlflow(X_train, X_test, y_train, y_test, model, model_name, params=None):
    """
    Melatih model dengan MLflow tracking
    
    Parameters:
    -----------
    X_train, X_test, y_train, y_test : tuple
        Data training dan testing
    model : sklearn model
        Model yang akan dilatih
    model_name : str
        Nama model untuk tracking
    params : dict
        Parameter model (optional)
    """
    with mlflow.start_run(run_name=model_name) as run:
        print(f"\n{'='*70}")
        print(f"🚀 TRAINING MODEL: {model_name}")
        print(f"{'='*70}")
        
        # Log parameters
        if params:
            mlflow.log_params(params)
        
        # Train model
        model.fit(X_train, y_train)
        print(f"✅ Model trained successfully!")
        
        # Evaluate model
        metrics = evaluate_model(model, X_test, y_test, model_name)
        
        # Log metrics to MLflow
        mlflow.log_metrics(metrics)
        
        # Log model explicitly (autolog may not always work)
        mlflow.sklearn.log_model(model, "model")
        
        # Get run info for debugging
        run_id = run.info.run_id
        artifact_uri = run.info.artifact_uri
        print(f"\n📁 Run ID: {run_id}")
        print(f"📁 Artifact URI: {artifact_uri}")
        
        print(f"\n✅ MLflow tracking completed for {model_name}")
        
        return metrics

def main():
    """
    Fungsi utama untuk menjalankan pipeline training
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train ML models for Heart Disease Classification')
    parser.add_argument('--model_type', type=str, default='all',
                      choices=['all', 'Logistic_Regression', 'Random_Forest', 'Gradient_Boosting', 
                              'Decision_Tree', 'K_Nearest_Neighbors', 'Support_Vector_Machine'],
                      help='Model to train (default: all)')
    args = parser.parse_args()
    
    # Get the script's directory (where modelling.py is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Script directory: {script_dir}")
    print(f"📁 Current working directory: {os.getcwd()}")
    
    print("\n" + "="*70)
    print("🎯 MACHINE LEARNING MODEL TRAINING WITH MLFLOW")
    print("="*70)
    print("Dataset: Heart Disease")
    print("Author: Raifal Bagus Afdiansah")
    print(f"Model Type: {args.model_type}")
    print("="*70 + "\n")
    
    # Set MLflow tracking URI ke folder lokal (use script directory)
    mlflow_tracking_uri = os.path.join(script_dir, "mlruns")
    mlflow.set_tracking_uri(f"file:///{mlflow_tracking_uri}")
    print(f"📁 MLflow Tracking URI: {mlflow.get_tracking_uri()}")
    
    # Set experiment name
    experiment_name = "Heart_Disease_Classification"
    mlflow.set_experiment(experiment_name)
    print(f"🧪 Experiment Name: {experiment_name}\n")
    
    # Enable autolog untuk sklearn
    mlflow.sklearn.autolog(
        log_input_examples=True,
        log_model_signatures=True,
        log_models=True
    )
    print("✅ MLflow autolog enabled for sklearn\n")
    
    # Load preprocessed data (use script directory for correct path)
    preprocessed_path = os.path.join(script_dir, 'Heart_Disease_preprocessing.csv')
    X_train, X_test, y_train, y_test = load_preprocessed_data(preprocessed_path)
    
    # Define all available models
    all_models = [
        {
            'name': 'Logistic_Regression',
            'model': LogisticRegression(random_state=42, max_iter=1000),
            'params': {'random_state': 42, 'max_iter': 1000}
        },
        {
            'name': 'Random_Forest',
            'model': RandomForestClassifier(random_state=42, n_estimators=100),
            'params': {'random_state': 42, 'n_estimators': 100}
        },
        {
            'name': 'Gradient_Boosting',
            'model': GradientBoostingClassifier(random_state=42, n_estimators=100),
            'params': {'random_state': 42, 'n_estimators': 100}
        },
        {
            'name': 'Decision_Tree',
            'model': DecisionTreeClassifier(random_state=42),
            'params': {'random_state': 42}
        },
        {
            'name': 'K_Nearest_Neighbors',
            'model': KNeighborsClassifier(n_neighbors=5),
            'params': {'n_neighbors': 5}
        },
        {
            'name': 'Support_Vector_Machine',
            'model': SVC(random_state=42, kernel='rbf'),
            'params': {'random_state': 42, 'kernel': 'rbf'}
        }
    ]
    
    # Filter models based on model_type argument
    if args.model_type == 'all':
        models_to_train = all_models
    else:
        models_to_train = [m for m in all_models if m['name'] == args.model_type]
        if not models_to_train:
            print(f"❌ Model '{args.model_type}' not found!")
            sys.exit(1)
    
    # Train selected models with MLflow tracking
    all_results = []
    
    for model_config in models_to_train:
        try:
            metrics = train_model_with_mlflow(
                X_train, X_test, y_train, y_test,
                model_config['model'],
                model_config['name'],
                model_config['params']
            )
            all_results.append({
                'model': model_config['name'],
                **metrics
            })
        except Exception as e:
            print(f"❌ Error training {model_config['name']}: {e}")
    
    # Summary of all models
    if all_results:
        print("\n" + "="*70)
        print("📊 SUMMARY OF ALL MODELS")
        print("="*70)
        results_df = pd.DataFrame(all_results)
        results_df = results_df.sort_values('test_accuracy', ascending=False)
        print(results_df.to_string(index=False))
        print("="*70)
        
        # Save results - use script directory to ensure correct location
        csv_path = os.path.join(script_dir, 'model_comparison_results.csv')
        results_df.to_csv(csv_path, index=False)
        print(f"\n✅ Results saved to: {csv_path}")
        
        # Also save as JSON for easier parsing
        json_path = os.path.join(script_dir, 'model_comparison_results.json')
        results_df.to_json(json_path, orient='records', indent=2)
        print(f"✅ Results also saved to: {json_path}")
        
        # Verify files exist
        print(f"\n📂 Verifying output files:")
        print(f"   CSV exists: {os.path.exists(csv_path)}")
        print(f"   JSON exists: {os.path.exists(json_path)}")
    else:
        print("\n⚠️  No models were trained successfully!")
    
    print("\n" + "="*70)
    print("🎉 TRAINING COMPLETED!")
    print("="*70)
    print(f"\n📂 To view MLflow UI, run:")
    print(f"   mlflow ui --backend-store-uri file:///{mlflow_tracking_uri}")
    print(f"\n   Then open: http://localhost:5000")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
