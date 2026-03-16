import pandas as pd

df = pd.read_csv("mobile_prices.csv")

# ── Clean all columns that might have letters like '32M', '128GB', '6.1"' ──
def clean_numeric(series):
    return series.astype(str).str.replace(r'[^\d.]', '', regex=True).astype(float)

df['back_camera'] = clean_numeric(df['back_camera']).astype(int)
df['battery']     = clean_numeric(df['battery']).astype(int)
df['display']     = clean_numeric(df['display'])
df['ram']         = clean_numeric(df['ram']).astype(int)
df['price']       = df['price'].astype(str).str.replace(',', '').str.replace(r'[^\d]', '', regex=True).astype(int)

# Extract brand
df['brand'] = df['name'].str.extract(r'^(Apple|Samsung|Google|OnePlus)', expand=False).fillna('Other')

# Extract tier
def get_tier(name):
    n = name.lower()
    if 'promax' in n or 'pro max' in n: return 'ProMax'
    elif 'pro' in n:                     return 'Pro'
    elif 'plus' in n or 'air' in n:      return 'Plus'
    else:                                return 'Base'

df['tier'] = df['name'].apply(get_tier)

# Encode
brand_map = {'Apple': 0, 'Samsung': 1, 'Google': 2, 'OnePlus': 3, 'Other': 4}
df['brand_encoded'] = df['brand'].map(brand_map).fillna(4).astype(int)

tier_map = {'Base': 0, 'Plus': 1, 'Pro': 2, 'ProMax': 3}
df['tier_encoded'] = df['tier'].map(tier_map).astype(int)

# Save
df_model = df[['back_camera', 'battery', 'display', 'ram', 'brand_encoded', 'tier_encoded', 'price']]
df_model.to_csv("mobile_prices_transformed.csv", index=False)

print("✅ Done! Saved as mobile_prices_transformed.csv")
print(df_model.head())
print("\nData types:")
print(df_model.dtypes)