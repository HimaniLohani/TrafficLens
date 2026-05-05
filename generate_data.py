import pandas as pd
import random

data = []

for _ in range(500):   # 🔥 500 rows
    hour = random.randint(0, 23)
    day = random.randint(0, 6)

    # 🔥 realistic traffic logic
    if hour in [8, 9, 10, 17, 18, 19]:   # peak hours
        vehicle_count = random.randint(180, 300)
    elif hour in [11, 12, 13, 14, 15]:   # medium
        vehicle_count = random.randint(100, 180)
    else:  # night / low
        vehicle_count = random.randint(30, 100)

    data.append([hour, day, vehicle_count])

df = pd.DataFrame(data, columns=["hour", "day", "vehicle_count"])

df.to_csv("data/traffic.csv", index=False)

print(" Dataset generated successfully (500 rows)")