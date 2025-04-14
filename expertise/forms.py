# expertise/forms.py

from django import forms
from .models import CompagnieAerienne, FicheEvenement

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

# expertise/forms.py

class FicheEvenementForm(forms.ModelForm):
    class Meta:
        model = FicheEvenement
        exclude = ['personnel', 'no_facture', 'total', 'paye_par_patient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si une instance est fournie avec une date_evenement
        date = self.initial.get('date_evenement') or self.data.get('date_evenement')
        if date:
            date_fields = [field for field in self.fields if field.startswith('date_')]
            for field in date_fields:
                self.fields[field].initial = date
