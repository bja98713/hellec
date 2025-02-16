from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class CompagnieAerienne(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    iata = models.CharField(
        max_length=3,
        blank=True,  # si tu veux autoriser vide
        null=True,   # si tu veux autoriser null
        verbose_name="Code IATA"
    )

    def __str__(self):
        # Afficher le code IATA dans la liste des compagnies
        return f"{self.nom} ({self.iata})" if self.iata else self.nom


# Modèle pour stocker les médecins
class Medecin(models.Model):
    nom = models.CharField("Nom", max_length=100)
    prenom = models.CharField("Prénom", max_length=100)

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"

    def __str__(self):
        return f"Dr. {self.prenom} {self.nom}"

# Modèle pour le personnel navigant
class PersonnelNavigant(models.Model):
    dn_validator = RegexValidator(
        regex=r'^\d{7}$',
        message="Christian, le numéro de sécurité sociale doit comporter 7 chiffres."
    )
    dn = models.CharField(
        max_length=7,
        unique=True,
        validators=[dn_validator],
        verbose_name="Numéro DN"
    )
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    date_de_naissance = models.DateField(verbose_name="Date de naissance")
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")

    # Ancien champ, à supprimer plus tard :
    nom_ca = models.CharField(max_length=100, verbose_name="Nom de la compagnie aérienne")

    # Nouveau champ ForeignKey
    compagnie = models.ForeignKey(
        CompagnieAerienne,
        on_delete=models.CASCADE,  # ou SET_NULL si tu veux le garder en base
        null=True,  # Permet de rendre ce champ temporairement optionnel
        blank=True,  # pour ne pas bloquer les anciennes données
        verbose_name="Compagnie Aérienne"
    )

    STATUT_PN_CHOICES = (
        ('PNT', 'PNT (Pilote)'),
        ('PNC', 'PNC (Personnel Navigant Commercial)'),
    )
    statut_pn = models.CharField(
        max_length=3,
        choices=STATUT_PN_CHOICES,
        verbose_name="Statut PN",
        default='PNT',  # ex. valeur par défaut
        help_text="(PNT pour pilote, PNC pour hôtesse/steward)"
    )

    # Exemple de liste de choix iata
    IATA_CHOICES = (
        ('AFR', 'Air France'),
        ('ATN', 'Air Tahiti Nui'),
        ('XZY', 'Compagnie fictive'),
    )

    iata = models.CharField(
        max_length=3,
        choices=IATA_CHOICES,
        verbose_name="IATA",
        default='AFR',  # éventuel default
        help_text="Code IATA de la compagnie (ex : AFR, ATN...)."
    )

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.iata}"

# Modèle pour la fiche d'événement
class FicheEvenement(models.Model):
    date_evenement = models.DateField(verbose_name="Date de l'événement")
    personnel = models.ForeignKey(
        PersonnelNavigant,
        on_delete=models.CASCADE,
        to_field='dn',
        verbose_name="Personnel (DN)",
        related_name='evenements'
    )
    
    # Variables relatives à CS CEMPn
    cs_cempn = models.BooleanField("Consultation CEMPN", default=False)
    date_cempn = models.DateField("Date de la consultation CEMPN", null=True, blank=True)
    honoraire_cempn = models.IntegerField("Honoraire de la CS CEMPN", default=0)
    medecin_cempn = models.ForeignKey(
        Medecin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements_cempn',
        verbose_name="Médecin CEMPN"
    )
    
    # Variables relatives à CS OPH
    cs_oph = models.BooleanField("Consultation OPH", default=False)
    date_cs_oph = models.DateField("Date de la consultation OPH", null=True, blank=True)
    honoraire_cs_oph = models.IntegerField("Honoraire de la CS OPH", default=0)
    medecin_oph = models.ForeignKey(
        Medecin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements_oph',
        verbose_name="Médecin OPH"
    )
    
    # Variables relatives à CS ORL
    cs_orl = models.BooleanField("Consultation ORL", default=False)
    date_cs_orl = models.DateField("Date de la consultation ORL", null=True, blank=True)
    honoraire_cs_orl = models.IntegerField("Honoraire de la CS ORL", default=0)
    medecin_orl = models.ForeignKey(
        Medecin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements_orl',
        verbose_name="Médecin ORL"
    )
    
    # Variables relatives à CS LABO
    cs_labo = models.BooleanField("Laboratoire AM Javouhey", default=False)
    date_cs_labo = models.DateField("Date du prélévement", null=True, blank=True)
    honoraire_cs_labo = models.IntegerField("Honoraire Laboratoire AMJ", default=0)
    
    # Variables relatives à CS LBX
    cs_lbx = models.BooleanField("Prélévement Urinaire (Labstix)", default=False)
    date_cs_lbx = models.DateField("Date du prélévement urinaire", null=True, blank=True)
    honoraire_cs_lbx = models.IntegerField("Honoraire prélévement urinaire", default=0)
    
    # Variables relatives à CS RADIO
    cs_radio = models.BooleanField("Examen d'imagerie", default=False)
    date_cs_radio = models.DateField("Date de l'examen d'imagerie", null=True, blank=True)
    honoraire_cs_radio = models.IntegerField("Prix des examens d'imagerie", default=0)
    medecin_radio = models.ForeignKey(
        Medecin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements_radio',
        verbose_name="Médecin radiologue"
    )
    
    # Informations complémentaires
    recherche_toxique = models.BooleanField("Recherche toxique", default=False)
    frais_dossier = models.IntegerField("Frais de dossier", default=0)
    total = models.IntegerField("Total", default=0, help_text="Somme des honoraires et frais de dossier")
    
    # Informations sur le paiement
    paiement = models.BooleanField("Paiement", default=False)
    date_paiement = models.DateField("Date de paiement", null=True, blank=True)
    MODALITE_CHOICES = (
        ('liquide', 'Liquide'),
        ('virement', 'Virement'),
        ('cb', 'Carte Bancaire'),
    )
    modalite_paiement = models.CharField("Modalité de paiement", max_length=10, choices=MODALITE_CHOICES, null=True, blank=True)
    
    # Nouveaux champs pour la gestion de la quote-part et le numéro de facture
    quote_part_patient = models.BooleanField("Quote-part patient", default=False)
    paye_par_patient = models.IntegerField("Payé par le patient", default=0)
    no_facture = models.CharField("Numéro de facture", max_length=50, blank=True, null=True, editable=False)
    
    def save(self, *args, **kwargs):
        # Calcul du total (somme des honoraires et des frais)
        self.total = (
            (self.honoraire_cempn or 0) +
            (self.honoraire_cs_oph or 0) +
            (self.honoraire_cs_orl or 0) +
            (self.honoraire_cs_labo or 0) +
            (self.honoraire_cs_lbx or 0) +
            (self.honoraire_cs_radio or 0) +
            (self.frais_dossier or 0)
        )
        # Mise à jour de la quote-part
        if self.quote_part_patient:
            self.paye_par_patient = self.total
        else:
            self.paye_par_patient = 0

        # Génération automatique du numéro de facture s'il n'est pas défini
        if not self.no_facture:
            event_date = self.date_evenement or timezone.now().date()
            year = event_date.year
            month = event_date.month
            count = FicheEvenement.objects.filter(date_evenement__year=year).count() + 1
            self.no_facture = f"{year}E{month:02d}.{count}/01"

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Événement du {self.date_evenement} pour {self.personnel}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('evenement_detail', kwargs={'id': self.id})
