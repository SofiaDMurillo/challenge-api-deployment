
from lightgbm import early_stopping, log_evaluation, LGBMRegressor
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from pathlib import Path
import numpy as np
import pickle
import optuna

def main(optimize=False):
    # Load data
    base_path = Path(__file__).resolve().parent.parent
    train_set = pd.read_csv(base_path / 'data' / 'processed' / 'train_set.csv')
    test_set  = pd.read_csv(base_path / 'data' / 'processed' / 'test_set.csv')

    numeric_features = ['habitableSurface', 'bedroomCount','buildingCondition',
                        'hasGarden', 'gardenSurface', 'hasTerrace']
    categorical_features = ['postCode', 'type']
    target = 'price'

    # Convert categorical columns to 'category' dtype
    for col in categorical_features:
        train_set[col] = train_set[col].astype('category')
        test_set[col] = test_set[col].astype('category')

    # Separate X and y
    X_train_full = train_set[numeric_features + categorical_features]
    y_train_full = train_set[target]
    X_test  = test_set[numeric_features + categorical_features]
    y_test  = test_set[target]

    # Optional train/valid split for Optuna optimization
    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train_full, y_train_full, test_size=0.2, random_state=42
    )

    # Objective function for Optuna
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 200, 1000),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'num_leaves': trial.suggest_int('num_leaves', 20, 100),
            'min_child_samples': trial.suggest_int('min_child_samples', 5, 50),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 1.0),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 1.0),
            'random_state': 42
        }

        model = LGBMRegressor(**params)
        model.fit(
            X_train, y_train,
            categorical_feature=categorical_features,
            eval_set=[(X_valid, y_valid)],
            eval_metric="rmse",
            callbacks=[early_stopping(stopping_rounds=50), log_evaluation(0)]
        )

        preds = model.predict(X_valid)
        rmse = np.sqrt(mean_squared_error(y_valid, preds))
        return rmse

    # Run Optuna if optimize flag is True
    if optimize:
        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=50)
        print("✅ Best parameters found:")
        print(study.best_params)

        final_params = study.best_params
    else:
        # Default parameters (your original ones)
        final_params = {
            'n_estimators': 300,
            'learning_rate': 0.05,
            'max_depth': 6,
            'random_state': 42
        }

    # Final model training with best params on full training data
    model = LGBMRegressor(**final_params)
    model.fit(
        X_train_full, y_train_full,
        categorical_feature=categorical_features,
        eval_set=[(X_test, y_test)],
        eval_metric="rmse",
        callbacks=[early_stopping(stopping_rounds=100), log_evaluation(100)]
    )

    # Predict on train and test sets
    y_train_pred = model.predict(X_train_full)
    y_test_pred = model.predict(X_test)

    # Collect metrics
    metrics = {
        'Train_R2': r2_score(y_train_full, y_train_pred),
        'Train_RMSE': np.sqrt(mean_squared_error(y_train_full, y_train_pred)),
        'Train_MAE': mean_absolute_error(y_train_full, y_train_pred),
        'Test_R2': r2_score(y_test, y_test_pred),
        'Test_RMSE': np.sqrt(mean_squared_error(y_test, y_test_pred)),
        'Test_MAE': mean_absolute_error(y_test, y_test_pred)
    }

    # Print metrics
    print("✅ LightGBM Optuna Regression Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.3f}")

    # Save model
    model_path = base_path / 'outputs' / 'models'
    model_path.mkdir(parents=True, exist_ok=True)
    with open(model_path / 'model_lightgbm_Optuna_retrained.pkl', 'wb') as file:
        pickle.dump(model, file)

    # Save metrics report
    metrics_path = base_path / 'outputs' / 'reports'
    metrics_path.mkdir(parents=True, exist_ok=True)
    report_file = metrics_path / 'metrics_lightgbm_Optuna_retrained.txt'
    with open(report_file, 'w') as f:
        f.write("LightGBM Optuna Regression Metrics Report\n\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value:.3f}\n")

    print(f"\n✅ Model and metrics saved to {report_file}")

    # Feature importances
    importances = model.feature_importances_
    feature_names = X_train_full.columns
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)

    print("\n✅ Feature Importances:")
    print(importance_df)

if __name__ == "__main__":
    # Set optimize=True if you want to run Optuna hyperparameter search
    main(optimize=True)