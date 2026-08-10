"""
Loan Default Prediction API
"""

from typing import Any, Dict

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.config import MODEL_PATH
from src.features import execute_feature_engineering


class LoanDefaultPredictor:
    """Production predictor wrapper for online or batch loan default scoring."""

    def __init__(self, model_path=MODEL_PATH):
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. Train model first."
            )

        self.model = joblib.load(model_path)

    def predict_single(
        self,
        application_dict: Dict[str, Any]
    ) -> Dict[str, Any]:

        df_single = pd.DataFrame([application_dict])

        df_fe = execute_feature_engineering(df_single)

        # Align features with expected model input
        if hasattr(self.model, "feature_names_in_"):

            expected_cols = self.model.feature_names_in_

            for col in expected_cols:
                if col not in df_fe.columns:
                    df_fe[col] = 0

            df_input = df_fe[expected_cols]

        else:
            df_input = df_fe

        prob = float(
            self.model.predict_proba(df_input)[0, 1]
        )

        decision = (
            "REJECT / HIGH RISK"
            if prob >= 0.50
            else "APPROVE / LOW RISK"
        )

        return {
            "default_probability": round(prob, 4),
            "underwriting_recommendation": decision,
            "risk_score": int((1 - prob) * 850)
        }


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Loan Default Prediction API",
    description="ML API for predicting loan default risk",
    version="1.0.0"
)


# Load model when application starts
try:
    predictor = LoanDefaultPredictor()
except FileNotFoundError as e:
    predictor = None
    model_error = str(e)


@app.get("/")
def home():
    return {
        "message": "Loan Default Prediction API is running"
    }


@app.get("/health")
def health():
    if predictor is None:
        return {
            "status": "unhealthy",
            "model": "not loaded"
        }

    return {
        "status": "healthy",
        "model": "loaded"
    }


@app.post("/predict")
def predict(application: Dict[str, Any]):

    if predictor is None:
        raise HTTPException(
            status_code=500,
            detail=model_error
        )

    try:
        result = predictor.predict_single(application)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )