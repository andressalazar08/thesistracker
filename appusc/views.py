
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

from pulp import*
import pandas as pd
import random
import numpy as np
import statistics

# Create your views here.
#Ojo esta vista tiene un primary key para controlar los comentarios que viene del template y del url
def tgrados_historial_tm(request,pk):
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
            return render(request,'appusc/tgrados_historial_tm.html',{'lista_post':lista_post,'form':form,'usuario_logueado':usuario_logueado})
            #return render(request,'appusc/formularios.html')
    else:
        #cuando se ingresa a la página el formulario debe estar en blanco
        form=formularioposteos()
        print(len(usuario_logueado))
        #aqui se realiza el filtro de los comentarios asociados al trabajo de grado que estoy consultando
        #por defecto django asigna un _id al campo foreign de la base de datos
        lista_post=posteos.objects.filter(trabajo_grado_id=pk).order_by('-fecha_pub')
        return render(request,'appusc/tgrados_historial_tm.html',{'lista_post':lista_post,'form':form,'usuario_logueado':usuario_logueado})

def cargaarchivos(request):
    #Vista de Prueba para cargue de archivos
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
    return render(request,'appusc/ctg_nuevatutoria_tm.html', {'form': form})

def tragrados(request):
    #Vista que controla el listado de tutorías asignadas
    tgs=tgrados.objects.all()
    return render(request,'appusc/tragrados_tm.html',{'tgs':tgs})


    
def ctg_listaprofes_tm(request):
    profes=profesores.objects.all()
    return render(request,'appusc/ctg_listaprofes_tm.html',{'profes':profes})

def ctg_listaestudiantes_tm(request):
    estud=estudiantes.objects.all()
    return render(request,'appusc/ctg_listaestudiantes_tm.html',{'estud':estud})


def dashboard(request):
    consulta=None
    if request.user.is_authenticated:
        #capturo el usuario que está ingresando a la aplicación.
        usuario_logeado=User.objects.get(username=request.user.get_username())
        #filtro una consulta a la base de datos donde el campo de referencia es el creado en el modelo
        consulta=comentarios.objects.filter(autor=usuario_logeado)
        #print(nombres)
        
        #print(consulta)
        #print(me)
      
        return render(request,'appusc/pro_dashboard_tm.html')
    return redirect('/')



def detail(request):
    #Vista que amarra el botón "Cerrar Sesión"
    do_logout(request)
    return render(request,'appusc/app_inicio.html')

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


def modelo(request):
    #Vista del modelo de optimización
    evaluadores=["Ev1","Ev2","Ev3","Ev4"]
    rev=evaluadores # índice i
    tgs = [1,2,3,4,5] # índice j


    # Diccionario parámetro preferencias

    preferencias={"Ev1":{1:0.10, 2:0.35, 3:0.40, 4:0.10, 5:0.05},
                "Ev2":{1:0.34, 2:0.10, 3:0.24, 4:0.20, 5:0.12},
                "Ev3":{1:0.60, 2:0.12, 3:0.09, 4:0.19, 5:0.00},
                "Ev4":{1:0.10, 2:0.00, 3:0.00, 4:0.00, 5:0.00}}

    penalizacion={"Ev1":{1:1, 2:0, 3:0, 4:1, 5:1},
                "Ev2":{1:0, 2:0, 3:1, 4:1, 5:1},
                "Ev3":{1:1, 2:1, 3:1, 4:1, 5:1},
                "Ev4":{1:1, 2:1, 3:1, 4:1, 5:1}}



    #VARIABLES DE DECISIÓN
    #Si el evaluador i es asignado al tg j 
    X = LpVariable.dicts("Asignación",[(i,j)for i in rev for j in tgs],lowBound=0,upBound=1, cat="Binary")

    #Definición del modelo
    modelo = LpProblem("ReviewerAsignment",LpMaximize)

    #Función Objetivo
    modelo+=lpSum(X[(i,j)]*preferencias[i][j]*penalizacion[i][j] for i in rev for j in tgs)

    #Un evaluador puede ser asignado máximo a 3 trabajos de grado
    for i in rev:
        modelo+=lpSum(X[(i,j)] for j in tgs)<=3

    #Un trabajo de grado debe tener asignado dos revisores siempre
    for j in tgs:
        modelo+=lpSum(X[(i,j)] for i in rev)<=2

    #Un trabajo de grado no puede ser asignado si hay algun tipo de conflicto
    for i in rev:
        for j in tgs:
            modelo+=X[(i,j)]<=penalizacion[i][j]
      
    modelo.solve()
    tipo_resultado=(LpStatus[modelo.solve()])
    #Ajuste de los datos para que el resultado de las variables salga en dataframe
    listares=[]
    for v in modelo.variables():
        listares.append(v.varValue)
    
    listadef=[]
    w=0
    for k in range(len(evaluadores)):
        listadef.append(listares[w:w+len(tgs)])
        w=w+len(tgs)
    #Este dataframe se construye dinamicamente según sean los tamaños de los elementos
    df = pd.DataFrame(listadef, columns = tgs)
    prueba_tabla=df.rename(index=lambda s:evaluadores[s])
    #Se construye el datafame como elemento html y se asigna a una variable
    prueba_tabla=prueba_tabla.to_html()
    Funcion_Objetivo=value(modelo.objective)
    
    return render(request,"appusc/modelo.html",{'tipo_resultado':tipo_resultado,'prueba_tabla':prueba_tabla,'Funcion_Objetivo':Funcion_Objetivo})




def ga(request):
    #Vista del RAP utilizando un Algoritmo Genético
    #Preferencias iniciales
    d = {0: [0.10, 0.34, 0.6, 0.1], 1: [0.35, 0.10, 0.12, 0], 2: [0.4, 0.24, 0.09, 0],3: [0.10, 0.20, 0.19, 0],4: [0.05, 0.12, 0, 0]}
    prefer = pd.DataFrame(data=d,index=[1,2,3,4])
    #Penalizaciones
    d = {0: [1, 0, 1, 1], 1: [0, 0,1, 1], 2: [0, 1, 1, 1],3: [1, 1, 1, 1],4: [1,1,1,1]}
    penal = pd.DataFrame(data=d,index=[1,2,3,4])
    
    #Step 1
    #Generación de la población incial
    FO_Z=[]
    FO_cromosoma=[]
    FO_w=[]
    #mires={}
    #for t in range(1,10000):
    while len(FO_Z)<30: #Se plantea una población incial de 30 cromosomas
        sol={}
        
        for i in range(1,5):
            #Ojo con este parámetro, representa la restricción
            w=random.randrange(1,4)
            my_list = [0]*(5-w) + [1]*w
            random.shuffle(my_list)
            sol[i]=my_list
        cromosoma=pd.DataFrame.from_dict(sol).T
        #Se evalúa la restricción de que no se asignen más de dos evaluadores a un tg
        valida=0
        for i in cromosoma-1:
            j=cromosoma[i].sum()
            if j==2:
                valida=valida+1
        if valida==len(cromosoma)+1:    
            #Se evalúa la restricción de penalidad por conflicto de intereses
            restriccion=cromosoma.le(penal)
            af=restriccion.all(axis=0).to_list()
            val=""
            for i in af:
                if i==False:
                    val=False
                    break
            if val=="":
                # Se cumplen dos restricciones más la que genera el mismo cromosoma
                #Si la matriz cumple las restricciones saco el valor de Z
                #calificacion="Si"
                #No sería necesario evaluar la función objetivo en este paso aún
                xcol=0
                for h in penal-1:
                    xcol=xcol+round((penal[h] * prefer[h]*cromosoma[h]).sum(),2)
                z=round(xcol,2)
                FO_Z.append(z)
                FO_cromosoma.append(cromosoma)

    #Integración de todo el proceso

    #------------Selección de padres

    #Se genera un número aleatorio entre 0 y el tamaño de la lista
    lista_ganadores=[0]*(len(FO_Z))

    while sum(lista_ganadores)<len(FO_Z):    
        ran_num_p1=random.randrange(0,len(FO_Z))
        print(ran_num_p1)
        ran_num_p2=random.randrange(0,len(FO_Z))
        print(ran_num_p2)
        padres_torneo=[]
        if ran_num_p1!=ran_num_p2:
            padres_torneo.append(FO_Z[ran_num_p1])
            padres_torneo.append(FO_Z[ran_num_p2])
            if FO_Z[ran_num_p1]>=FO_Z[ran_num_p2]:
                ganador=FO_Z[ran_num_p1]
                ubicacion=ran_num_p1
            else:
                ganador=FO_Z[ran_num_p2]
                ubicacion=ran_num_p2
            lista_ganadores[ubicacion]=lista_ganadores[ubicacion]+1

    #-----------Cruce de padres para obtener hijos

    nueva_generacion=[]
    nueva_generacion_FO=[]
    seg_mejor_ubicado=-2
    pri_mejor_ubicado=None

    lista_ganadores_2=lista_ganadores

    #while len(nueva_generacion)<30:

    #Selecciono los dos mejores padres para cruzar de la lista_ganadores
    delete=-2

    while len(nueva_generacion)<30:
        for i in range(1,5):
            top_2_idx = np.argsort(lista_ganadores_2)[seg_mejor_ubicado:pri_mejor_ubicado]
            top_2_values = [lista_ganadores_2[i] for i in top_2_idx]
            mejores_padres =top_2_idx.tolist()

            #Escojo la primera sección del primer mejor padre
            first_slice_1=FO_cromosoma[mejores_padres[0]].loc[:,[0, 1]]

            #Escojo la segunda sección del segundo mejor padre
            second_slice_1=FO_cromosoma[mejores_padres[1]].loc[:,[2,3,4]]

            #Combino las secciones para obtener el primer hijo
            cruce_1 = pd.concat([first_slice_1, second_slice_1], axis=1)


            #Escojo la segunda sección del primer mejor padre
            first_slice_2=FO_cromosoma[mejores_padres[0]].loc[:,[2,3,4]]

            #Escojo la segunda sección del segundo mejor padre
            second_slice_2=FO_cromosoma[mejores_padres[1]].loc[:,[0, 1]]

            #Combino las secciones para obtener el segundo hijo
            cruce_2 = pd.concat([second_slice_2,first_slice_2], axis=1)


            #-----------Mutación de hijos

            #Genero un número aleatorio para determinar la probabilidad de mutación
            tamanio=1/len(FO_Z)
            alpha = round(np.random.uniform(0,1,1)[0],3)
            if tamanio>alpha:
                print(alpha)
                print("Hace mutación")   
                #Realiza la mutacion del primer hijo
                var=random.randrange(1,len(cruce_1.index))
                temp = cruce_1.iloc[-var]
                cruce_1.iloc[-var] = cruce_1.iloc[-(var+1)]
                cruce_1.iloc[-(var+1)] = temp
                #Realiza la mutación del segundo hijo
                var=random.randrange(1,len(cruce_2.index))
                temp = cruce_2.iloc[-var]
                cruce_2.iloc[-var] = cruce_2.iloc[-(var+1)]
                cruce_2.iloc[-(var+1)] = temp


            #-----------Validación si los hijos cruzados y/o mutados son factibles

            #Valido si el primer hijo es factible

            #Se evalúa la restricción de que no se asignen más de dos evaluadores a un tg en el primer hijo
            valida_1=0
            for i in cruce_1-1:
                j=cruce_1[i].sum()
                if j==2:
                    valida_1=valida_1+1

            #Se evalúa la restricción de que no se le asignen más de tres trabajos de grado a cada evaluador en el primer hijo
            lista_revalida_1=cruce_1.sum(axis=1).tolist()
            revalida_1=0 #cero si no hay problema con la restricción
            for k in lista_revalida_1:
                if k >3:
                    revalida_1=1
                    break

            #Se evalúa la restricción de que no tenga conclicto de intereses en el primer hijo
            restriccion_1=cruce_1.le(penal)
            af_1=restriccion_1.all(axis=0).to_list()
            val_1=""
            for i in af_1:
                if i==False:
                    val_1=False
                    break

            #Valido si el segundo hijo es factible

            #Se evalúa la restricción de que no se asignen más de dos evaluadores a un tg en el primer hijo
            valida_2=0
            for i in cruce_2-1:
                j=cruce_2[i].sum()
                if j==2:
                    valida_2=valida_2+1

            #Se evalúa la restricción de que no se le asignen más de tres trabajos de grado a cada evaluador en el segundo hijo
            lista_revalida_2=cruce_2.sum(axis=1).tolist()
            revalida_2=0 #cero si no hay problema con la restricción
            for k in lista_revalida_2:
                if k >3:
                    revalida_2=1

            #Se evalúa la restricción de que no tenga conclicto de intereses en el segundo hijo
            restriccion_2=cruce_2.le(penal)
            af_2=restriccion_2.all(axis=0).to_list()
            val_2=""
            for i in af_2:
                if i==False:
                    val_2=False
                    break

            #-----------Construcción de la nueva generación



            if valida_1==len(cruce_1)+1 and val_1=="" and revalida_1==0:
                nueva_generacion.append(cruce_1)
                xa=round((penal[0] * prefer[0]*cruce_1[0]).sum(),2)
                xb=round((penal[1] * prefer[1]*cruce_1[1]).sum(),2)
                xc=round((penal[2] * prefer[2]*cruce_1[2]).sum(),2)
                xd=round((penal[3] * prefer[3]*cruce_1[3]).sum(),2)
                xe=round((penal[4] * prefer[4]*cruce_1[4]).sum(),2)
                z=round(xa+xb+xc+xd+xe,2)
                nueva_generacion_FO.append(z)

            if valida_2==len(cruce_2)+1 and val_2=="" and revalida_2==0:
                nueva_generacion.append(cruce_2)
                xa=round((penal[0] * prefer[0]*cruce_2[0]).sum(),2)
                xb=round((penal[1] * prefer[1]*cruce_2[1]).sum(),2)
                xc=round((penal[2] * prefer[2]*cruce_2[2]).sum(),2)
                xd=round((penal[3] * prefer[3]*cruce_2[3]).sum(),2)
                xe=round((penal[4] * prefer[4]*cruce_2[4]).sum(),2)
                z=round(xa+xb+xc+xd+xe,2)
                nueva_generacion_FO.append(z)

            print("Hasta aquí la lista va en " +str(lista_ganadores) )
            lista_ganadores_2=lista_ganadores_2[:-1]

        nueva_generacion_FO=nueva_generacion_FO[:30]
        nueva_generacion=nueva_generacion[:30]       
    
        
    max_value = max(nueva_generacion_FO)
    max_index = nueva_generacion_FO.index(max_value)
    resultado_ga_fo=max_value
    prueba_tabla=nueva_generacion[max_index].to_html()
    #evaluadores=["Ev1","Ev2","Ev3","Ev4"]
    #prueba_tabla=prueba_tabla.rename(index=lambda s:evaluadores[s]).to_html()
    

    return render(request,"appusc/genetic_algorithm.html",{'prueba_tabla':prueba_tabla,'resultado_ga_fo':resultado_ga_fo})



