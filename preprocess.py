import pandas as pd

def load_data():
    try:
        df = pd.read_csv("data/traffic.csv")
    except FileNotFoundError:
        raise Exception("Dataset not found. Check file path.")

    # Basic validation
    required_cols = ["hour", "day", "vehicle_count"]
    for col in required_cols:
        if col not in df.columns:
            raise Exception(f"Missing column: {col}")

    # Handle missing values
    df = df.dropna()

    return df


def add_congestion_column(df):
    # Dynamic thresholds (better than fixed)
    low_th = df["vehicle_count"].quantile(0.33)
    high_th = df["vehicle_count"].quantile(0.66)

    def get_congestion(count):
        if count < low_th:
            return 0   # Low
        elif count < high_th:
            return 1   # Medium
        else:
            return 2   # High

    df["congestion"] = df["vehicle_count"].apply(get_congestion)

    return df