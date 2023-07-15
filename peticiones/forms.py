from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Peticion,Personal,Problema,Correos
 
class RequestCreationForm(forms.ModelForm):
    class Meta:
        model = Peticion
        fields = 'area','personal','equipo','problema'
         
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['personal'].queryset = Personal.objects.none()
        self.fields['problema'].queryset = Problema.objects.none()
 
        if 'area' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['personal'].queryset = Personal.objects.filter(area_id=area_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['personal'].queryset = self.instance.area.personal_set.order_by('name')

        if 'equipo' in self.data:
            try:
                equipo_id = int(self.data.get('equipo'))
                self.fields['problema'].queryset = Problema.objects.filter(equipo_id=equipo_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['problema'].queryset = self.instance.equipo.problema_set.order_by('name')            

#////////////////////////////////////////////////#


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name', 'last_name', 'email', 'password1', 'password2','groups']

class ComentarioContactoForm(forms.ModelForm):
    class Meta:
        model = Correos
        fields = ['nombre','ncontrol','accion','imagen']             