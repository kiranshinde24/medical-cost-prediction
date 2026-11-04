"""Streamlit app: predict individual medical insurance charges."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent
REGION_MAP = {"Southwest": 1, "Southeast": 2, "Northwest": 3, "Northeast": 4}


@st.cache_resource
def load_model():
    # model.joblib is produced by train_model.py; fall back to the old file name
    for name in ("model.joblib", "model_joblib_gr"):
        path = BASE_DIR / name
        if path.exists():
            return joblib.load(path)
    return None


def main():
    st.set_page_config(page_title="Medical Insurance Cost Prediction", page_icon="🩺")
    st.title("🩺 Medical Insurance Cost Prediction")
    st.caption(
        "Gradient Boosting model trained on the Medical Cost Personal dataset "
        "(1,338 records). Estimates only, not real insurance pricing."
    )

    model = load_model()
    if model is None:
        st.error("Model file not found. Run `python train_model.py` first.")
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", 18, 64, 30)
        sex = st.selectbox("Sex", ["Male", "Female"])
        bmi = st.number_input("BMI", min_value=15.0, max_value=55.0, value=27.0, step=0.1)
    with col2:
        children = st.slider("Number of children", 0, 5, 0)
        smoker = st.selectbox("Smoker", ["No", "Yes"])
        region = st.selectbox("Region (US)", list(REGION_MAP))

    if st.button("Predict", type="primary"):
        features = pd.DataFrame(
            [
                {
                    "age": age,
                    "sex": 1 if sex == "Male" else 0,
                    "bmi": bmi,
                    "children": children,
                    "smoker": 1 if smoker == "Yes" else 0,
                    "region": REGION_MAP[region],
                }
            ]
        )
        prediction = model.predict(features)[0]
        st.success(f"Estimated yearly insurance charges: ${prediction:,.2f}")


if __name__ == "__main__":
    main()
