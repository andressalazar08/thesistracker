from django import forms
from .models import*

class formulariotutorias(forms.ModelForm):

    class Meta:
        model=tgrados
        fields=('titulo','modalidad','cedula1','nombre1','apellidos1','programa1','cedula2','nombre2','apellidos2','programa2','cedula3','nombre3','apellidos3','programa3')
        #Se introducen etiquetas para que el usuario vea un formulario mejor presentado
        labels={'titulo':'Final Work Title',

        'cedula1':'ID First Student',
        'nombre1':'First Student Name',
        'apellidos1':'First Student Last Name',
        'programa1':'Study Plan',

        
        'cedula2':'ID Second Student',
        'nombre2':'Second Student Name',
        'apellidos2':'Second Student Last Name',
        'programa2':'Study Plan',

        
        'cedula3':'ID Third Student',
        'nombre3':'First Student Name',
        'apellidos3':'First Student Last Name',
        'programa3':'Study Plan',
        
        
        }
from django.forms.widgets import HiddenInput

class formularioposteos(forms.ModelForm):

    class Meta:
        model=posteos
         
        fields= ('titulo','texto','archivo')
        exclude=('fecha_pub','trabajo_grado','autor')
        labels={
            'titulo':'Title',
            'texto': 'Enter a Description',
            'archivo': 'Files to load',
        }


