import pandas as pd
from datetime import datetime
import numpy as np
import nltk
from nltk.corpus import names

print("🚀 Sāk harmonizāciju...")

# Failu ceļi
df1 = pd.read_csv('../datnes/DatubazeMed.csv')
df2 = pd.read_csv('../datnes/healthcare_dataset.csv', delimiter=';')
print("✅ Faili ielādēti:", df1.shape, df2.shape)

# Sinonīmu vārdnīca
synonyms = {
    'Patient_Name': ['Patient name', 'Name'],
    'Blood_Group': ['Blood group', 'Blood Type'],
    'Medical_Condition': ['Chronic conditions', 'Medical Condition'],
    'Age': ['Age'],
    'Medication': ['Medication'],
    'Gender': ['Gender'],
    'Date_of_Birth': ['Date of birth']
}

# Harmonizētie datu ietvari
df1_h = pd.DataFrame()
df2_h = pd.DataFrame()

for unified, variants in synonyms.items():
    df1_col = next((v for v in variants if v in df1.columns), None)
    df2_col = next((v for v in variants if v in df2.columns), None)
    
    df1_h[unified] = df1[df1_col] if df1_col else pd.NA
    df2_h[unified] = df2[df2_col] if df2_col else pd.NA

# Aprēķina vecumu no dzimšanas datuma
if 'Date_of_Birth' in df1_h.columns:
    excel_origin = datetime(1899, 12, 30)
    df1_h['Date_of_Birth'] = pd.to_timedelta(df1_h['Date_of_Birth'], unit='D') + excel_origin
    df1_h['Age'] = datetime.today().year - df1_h['Date_of_Birth'].dt.year

# 🔍 Dzimuma noteikšana pēc vārda, izmantojot nltk
print("🧠 Noteikts dzimums pēc vārda (nltk)...")
nltk.download('names', quiet=True)
male_names = set(names.words('male.txt'))
female_names = set(names.words('female.txt'))

def infer_gender_nltk(name):
    if pd.isna(name):
        return 'Unknown'
    first = str(name).split()[0].capitalize()
    if first in male_names:
        return 'Male'
    elif first in female_names:
        return 'Female'
    else:
        return 'Unknown'

df1_h.loc[df1_h['Gender'].isna(), 'Gender'] = df1_h['Patient_Name'].apply(infer_gender_nltk)

# Pievieno trūkstošās kolonnas
for col in df1_h.columns:
    if col not in df2_h.columns:
        df2_h[col] = pd.NA
for col in df2_h.columns:
    if col not in df1_h.columns:
        df1_h[col] = pd.NA

# Sakārto kolonnu secību
df1_h = df1_h[df2_h.columns]

# Apvieno
combined = pd.concat([df1_h, df2_h], ignore_index=True)
print("Teste gender funkciju:")
print("Anna →", infer_gender_nltk("Anna"))
print("Mark →", infer_gender_nltk("Mark"))
print("Līga →", infer_gender_nltk("Līga"))  # netiks atpazīts – nav angļu vārdnīcā

# Saglabā rezultātu
combined.to_csv('../output/final_harmonized.csv', index=False)
print("✅ Harmonizācija veiksmīga! Rezultāts: output/final_harmonized.csv")
print("🧾 Forma:", combined.shape)
