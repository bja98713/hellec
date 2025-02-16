# expertise/urls.py

from django.urls import path
from .views import (
    PersonnelListView,
    PersonnelDetailView,
    PersonnelCreateView,
    PersonnelUpdateView,
    PersonnelDeleteView,
    FicheEvenementCreateView,
    FicheEvenementUpdateView,
    FicheEvenementDeleteView,
    bordereau_selection_view,
    bordereau_view,
    download_bordereau,
    FactureView,  # Import de la nouvelle vue
)

urlpatterns = [
    path('personnels/', PersonnelListView.as_view(), name='personnel_list'),
    path('personnels/add/', PersonnelCreateView.as_view(), name='personnel_add'),
    path('personnels/<str:dn>/', PersonnelDetailView.as_view(), name='personnel_detail'),
    path('personnels/<str:dn>/edit/', PersonnelUpdateView.as_view(), name='personnel_edit'),
    path('personnels/<str:dn>/delete/', PersonnelDeleteView.as_view(), name='personnel_delete'),
    path('personnels/<str:dn>/evenements/add/', FicheEvenementCreateView.as_view(), name='evenement_add'),
    path('evenement/<int:pk>/edit/', FicheEvenementUpdateView.as_view(), name='evenement_edit'),
    path('evenement/<int:pk>/delete/', FicheEvenementDeleteView.as_view(), name='evenement_delete'),
    path('evenement/<int:pk>/facture/', FactureView.as_view(), name='facture'),
    path("bordereau/<int:annee>/<int:mois>/<str:iata>/", bordereau_view, name="bordereau_detail"),
    path("bordereau/selection/", bordereau_selection_view, name="selectionner_bordereau"),
    path('bordereau/<int:mois>/<int:annee>/<str:iata>/download/', download_bordereau, name='download_bordereau'),
]