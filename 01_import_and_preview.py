import pandas as pd
import matplotlib.pyplot as plt

path_med = '../datnes/DatubazeMed.csv'
path_health = '../datnes/healthcare_dataset.csv'

try:
    df1 = pd.read_csv(path_med)
    print("DatubazeMed.csv ielādēts:", df1.shape)
except Exception as e:
    print("Kļūda ielādējot DatubazeMed:", e)

try:
    df2 = pd.read_csv(path_health, delimiter=';')
    print("healthcare_dataset.csv ielādēts:", df2.shape)
except Exception as e:
    print("Kļūda ielādējot healthcare_dataset:", e)

print("\nKolonnas DatubazeMed:")
print(df1.columns.tolist())
print("\nPirmās 3 rindas DatubazeMed:")
print(df1.head(3), '\n')

print("Kolonnas healthcare_dataset:")
print(df2.columns.tolist())
print("\nPirmās 3 rindas healthcare_dataset:")
print(df2.head(3), '\n')

def save_table(df, title, filename):
    fig, ax = plt.subplots(figsize=(min(25, 2 + 2 * len(df.columns)), 1 + 0.6 * len(df)))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left', colLoc='left')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1.5, 1.5)  
    plt.title(title, fontsize=10)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

save_table(df1.head(3), "DatubazeMed – pirmās 3 rindas", "../output/preview_med.png")
save_table(df2.head(3), "Healthcare Dataset – pirmās 3 rindas", "../output/preview_health.png")
print("Saglabāti attēli: preview_med.png un preview_health.png")
