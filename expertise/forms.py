# expertise/forms.py

from django import forms
from .models import CompagnieAerienne

class BordereauSelectionForm(forms.Form):
    # Exemple de champs mois/année
    MOIS_CHOICES = [(m, f"{m:02d}") for m in range(1, 13)]
    ANNEE_CHOICES = [(y, str(y)) for y in range(2020, 2031)]
    
    mois = forms.ChoiceField(choices=MOIS_CHOICES, label="Mois")
    annee = forms.ChoiceField(choices=ANNEE_CHOICES, label="Année")

    # Sélection de la compagnie via ModelChoiceField
    compagnie = forms.ModelChoiceField(
        queryset=CompagnieAerienne.objects.all(),
        label="Compagnie aérienne",
        required=True,
    )
