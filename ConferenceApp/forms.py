from django import forms

from .models import Conference


class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','description','location','start_date','end_date']

        labels = {
            'name': 'Conference Name',
            'theme': 'Conference Theme',
            'description': 'Description',
            'location': 'Location',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        widgets ={
            'start_date' : forms.DateInput(
                attrs= {
                    'type':"date",
                    'placeholder':"date de debut"
                }
            
            ),
            'end_date' : forms.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder':"date de fin"            
                            }
            )
        }