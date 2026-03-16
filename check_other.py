import pandas as pd

df = pd.read_csv("mobile_prices.csv")
df['name_lower'] = df['name'].str.strip().str.lower()

known = ['apple','samsung','xiaomi','poco','realme','infinix','oppo','oneplus','tecno','vivo','google']

mask = ~df['name_lower'].apply(lambda x: any(x.startswith(b) for b in known))
result = df[mask]['name'].value_counts()

if result.empty:
    print("Zero unknown brands — all names matched! 🌞")
else:
    print(f"⚠️ {mask.sum()} unmatched rows:")
    print(result.head(20))