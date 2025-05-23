import pandas as pd

df = pd.read_csv('../output/final_harmonized.csv')

def fix_name_format(value):
    if pd.isna(value):
        return value
    return ' '.join(word.capitalize() for word in str(value).split())

df['Patient_Name'] = df['Patient_Name'].apply(fix_name_format)

df.to_csv('../output/final_names_fixed.csv', index=False)

print("✅ Gatavs: output/final_names_fixed.csv")
