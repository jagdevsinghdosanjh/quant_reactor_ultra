#Quant_Reactor_Ultra (VS Code Project using Python and streamlit)
#core/engine/ml_regime.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Ret1"] = df["Returns"].shift(1)
    df["Ret2"] = df["Returns"].shift(2)
    df["Vol10"] = df["Returns"].rolling(10).std()
    df["Vol20"] = df["Returns"].rolling(20).std()
    df["Target"] = (df["Returns"].shift(-1) > 0).astype(int)
    df = df.dropna()
    return df

def train_regime_model(df: pd.DataFrame):
    df_feat = prepare_features(df)
    X = df_feat[["Ret1", "Ret2", "Vol10", "Vol20"]]
    y = df_feat["Target"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42, shuffle=False
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    return model, scaler, score, df_feat.index

def apply_regime_model(df: pd.DataFrame, model, scaler):
    df_feat = prepare_features(df)
    X = df_feat[["Ret1", "Ret2", "Vol10", "Vol20"]]
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[:, 1]
    preds = (proba > 0.5).astype(int)

    out = df.copy()
    out.loc[df_feat.index, "ML_Regime_Prob"] = proba
    out.loc[df_feat.index, "ML_Regime_Up"] = preds.astype(bool)
    return out
