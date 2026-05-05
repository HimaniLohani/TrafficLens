import pandas as pd

def load_data():
    df = pd.read_csv("data/traffic.csv")
    return df


def add_congestion_column(df):
    def get_congestion(count):
        if count < 100:
            return 0   # Low
        elif count < 180:
            return 1   # Medium
        else:
            return 2   # High

    df["congestion"] = df["vehicle_count"].apply(get_congestion)
    return df