from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class profesores(models.Model):
    cedula=models.IntegerField()
    nombres=models.CharField(max_length=400)
    apellidos=models.CharField(max_length=400)

class estudiantes(models.Model):
    cedula=models.IntegerField()
    nombres=models.CharField(max_length=400)
    apellidos=models.CharField(max_length=400)


modalidades=(('Diploma Course','Diploma Course'),('Research Case','Research Case'),('Entrepeneuership work','Entrepeneuership work'))
estados=(('In Progress','In Progress'),('Finished','Finished'))

class tgrados(models.Model):
    #modelo que se usa en ctg_nuevatutoria
    titulo=models.CharField(max_length=400)
    Status=models.CharField(max_length=100,choices=estados,default='In Progress')
    modalidad=models.CharField(max_length=100,choices=modalidades,default='Study Case Research')
    cedula1=models.IntegerField()
    nombre1=models.CharField(max_length=400)
    apellidos1=models.CharField(max_length=400)
    programa1=models.CharField(max_length=400)
    cedula2=models.IntegerField(blank=True,null=True)
    nombre2=models.CharField(max_length=400,blank=True, default='')
    apellidos2=models.CharField(max_length=400,blank=True, default='')
    programa2=models.CharField(max_length=400,blank=True, default='')
    cedula3=models.IntegerField(blank=True,null=True)
    nombre3=models.CharField(max_length=400,blank=True, default='')
    apellidos3=models.CharField(max_length=400,blank=True, default='')
    programa3=models.CharField(max_length=400,blank=True, default='')
    fecha_asignacion=models.DateTimeField(default=timezone.now)
    def publish(self):
        self.fecha_asignacion=timezone.now()
        self.save()

    def __str__(self):
        return str(self.titulo)

class posteos(models.Model):
    
    titulo=models.CharField(max_length=100)
    fecha_pub=models.DateTimeField(default=timezone.now)
    #fecha_pub=models.DateField(default=timezone.now)
    trabajo_grado=models.ForeignKey(tgrados,on_delete=models.CASCADE)
    autor=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    texto=models.TextField(max_length=300)
    archivo=models.FileField(upload_to='postarchivos/',default='',blank=True)


    def __str__(self):
        return self.titulo

    class Meta:
        ordering=['-fecha_pub']

class comentarios(models.Model):
    autor=models.ForeignKey('auth.User',on_delete=models.CASCADE)

    titulo=models.CharField(max_length=400)
    texto=models.TextField()
    fecha_creacion=models.DateTimeField(default=timezone.now)
    fecha_publicacion=models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.fecha_publicacion=timezone.now()
        self.save()
    
    def __str__(self):
        return self.titulo

