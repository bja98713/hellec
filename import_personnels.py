import os
import django
import pandas as pd

# Initialiser Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CEPN.settings")
django.setup()

from expertise.models import PersonnelNavigant, CompagnieAerienne

# Lire le fichier CSV avec le bon séparateur
df = pd.read_csv("fichier.csv", sep=",", engine="python")

# Afficher les premières lignes pour vérifier
print(df.head())

# Vérifier les colonnes présentes
print("Colonnes :", df.columns)

# ➤ Adapter les noms de colonnes si nécessaire
# Exemple si les noms ne sont pas corrects :
# df.columns = ['dn', 'nom', 'prenom', 'compagnie_id', 'date_de_naissance', 'sexe', 'statut_pn']

# Boucle d’import
for _, row in df.iterrows():
    try:
        compagnie = CompagnieAerienne.objects.get(id=row['compagnie_id'])
        PersonnelNavigant.objects.update_or_create(
            dn=row['dn'],
            defaults={
                'nom': row['nom'],
                'prenom': row['prenom'],
                'compagnie': compagnie,
                'date_de_naissance': row.get('date_de_naissance') or None,
                'sexe': row.get('sexe') or None,
                'statut_pn': row.get('statut_pn') or None,
            }
        )
        print(f"{row['dn']} importé avec succès.")
    except Exception as e:
        print(f"Erreur pour {row.get('dn')}: {e}")
