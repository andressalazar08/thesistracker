from django.contrib import admin
from .models import comentarios, profesores,estudiantes,tgrados,posteos

# Register your models here.
#cada que se cree un modelo hay que registrarlo a la aplicación
admin.site.register(comentarios)
admin.site.register(profesores)
admin.site.register(estudiantes)
admin.site.register(tgrados)
admin.site.register(posteos)
