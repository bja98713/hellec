from django.contrib import admin
from .models import PersonnelNavigant, FicheEvenement, Medecin
from .models import CompagnieAerienne, Bordereau

#admin.site.register(PersonnelNavigant)
admin.site.register(FicheEvenement)
admin.site.register(Medecin)


@admin.register(CompagnieAerienne)
class CompagnieAerienneAdmin(admin.ModelAdmin):
    list_display = ("nom","iata")

@admin.register(PersonnelNavigant)
class PersonnelNavigantAdmin(admin.ModelAdmin):
    list_display = ("dn", "nom", "prenom", "compagnie", "get_iata_compagnie")

    def get_iata_compagnie(self, obj):
        return obj.compagnie.iata if obj.compagnie else ""
    get_iata_compagnie.short_description = "Code IATA de la compagnie"

@admin.register(Bordereau)
class BordereauAdmin(admin.ModelAdmin):
    list_display = ('no_bordereau', 'date_bordereau', 'virement')
    list_editable = ('virement',)

class MedecinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'specialite', 'iban')
