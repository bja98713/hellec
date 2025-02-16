# expertise/views.py

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import PersonnelNavigant, FicheEvenement
from django.db.models import Q
from .forms import BordereauSelectionForm  # <-- Voilà
from num2words import num2words  # ✅ Importer la fonction


import io
import base64
import barcode
from barcode.writer import ImageWriter



# ----- VUES POUR LES PERSONNELS -----

class PersonnelListView(ListView):
    model = PersonnelNavigant
    template_name = 'expertise/personnel_list.html'
    context_object_name = 'personnels'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(prenom__icontains=query) |
                Q(dn__icontains=query)
            )
        return queryset


class PersonnelDetailView(DetailView):
    """
    Affiche le détail d'un personnel navigant, identifié par son DN.
    Ajoute également dans le contexte la liste des événements associés.
    """
    model = PersonnelNavigant
    template_name = 'expertise/personnel_detail.html'
    context_object_name = 'personnel'
    slug_field = 'dn'
    slug_url_kwarg = 'dn'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Grâce au related_name 'evenements' défini dans le modèle FicheEvenement,
        # on peut accéder aux événements via self.object.evenements.all()
        context['evenements'] = self.object.evenements.all()
        return context


class PersonnelCreateView(CreateView):
    """
    Permet d'ajouter un nouveau personnel navigant.
    """
    model = PersonnelNavigant
    fields = ['dn', 'nom', 'prenom', 'date_de_naissance', 'sexe', 'statut_pn', 'compagnie']
    template_name = 'expertise/personnel_form.html'
    success_url = reverse_lazy('personnel_list')


class PersonnelUpdateView(UpdateView):
    model = PersonnelNavigant
    fields = ['dn', 'nom', 'prenom', 'date_de_naissance', 'sexe', 'statut_pn', 'compagnie']
    template_name = 'expertise/personnel_form.html'
    success_url = reverse_lazy('personnel_list')
    slug_field = 'dn'
    slug_url_kwarg = 'dn'



class PersonnelDeleteView(DeleteView):
    model = PersonnelNavigant
    template_name = 'expertise/personnel_confirm_delete.html'
    success_url = reverse_lazy('personnel_list')
    slug_field = 'dn'
    slug_url_kwarg = 'dn'



# ----- VUES POUR LES EVENEMENTS -----

# expertise/views.py

class FicheEvenementCreateView(CreateView):
    model = FicheEvenement
    fields = [
        'date_evenement',
        'cs_cempn', 'date_cempn', 'honoraire_cempn', 'medecin_cempn',
        'cs_oph', 'date_cs_oph', 'honoraire_cs_oph', 'medecin_oph',
        'cs_orl', 'date_cs_orl', 'honoraire_cs_orl', 'medecin_orl',
        'cs_labo', 'date_cs_labo', 'honoraire_cs_labo',
        'cs_lbx', 'date_cs_lbx', 'honoraire_cs_lbx',
        'cs_radio', 'date_cs_radio', 'honoraire_cs_radio', 'medecin_radio',
        'recherche_toxique', 'medecin_cempn', 'medecin_oph', 'medecin_orl', 'medecin_radio',
        'frais_dossier',
        'quote_part_patient',
        'paiement', 'date_paiement', 'modalite_paiement',
    ]
    template_name = 'expertise/evenement_form.html'
    # La suite de la vue reste identique...


    def form_valid(self, form):
        dn = self.kwargs['dn']
        personnel = get_object_or_404(PersonnelNavigant, dn=dn)
        form.instance.personnel = personnel
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dn'] = self.kwargs['dn']
        personnel = get_object_or_404(PersonnelNavigant, dn=self.kwargs['dn'])
        context['evenements'] = personnel.evenements.all()
        return context

    def get_success_url(self):
        return reverse_lazy('personnel_detail', kwargs={'dn': self.object.personnel.dn})


class FicheEvenementUpdateView(UpdateView):
    model = FicheEvenement
    fields = [
        'date_evenement',
        'cs_cempn', 'date_cempn', 'honoraire_cempn',
        'cs_oph', 'date_cs_oph', 'honoraire_cs_oph',
        'cs_orl', 'date_cs_orl', 'honoraire_cs_orl',
        'cs_labo', 'date_cs_labo', 'honoraire_cs_labo',
        'cs_lbx', 'date_cs_lbx', 'honoraire_cs_lbx',
        'cs_radio', 'date_cs_radio', 'honoraire_cs_radio',
        'recherche_toxique', 'medecin_cempn', 'medecin_oph', 'medecin_orl', 'medecin_radio',
        'frais_dossier',
        'quote_part_patient',  # Positionné ici aussi
        'paiement', 'date_paiement', 'modalite_paiement',
    ]
    template_name = 'expertise/evenement_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dn'] = self.object.personnel.dn
        return context

    def get_success_url(self):
        return reverse_lazy('personnel_detail', kwargs={'dn': self.object.personnel.dn})


class FicheEvenementDeleteView(DeleteView):
    """
    Permet de supprimer un événement.
    """
    model = FicheEvenement
    template_name = 'expertise/evenement_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('personnel_detail', kwargs={'dn': self.object.personnel.dn})

# expertise/views.py

import io
import base64
import barcode
from barcode.writer import ImageWriter
from django.views.generic import DetailView
from .models import FicheEvenement

import io
import base64
import barcode
from barcode.writer import ImageWriter
from django.views.generic import DetailView
from .models import FicheEvenement

import io
import base64
import barcode
from barcode.writer import ImageWriter
from django.views.generic import DetailView
from .models import FicheEvenement

class FactureView(DetailView):
    model = FicheEvenement
    template_name = 'expertise/facture.html'
    context_object_name = 'evenement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_number = self.object.no_facture
        if invoice_number:
            Code128 = barcode.get_barcode_class('code128')
            barcode_instance = Code128(invoice_number, writer=ImageWriter())
            buffer = io.BytesIO()
            barcode_instance.write(buffer)
            barcode_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            context['barcode'] = barcode_base64
        return context

    # expertise/views.py

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import FicheEvenement, CompagnieAerienne
from datetime import date

from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import CompagnieAerienne, FicheEvenement
from .utils import nombre_en_lettres


def bordereau_view(request, annee, mois, iata):
    # 📌 Vérifier que la compagnie existe
    compagnie = get_object_or_404(CompagnieAerienne, iata=iata)

    # 📌 Filtrer les événements liés à la compagnie et la période
    evenements = FicheEvenement.objects.filter(
        date_evenement__year=annee,
        date_evenement__month=mois,
        personnel__compagnie=compagnie
    )

    # ✅ Debugging : Affiche les événements trouvés
    print(f"DEBUG: Nombre d'événements trouvés : {evenements.count()}")
    for e in evenements:
        print(f"Facture: {e.no_facture}, DN: {e.personnel.dn}, Nom: {e.personnel.nom}, Prénom: {e.personnel.prenom}, Total: {e.total}XPF")

    # 📌 Ajout de la date du bordereau (date actuelle)
    date_bordereau = datetime.today().strftime('%d/%m/%Y')

    # 📌 Génération du numéro de bordereau
    no_bordereau = f"EB{datetime.today().day:02d}{mois:02d}{str(annee)[-2:]}{iata}"

    # 📌 Calcul du nombre de factures et du total général
    nombre_factures = evenements.count()
    total_global = sum(e.total for e in evenements)
    total_global_lettres = nombre_en_lettres(total_global)  # 🔥 Convertir en lettres

    # ✅ Debugging : Affiche les informations essentielles
    print(f"DEBUG: Date Bordereau = {date_bordereau}, Numéro Bordereau = {no_bordereau}")
    print(f"DEBUG: IATA reçu = {iata}, Nombre de factures = {nombre_factures}, Total général = {total_global}")

    return render(request, "expertise/bordereau.html", {
        "evenements": evenements,  # ✅ Vérifie que cette variable est bien transmise
        "mois": mois,
        "annee": annee,
        "iata": iata,
        "compagnie": compagnie,
        "date_bordereau": date_bordereau,  # ✅ Ajout de la date
        "no_bordereau": no_bordereau,  # ✅ Ajout du numéro
        "nombre_factures": nombre_factures,
        "total_global": total_global,
        "total_global_lettres": total_global_lettres,  # 🆕 Ajouter cette variable au template
    })


from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BordereauSelectionForm

def bordereau_selection_view(request):
    if request.method == 'POST':
        form = BordereauSelectionForm(request.POST)
        if form.is_valid():
            mois = form.cleaned_data['mois']
            annee = form.cleaned_data['annee']
            compagnie = form.cleaned_data['compagnie']  # c'est un objet CompagnieAerienne
            # => on récupère le code iata :
            iata = compagnie.iata  # si c'est ça que tu utilises dans l'URL

            # Rediriger vers l'URL de bordereau :
            # par ex: /bordereau/2023/10/AFR/
            return redirect(
                'bordereau_detail',
                annee=annee,
                mois=mois,
                iata=iata
            )
    else:
        form = BordereauSelectionForm()

    return render(request, 'expertise/selection_bordereau.html', {'form': form})

from django.http import HttpResponse
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import CompagnieAerienne, FicheEvenement

from django.http import HttpResponse
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import CompagnieAerienne, FicheEvenement
from num2words import num2words  # Assure-toi que cette importation est bien là


def download_bordereau(request, mois, annee, iata):
    # 📌 Vérifier que la compagnie existe
    compagnie = get_object_or_404(CompagnieAerienne, iata=iata)

    # 📌 Filtrer les événements pour ce mois et cette année
    evenements = FicheEvenement.objects.filter(
        date_evenement__year=annee,
        date_evenement__month=mois,
        personnel__compagnie=compagnie
    )

    # 📌 Générer le numéro du bordereau
    date_creation = datetime.today()
    no_bordereau = f"EB{date_creation.day:02d}{mois:02d}{str(annee)[-2:]}{iata}"

    total_general = sum(evenement.total for evenement in evenements)
    total_global_lettres = num2words(total_general, lang='fr').capitalize()

    # 📌 Création du document Word
    doc = Document()

    # 📌 Ajouter un pied de page avec le RIB sur chaque page
    section = doc.sections[0]
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.text = "RIB BDT : 12239.00001.62288701000.14"
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    paragraph.runs[0].font.size = Pt(9)  # Réduction de la taille du texte

    # 📌 Ajouter l'en-tête
    for text, level in [
        ('Centre d’Expertise Médicale du Personnel Naviguant', 1),
        ('BP 295 - 98713 Papeete', 2),
        ('Tel : 87.71.50.90 | Mel : cmpnpf@gmail.com', 2),
        ('Bordereau de dépôts de factures', 1),
    ]:
        heading = doc.add_heading(text, level=level)
        heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # 📌 Informations du bordereau
    doc.add_paragraph("\n")
    doc.add_paragraph(f"📅 Date de création : {date_creation.strftime('%d/%m/%Y')}")
    doc.add_paragraph(f"📄 Numéro du bordereau : {no_bordereau}")
    doc.add_paragraph(f"✈️ Compagnie aérienne : {compagnie.nom} ({compagnie.iata})")
    doc.add_paragraph("\n")

    # 📌 Création du tableau principal des factures
    table = doc.add_table(rows=1, cols=6)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER  # Centrage du tableau

    # 📌 Ajouter l'entête du tableau
    hdr_cells = table.rows[0].cells
    headers = ["Numéro de facture", "DN", "Nom", "Prénom", "Total (XPF)", "Paiement"]

    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        hdr_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Centrer le texte
        hdr_cells[i].paragraphs[0].runs[0].bold = True  # Mettre en gras
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)  # Réduire la taille de la police

    # 📌 Ajouter les données
    total_general = 0
    for evenement in evenements:
        row_cells = table.add_row().cells
        row_data = [
            evenement.no_facture or "N/A",
            evenement.personnel.dn,
            evenement.personnel.nom,
            evenement.personnel.prenom,
            f"{evenement.total} XPF",
            "✅ Payé" if evenement.paiement else "❌ Non payé"
        ]

        for i, data in enumerate(row_data):
            row_cells[i].text = data
            row_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Centrer le texte
            row_cells[i].paragraphs[0].runs[0].font.size = Pt(9)  # Réduire la taille de la police

        total_general += evenement.total

    # 📌 Ajouter le résumé
    doc.add_paragraph("\n")
    summary = doc.add_paragraph()
    summary_run = summary.add_run(f"Nombre de factures : {evenements.count()}  |   Total général : {total_general} XPF (soit {total_global_lettres} francs)")
    summary_run.bold = True


    # 📌 Ajouter les factures détaillées
    for evenement in evenements:
        doc.add_page_break()
        
        # 📌 Répéter l’en-tête
        for text, level in [
            ('Centre d’Expertise Médicale du Personnel Naviguant', 1),
            ('BP 295 - 98713 Papeete', 2),
            ('Tel : 87.71.50.90 | Mel : cmpnpf@gmail.com', 2),
            (f"Facture {evenement.no_facture}", 2),
        ]:
            heading = doc.add_heading(text, level=level)
            heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        doc.add_paragraph("\n")
        doc.add_paragraph(f"DN : {evenement.personnel.dn}")
        doc.add_paragraph(f"Nom : {evenement.personnel.nom}")
        doc.add_paragraph(f"Prénom : {evenement.personnel.prenom}")
        doc.add_paragraph(f"Date de l'événement : {evenement.date_evenement.strftime('%d/%m/%Y')}")

        # 📌 Tableau des consultations
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER  # Centrage du tableau

        hdr_cells = table.rows[0].cells
        headers = ["Consultation", "Date", "Honoraire (XPF)", "Médecin"]
        for i, header in enumerate(headers):
            hdr_cells[i].text = header
            hdr_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            hdr_cells[i].paragraphs[0].runs[0].bold = True
            hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)

        consultations = [
            ("CEMPN", evenement.cs_cempn, evenement.date_cempn, evenement.honoraire_cempn, evenement.medecin_cempn),
            ("OPH", evenement.cs_oph, evenement.date_cs_oph, evenement.honoraire_cs_oph, evenement.medecin_oph),
            ("ORL", evenement.cs_orl, evenement.date_cs_orl, evenement.honoraire_cs_orl, evenement.medecin_orl),
            ("Radio", evenement.cs_radio, evenement.date_cs_radio, evenement.honoraire_cs_radio, evenement.medecin_radio),
            ("Labstix", evenement.cs_lbx, evenement.date_cs_lbx, evenement.honoraire_cs_lbx, None),
            ("Laboratoire AMJ", evenement.cs_labo, evenement.date_cs_labo, evenement.honoraire_cs_labo, None),
        ]

        for label, has_consult, date, honor, medecin in consultations:
            if has_consult:
                row_cells = table.add_row().cells
                row_data = [
                    label,
                    date.strftime('%d/%m/%Y') if date else "Non spécifiée",
                    f"{honor} XPF" if honor else "0 XPF",
                    str(medecin) if medecin else "Non spécifié"
                ]

                for i, data in enumerate(row_data):
                    row_cells[i].text = data
                    row_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    row_cells[i].paragraphs[0].runs[0].font.size = Pt(9)

        # 📌 Résumé paiement
        doc.add_paragraph("\n **Frais et Paiements**")
        doc.add_paragraph(f"Frais de dossier : {evenement.frais_dossier} XPF")
        doc.add_paragraph(f"Total payé par l'Organisme : {evenement.total} XPF" " | " f"Quote-part patient : {'Oui' if evenement.quote_part_patient else 'Non'}")
        #doc.add_paragraph(f"Quote-part patient : {'Oui' if evenement.quote_part_patient else 'Non'}")
        doc.add_paragraph(f"Paiement : {'Payé' if evenement.paiement else 'Non payé'}")

        if evenement.paiement:
            doc.add_paragraph(f" - Payé le : {evenement.date_paiement.strftime('%d/%m/%Y') if evenement.date_paiement else 'Non spécifiée'}")
            doc.add_paragraph(f" - Par : {evenement.get_modalite_paiement_display() if evenement.modalite_paiement else 'Non spécifiée'}")

    # 📌 Générer le fichier Word
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="Bordereau_{no_bordereau}.docx"'
    doc.save(response)

    return response  # ✅ Retourner la réponse HTTP







