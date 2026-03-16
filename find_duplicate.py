import pandas as pd

df = pd.read_csv("mobile_prices.csv")

dupes = df[df.duplicated(subset='name', keep=False)].sort_values('name')

if dupes.empty:
    print("Zero duplicates found! ☕")
else:
    print(f"⚠️ Total duplicate rows: {len(dupes)}")
    print(f"⚠️ Unique names duplicated: {dupes['name'].nunique()}")
    print("\nDuplicate names and count:")
    print(dupes['name'].value_counts())
    print("\nFull duplicate rows:")
    print(dupes.to_string())