from django.shortcuts import render
from .models import Conference
from django.urls import reverse_lazy
from .forms import ConferenceModel
from django.views.generic import ListView,DetailView,CreateView,UpdateView , DeleteView
from django.contrib.auth.mixins import  LoginRequiredMixin
# Create your views here.
def all_conference(req):
    conferences=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":conferences})

class ConferenceListe(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="Conference/liste.html"

class ConferenceDetail(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="Conference/details.html"
class ConferenceCreate(CreateView):
    model=Conference
    template_name="conference/conference_form.html"
    #fields ='__all__'
    form_class =ConferenceModel
    success_url=reverse_lazy("conference_liste")

class ConferenceUpdate(UpdateView):
    model= Conference
    template_name="conference/conference_form.html"
    #fields ='__all__'
    form_class =ConferenceModel
    success_url=reverse_lazy('conference_liste')
class ConferenceDelete(DeleteView):
    model=Conference
    template_name="conference/conference_confirm_delete.html"
    success_url=reverse_lazy("conference_liste")





