from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout as do_logout

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

#Instrucción para importar el modelo de base de datos a las vistas
from .models import *
from .forms import formulariotutorias,formularioposteos

#se importa el gestor de archivos de django como API
from django.core.files.storage import FileSystemStorage

from django.views.generic import ListView, DetailView

from django.utils import timezone



class post_view(ListView):
    model=posteos
    template_name='appusc/formularios.html'


class tutoria_detalle(DetailView):
    model=posteos
    template_name='appusc/detalles_tutorias.html'


# Create your views here.
#Ojo esta vista tiene un primary key para controlar los comentarios que viene del template y del url
def ultima(request,pk):
    usuario_logueado=request.user.get_username()
    if request.method=='POST':
        #creo una variable para guardar el formulario que se renderiza en esta página desde .forms
        #Del formulario se guardan los datos y el archivo
        form=formularioposteos(request.POST,request.FILES)
        #se verifica si el formulario es valido
        if form.is_valid():
            #Hago el commit temporal de lo que se va a guardar del formulario en una variable
            arreglo=form.save(commit=False)
            #la fecha viene por defecto en el modelo de la base de datos
                #arreglo.fecha_pub=timezone.now
            #Tomo de la url actual de la página el pk correspondiente para asignar el comentario al trabajo de grado
            arreglo.trabajo_grado_id=pk
            #capturo en la entrada el usuario logueado, debe quedar el post a nombre de él
            arreglo.autor=User.objects.get(username=request.user.get_username())
            #una vez tengo los datos completos guardo el formulario en la base de datos
            arreglo.save()
            #print(temporal)
            lista_post=posteos.objects.filter(trabajo_grado_id=pk).order_by('-fecha_pub')
            #Después de guardar los datos debe quedar en blanco el formulario y mostrar la misma página
            form=formularioposteos()
            return render(request,'appusc/lista.html',{'lista_post':lista_post,'form':form,'usuario_logueado':usuario_logueado})
            #return render(request,'appusc/formularios.html')
    else:
        #cuando se ingresa a la página el formulario debe estar en blanco
        form=formularioposteos()
        print(len(usuario_logueado))
        #aqui se realiza el filtro de los comentarios asociados al trabajo de grado que estoy consultando
        #por defecto django asigna un _id al campo foreign de la base de datos
        lista_post=posteos.objects.filter(trabajo_grado_id=pk).order_by('-fecha_pub')
        return render(request,'appusc/lista.html',{'lista_post':lista_post,'form':form,'usuario_logueado':usuario_logueado})

def cargaarchivos(request):
    url_tutoria=posteos.objects.all()
    print(url_tutoria)
    contexto={}

    if request.method=='POST':
        
        #coment=request.TextField['comentario']
        archivo_cargado=request.FILES['document']
        arch=FileSystemStorage()
        arch.save(archivo_cargado.name,archivo_cargado)
        nombre_ruta= arch.save(archivo_cargado.name,archivo_cargado)
        #De esta manera el sistema de archivos genera una url automática para el archivo cargado
        url_archivo=arch.url(nombre_ruta)
        #podemos pasarle la url como contexto al template
        contexto['url']=url_archivo

        print(archivo_cargado.name)
        print(archivo_cargado.size)
        print(url_archivo)
    return render(request,'appusc/formularios.html',contexto)



def nuevatutoria(request):
    if request.method=="POST":
        form=formulariotutorias(request.POST)
        if form.is_valid():
            datos=form.save(commit=False)
            datos.fecha_asignacion=timezone.now()
            datos.save()
            return redirect('/tutoriastgs')
    else:
        form=formulariotutorias()
    return render(request,'appusc/nuevatutoria.html', {'form': form})

def tutoriastgs(request):
    tgs=tgrados.objects.all()
    return render(request,'appusc/tutorias.html',{'tgs':tgs})

def base(request):
    return render(request,'appusc/base.html')
    
def listaprofes(request):
    profes=profesores.objects.all()
    return render(request,'appusc/listaprofes.html',{'profes':profes})

def listaestudiantes(request):
    estud=estudiantes.objects.all()
    return render(request,'appusc/listaestudiantes.html',{'estud':estud})


def dashboard(request):
    consulta=None
    if request.user.is_authenticated:
        #capturo el usuario que está ingresando a la aplicación.
        usuario_logeado=User.objects.get(username=request.user.get_username())
        #filtro una consulta a la base de datos donde el campo de referencia es el creado en el modelo
        consulta=comentarios.objects.filter(autor=usuario_logeado)
        #print(nombres)
        
        print(consulta)
        #print(me)
      
        return render(request,'appusc/dashboard.html')
    return redirect('/')

def dashboardcopy(request):
 
    return render(request,'appusc/dashboardcopy.html')


def detail(request):
    do_logout(request)
    return render(request,'appusc/inicio.html')

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "appusc/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    # Si llegamos al final renderizamos el formulario
    return render(request, "appusc/register.html", {'form': form})


def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos al template de bienvenida
                return redirect('/dashboard')

    # Si llegamos al final renderizamos el formulario
    return render(request, "appusc/login.html", {'form': form})

def salida(request):
    do_logout(request)
    return render(request,'appusc/vlogout.html')




