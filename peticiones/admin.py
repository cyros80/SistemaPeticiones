from django.contrib import admin

# Register your models here.
from peticiones.models import Area, Personal, Peticion,Problema,Equipo,Correos


class AdministrarModelo(admin.ModelAdmin):
    list_display = ('id', 'area', 'personal','estado')

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display= ('id', 'nombre')
    search_fields = ('id','created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')    


admin.site.register(Area)
admin.site.register(Personal)
admin.site.register(Peticion,AdministrarModelo)
admin.site.register(Problema)
admin.site.register(Equipo)
admin.site.register(Correos,AdministrarComentariosContacto)


