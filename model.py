from sklearn.metrics import accuracy_score
import pandas as pd
from preprocess import load_data, add_congestion_column
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model():
    # Load data
    df = load_data()

    # Add congestion labels
    df = add_congestion_column(df)

    # 🔥 NEW FEATURE (important)
    df["is_peak"] = df["hour"].apply(
        lambda x: 1 if x in [8, 9, 10, 17, 18, 19] else 0
    )

    # Features & target
    X = df[["hour", "day", "is_peak"]]
    y = df["congestion"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 🔥 IMPROVED MODEL
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",   # 🔥 fix imbalance
        random_state=42
    )

    model.fit(X_train, y_train)

    # Accuracy check
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Model Accuracy:", accuracy)

    # 🔥 DEBUG (important)
    print("\nClass Distribution:")
    print(y.value_counts())

    return model, accuracy


def predict_congestion(model, hour, day):
    is_peak = 1 if hour in [8, 9, 10, 17, 18, 19] else 0

    input_data = pd.DataFrame(
        [[hour, day, is_peak]],
        columns=["hour", "day", "is_peak"]
    )

    prediction = model.predict(input_data)
    return prediction[0]


# 🔥 TEST RUN
if __name__ == "__main__":
    model, acc = train_model()

    print("\nSample Predictions:")
    for h in [6, 9, 14, 18, 22]:
        print(f"Hour {h} ->", predict_congestion(model, h, 1))