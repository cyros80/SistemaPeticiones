from django.urls import path
 
from . import views
from .views import register
 
urlpatterns = [
    path('solicitudm/', views.create_view, name='add'),
    path('', views.select, name='home'),
    path('solicitud/<int:pk>/', views.update_view, name='change'), 
    path('member/ajax/load-personals/', views.load_personals, name='ajax_load_personals'), # AJAX
    path('logout/', views.signout,name='exit'),
    path('register/',register,name='register'),
    path('buscar/',views.index,name='index'),
    path('peticionescom/',views.todascom,name='peticionescom'),
    path('peticionesmat/',views.todasmat,name='peticionesmat'),
    path('list_peticiones/',views.list_peticones,name='list_peticiones'),
    path('editarPendinete3/<int:id>',views.editar3,name='editar3'),
    path('eliminar/<int:id>',views.eliminarPendiente,name='eliminar'),
    path('editarPendiente2/',views.editar_pendiente2,name='editarPendiente2'),
    path('showproducts/',views.show_products,name='showproducts'),
    path('createPdf',views.pdf_report_create,name='create-pdf'),
    path('createPdf/<int:id>',views.pdf_report_create_id,name='create-pdf-id'),
    path('createPdfForm/',views.pdf_report_create_form,name='create-pdf-form'),
    path('correo/',views.subirCorreo,name='correo'),
    path('registrar/',views.registrar,name='Registrar'),
    
    
]