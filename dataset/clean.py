import pandas as pd

# Load the file
df = pd.read_csv("mobile_prices.csv")

# Fix price column — remove commas and convert to integer
# Fix battery column to integer
df['battery'] = df['battery'].astype(int)
df['price'] = df['price'].astype(str).str.replace(',', '').astype(int)

# Extract brand from name
df['brand'] = df['name'].str.extract(r'^(Apple|Samsung|Google|OnePlus)', expand=False).fillna('Other')

# Extract tier from name
def get_tier(name):
    n = name.lower()
    if 'promax' in n or 'pro max' in n: return 'ProMax'
    elif 'pro' in n:                     return 'Pro'
    elif 'plus' in n or 'air' in n:      return 'Plus'
    else:                                return 'Base'

df['tier'] = df['name'].apply(get_tier)

# Encode brand as number
brand_map = {'Apple': 0, 'Samsung': 1, 'Google': 2, 'OnePlus': 3, 'Other': 4}
df['brand_encoded'] = df['brand'].map(brand_map).fillna(4).astype(int)

# Encode tier as number
tier_map = {'Base': 0, 'Plus': 1, 'Pro': 2, 'ProMax': 3}
df['tier_encoded'] = df['tier'].map(tier_map).astype(int)

# Drop columns not needed for model
df_model = df[['back_camera', 'battery', 'display', 'ram', 'brand_encoded', 'tier_encoded', 'price']]

# Save to CSV
df_model.to_csv("mobile_prices_transformed.csv", index=False)

print("✅ Done! File saved as mobile_prices_transformed.csv")
print(df_model.head())