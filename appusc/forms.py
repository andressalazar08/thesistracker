from django import forms
from .models import*

class formulariotutorias(forms.ModelForm):

    class Meta:
        model=tgrados
        fields=('titulo','modalidad','cedula1','nombre1','apellidos1','programa1','cedula2','nombre2','apellidos2','programa2','cedula3','nombre3','apellidos3','programa3')
        #Se introducen etiquetas para que el usuario vea un formulario mejor presentado
        labels={'titulo':'Título del Trabajo de Grado',

        'cedula1':'Cédula primer estudiante',
        'nombre1':'Nombres primer estudiante',
        'apellidos1':'Apellidos primer estudiante',
        'programa1':'Plan de estudios primer estudiante',

        
        'cedula2':'Cédula segundo estudiante',
        'nombre2':'Nombres segundo estudiante',
        'apellidos2':'Apellidos segundo estudiante',
        'programa2':'Plan de estudios segundo estudiante',

        
        'cedula3':'Cédula tercer estudiante',
        'nombre3':'Nombres tercer estudiante',
        'apellidos3':'Apellidos tercer estudiante',
        'programa3':'Plan de estudios tercer estudiante',
        
        
        }
from django.forms.widgets import HiddenInput

class formularioposteos(forms.ModelForm):

    class Meta:
        model=posteos
         
        fields= ('titulo','texto','archivo')
        exclude=('fecha_pub','trabajo_grado','autor')
        labels={
            'titulo':'Titulo',
            'texto': 'Ingrese un comentario',
            'archivo': 'Archivo a cargar',
        }


