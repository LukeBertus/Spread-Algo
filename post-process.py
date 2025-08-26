# Add index column
import pandas as pd
from scipy.stats import pearsonr

df = pd.read_csv("mid_spread.csv")

## Add index column ##
#df.insert(0, "Index", range(1, len(df) + 1))

## Add average column ##
#price_columns = [col for col in df.columns if col != "Index"]
#df["Average"] = df[price_columns].mean(axis=1)

## Delete Columns ##
#df = df.drop(columns=["Price_2", "Price_3", "Price_8"], errors="ignore")

## Convert to change in price ##
#price_columns = [col for col in df.columns if col != "Index"]
#for col in price_columns:
#    df[col] = df[col].diff()

## Remove Outliers ##
#price_columns = [col for col in df.columns if col != "Index"]
#for col in price_columns:
#    mask = (df[col] > 10) | (df[col] < -10)
#    df[col] = df[col].where(~mask, df[col].shift())
df['past_5_mid_change'] = df['mid'] - df['mid'].shift(5)
df['next_5_mid_change'] = df['mid'].shift(-5) - df['mid']

df_clean = df.dropna(subset=['past_5_mid_change', 'next_5_mid_change'])

corr, p_value = pearsonr(df_clean['past_5_mid_change'], df_clean['next_5_mid_change'])
print(f"Correlation: {corr:.4f}, p-value: {p_value:.4g}")
#df.to_csv("trade_prices.csv", index=False)
