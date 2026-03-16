import pandas as pd

df = pd.read_csv("mobile_prices.csv")

# Clean all columns that might have letters like '32M', '128GB', '6.1'.
def clean_numeric(series):
    return series.astype(str).str.replace(r'[^\d.]', '', regex=True).astype(float)

df['back_camera'] = clean_numeric(df['back_camera']).astype(int)
df['battery']     = clean_numeric(df['battery']).astype(int)
df['display']     = clean_numeric(df['display'])
df['ram']         = clean_numeric(df['ram']).astype(int)
df['price']       = df['price'].astype(str).str.replace(',', '').str.replace(r'[^\d]', '', regex=True).astype(int)

# Extract brand — lowercase first to handle VIVO, OPPO, vivo etc.
df['name_lower'] = df['name'].str.strip().str.lower()

def extract_brand(name):
    if name.startswith('apple'):   return 'Apple'
    if name.startswith('samsung'): return 'Samsung'
    if name.startswith('xiaomi'):  return 'Xiaomi'
    if name.startswith('poco'):    return 'Poco'
    if name.startswith('realme'):  return 'Realme'
    if name.startswith('infinix'): return 'Infinix'
    if name.startswith('oppo'):    return 'Oppo'
    if name.startswith('oneplus'): return 'OnePlus'
    if name.startswith('tecno'):   return 'Tecno'
    if name.startswith('vivo'):    return 'Vivo'
    if name.startswith('google'):  return 'Google'
    return 'Other'

df['brand'] = df['name_lower'].apply(extract_brand)

# Extract tier.
def get_tier(name):
    n = name.lower()
    if any(x in n for x in ['promax', 'pro max', 'ultra', 'max']): return 'ProMax'
    elif any(x in n for x in ['pro', 'plus', 'air', 'edge']):      return 'Pro'
    elif any(x in n for x in ['lite', 'mini', 'se', 'neo']):       return 'Plus'
    else:                                                            return 'Base'

df['tier'] = df['name'].apply(get_tier)

# Encode brand.
brand_map = {
    'Apple':   0,
    'Samsung': 1,
    'Xiaomi':  2,
    'Poco':    2,
    'Realme':  3,
    'Infinix': 4,
    'Oppo':    5,
    'OnePlus': 6,
    'Tecno':   7,
    'Vivo':    8,
    'Google':  9,
    'Other':   10
}
df['brand_encoded'] = df['brand'].map(brand_map).fillna(10).astype(int)

# Encode tier.
tier_map = {'Base': 0, 'Plus': 1, 'Pro': 2, 'ProMax': 3}
df['tier_encoded'] = df['tier'].map(tier_map).astype(int)

# Per-brand label — fairer for mixed price ranges across brands.
df['label'] = df.groupby('brand_encoded')['price'] \
                .transform(lambda x: (x > x.median()).astype(int))

# Save
df_model = df[['back_camera', 'battery', 'display', 'ram', 'brand_encoded', 'tier_encoded', 'price', 'label']]
df_model.to_csv("mobile_prices_transformed.csv", index=False)

print("Saved as mobile_prices_transformed.csv ⭐")
print(df_model.head(10))
print("\nBrand distribution: 🛍️")
print(df['brand'].value_counts())
print("\nData types: 🔰")
print(df_model.dtypes)