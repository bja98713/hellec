from django.apps import AppConfig

class ExpertiseConfig(AppConfig):
    name = 'expertise'

# expertise/forms.py

from django import forms
from .models import CompagnieAerienne

class BordereauSelectionForm(forms.Form):
    MOIS_CHOICES = [(m, f"{m:02d}") for m in range(1, 13)]  # 1->12
    ANNEE_CHOICES = [(y, str(y)) for y in range(2020, 2031)] # exemple 2020->2030

    mois = forms.ChoiceField(choices=MOIS_CHOICES, label="Mois")
    annee = forms.ChoiceField(choices=ANNEE_CHOICES, label="Année")

    # Soit on veut choisir la compagnie par son code iata :
    # iata = forms.ChoiceField(...)

    # OU on veut choisir la compagnie via un QuerySet (ForeignKey)
    compagnie = forms.ModelChoiceField(
        queryset=CompagnieAerienne.objects.all(),
        label="Compagnie aérienne",
        required=True,
    )
