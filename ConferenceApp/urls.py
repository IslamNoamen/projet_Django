from django.urls import path
from .views import *
#from . import views

urlpatterns=[
    #path("liste/",views.all_conference,name="conference_liste"),
    path("liste/",ConferenceListe.as_view(),name="conference_liste"),
    path("details/<int:pk>/",ConferenceDetail.as_view(),name="conference_detail"),
    path("form/",ConferenceCreate.as_view(),name="conference_add"),
    path("<int:pk>/edit/",ConferenceUpdate.as_view(),name="conference_update"),
    path("<int:pk>/delete/",ConferenceDelete.as_view(),name="conference_delete"), 


    
]