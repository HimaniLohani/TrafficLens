from sklearn.metrics import accuracy_score
import pandas as pd
from preprocess import load_data, add_congestion_column
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():
    df = load_data()
    df = add_congestion_column(df)

    X = df[["hour", "day"]]
    y = df["congestion"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Feature importance
    print("\nFeature Importance:")
    for col, val in zip(X.columns, model.feature_importances_):
        print(f"{col}: {val:.2f}")

    # Save model
    joblib.dump(model, "traffic_model.pkl")

    return model, accuracy


def load_saved_model():
    return joblib.load("traffic_model.pkl")


def predict_congestion(model, hour, day):
    if not (0 <= hour <= 23):
        raise ValueError("Hour must be between 0-23")

    if not (1 <= day <= 7):
        raise ValueError("Day must be between 1-7")

    input_data = pd.DataFrame([[hour, day]], columns=["hour", "day"])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data).max()

    return prediction, probability


if __name__ == "__main__":
    model, acc = train_model()
    print("\nModel Accuracy:", acc)

    result, prob = predict_congestion(model, 9, 1)
    print("Prediction:", result)
    print("Confidence:", prob)