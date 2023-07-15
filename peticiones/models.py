from django.db import models

# Create your models here.
class Area(models.Model):
    name=models.CharField(max_length=120)

    class Meta:
        verbose_name= "Area"
        verbose_name_plural= "Areas"
        
    
    def __str__(self):
        return self.name
    
class Personal(models.Model):
    area=models.ForeignKey(Area,on_delete=models.CASCADE)
    name=models.CharField(max_length=120)

    class Meta:
        verbose_name= "Personal"
        verbose_name_plural= "Personal"
       

    def __str__(self):
        return self.name
    

class Equipo(models.Model):
    name=models.CharField(max_length=40)

    class Meta:
        verbose_name= "Equipo"
        verbose_name_plural= "Equipos"
        

    def __str__(self):
        return self.name

class Problema(models.Model):
    equipo=models.ForeignKey(Equipo,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)

    class Meta:
        verbose_name= "Problema"
        verbose_name_plural= "Problemas"
        

    def __str__(self):
        return self.name        

class Peticion(models.Model):
    id=models.AutoField(primary_key=True)
    area=models.ForeignKey(Area,on_delete=models.SET_NULL,blank=False,null=True)
    personal=models.ForeignKey(Personal,on_delete=models.SET_NULL,blank=False,null=True)
    equipo=models.ForeignKey(Equipo,on_delete=models.SET_NULL,blank=False,null=True)
    problema=models.ForeignKey(Problema,on_delete=models.SET_NULL,blank=False,null=True)
    os_choices ={
        ('Pendiente', 'Pendiente'),
        ('En Proceso','En Proceso'),
        ('Finalizada','Finalizada'),
        
    }
    estado=models.CharField(max_length=20,default="Pendiente",choices=os_choices)
    fsolicitud=models.DateTimeField(auto_now_add=True)
    
    


    class Meta:
        verbose_name= "Peticion"
        verbose_name_plural= "Peticiones"

    def __str__(self):
        return self.area.name


class Correos(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=50,verbose_name='Nombre')
    ncontrol=models.CharField(max_length=15,verbose_name='Numero Control')
    os_choices ={
        ('Recuperar Contraseña', 'Recuperar Contraseña'),
        ('Crear Correo','Crear Correo'),
        
        
    }
    accion=models.CharField(choices=os_choices,max_length=20,verbose_name='Problema')
    imagen=models.ImageField(null=True,upload_to="fotos",verbose_name='Foto Credencial o Identificacion')
    created=models.DateTimeField(auto_now_add=True)             

    class Meta:
            verbose_name = "Solicitud Correo"
            verbose_name_plural = "Solicitudes Correos"
            ordering = ["-created"]
    def __int__(self):
     return self.id    

