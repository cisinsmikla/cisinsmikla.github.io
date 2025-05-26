import pandas as pd
import hashlib
import os
import glob

def hash_value(val):
    if pd.isna(val):
        return ''
    return hashlib.sha256(str(val).encode()).hexdigest()[:10]

SENSITIVE_KEYWORDS = [
    'name', 'id', 'address', 'email', 'contact', 'birth', 'employer',
    'policy', 'holder', 'city', 'country', 'surname', 'phone', 'patient'
]

input_folder = "datnes/"
output_folder = "output/"
os.makedirs(output_folder, exist_ok=True)
csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    # Automatizēta delimitera noteikšana
    with open(file, encoding="utf-8") as f:
        header = f.readline()
        delimiter = ';' if header.count(';') > header.count(',') else ','

    df = pd.read_csv(file, delimiter=delimiter, encoding="utf-8")

    # Atrodi visas sensitīvās kolonnas
    sensitive_cols = [col for col in df.columns
                      if any(key in col.lower() for key in SENSITIVE_KEYWORDS)]

    print(f"[INFO] {os.path.basename(file)} – sensitīvās kolonnas: {sensitive_cols}")

    # Aizvieto vērtības ar kodiem (hash)
    for col in sensitive_cols:
        df[col] = df[col].apply(hash_value)

    # Saglabā anonimizēto failu
    output_path = os.path.join(output_folder, "anonymized_" + os.path.basename(file))
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[OK] Saglabāts: {output_path}")

print("Automātiskā anonimizācija pabeigta!")
