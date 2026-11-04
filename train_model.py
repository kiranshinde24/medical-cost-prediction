"""Train and evaluate regression models for medical insurance cost prediction.

Usage:
    python train_model.py

Reads insurance.csv, compares four regressors on a held-out test set,
prints R2 / MAE / RMSE, then retrains the best model (Gradient Boosting)
on the full dataset and saves it to model.joblib for the Streamlit app.
"""

import joblib
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

RANDOM_STATE = 42

# Same encoding as the notebook; app.py uses the same mapping.
SEX_MAP = {"female": 0, "male": 1}
SMOKER_MAP = {"no": 0, "yes": 1}
REGION_MAP = {"southwest": 1, "southeast": 2, "northwest": 3, "northeast": 4}


def load_data(path="insurance.csv"):
    data = pd.read_csv(path)
    data["sex"] = data["sex"].map(SEX_MAP)
    data["smoker"] = data["smoker"].map(SMOKER_MAP)
    data["region"] = data["region"].map(REGION_MAP)
    X = data.drop(columns=["charges"])
    y = data["charges"]
    return X, y


def main():
    X, y = load_data()
    print(f"Dataset: {X.shape[0]} rows, {X.shape[1]} features")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    models = {
        "Linear Regression": LinearRegression(),
        "SVR": SVR(),
        "Random Forest": RandomForestRegressor(random_state=RANDOM_STATE),
        "Gradient Boosting": GradientBoostingRegressor(random_state=RANDOM_STATE),
    }

    rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        rows.append(
            {
                "Model": name,
                "R2": metrics.r2_score(y_test, pred),
                "MAE": metrics.mean_absolute_error(y_test, pred),
                "RMSE": metrics.mean_squared_error(y_test, pred) ** 0.5,
            }
        )

    results = pd.DataFrame(rows).set_index("Model").round(3)
    print("\nTest-set results:")
    print(results)

    # Feature importances from the tree-based model
    gb = models["Gradient Boosting"]
    importances = pd.Series(gb.feature_importances_, index=X.columns)
    print("\nGradient Boosting feature importances:")
    print(importances.sort_values(ascending=False).round(3))

    # Retrain the final model on all data for deployment
    final_model = GradientBoostingRegressor(random_state=RANDOM_STATE)
    final_model.fit(X, y)
    joblib.dump(final_model, "model.joblib")
    print("\nSaved final model to model.joblib")


if __name__ == "__main__":
    main()
