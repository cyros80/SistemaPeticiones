from django.shortcuts import render,redirect,get_object_or_404
from.forms import RequestCreationForm
from .models import Personal,Peticion,Problema
from peticiones import models
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import CustomUserCreationForm, RequestCreationForm,ComentarioContactoForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from .decorators import custom_login_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def create_view(request):
    form = RequestCreationForm()
    if request.method == 'POST':
        form = RequestCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-pdf-form')
        
    return render(request, 'home.html', {'form': form})
 
def update_view(request, pk):
    peticion = get_object_or_404(Peticion, pk=pk)
    form = RequestCreationForm(instance=peticion)
    if request.method == 'POST':
        form = RequestCreationForm(request.POST, instance=peticion)
        if form.is_valid():
            form.save()
            return redirect('change', pk=pk)
    return render(request, 'home.html', {'form': form})
 
# AJAX
def load_personals(request):
    area_id = request.GET.get('area_id')
    personals = Personal.objects.filter(area_id=area_id).all()
    equipo_id =request.GET.get('equipo_id')
    equipos = Problema.objects.filter(equipo_id=equipo_id).all()
    return render(request, 'personal_dropdown_list_options.html', {'personals': personals,'equipos':equipos})



def signout(request):
    logout(request)
    return redirect('/')


def register(request):
    data ={
        'form':CustomUserCreationForm()
    }

    if request.method =='POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()

            user=authenticate(username=user_creation_form.cleaned_data['username'],password=user_creation_form.cleaned_data['password1'],groups=user_creation_form.cleaned_data['groups'])
            login(request,user)

            return redirect('exit')

    return render(request, 'registration/register.html', data)

def index(request):
    return render(request,'index.html')

@login_required
def select(request):
    return render(request,'select.html')

def peticiones(request):
    return render(request,'peticiones.html')

def indexs(request):
    group = request.user.groups.filter(user=request.user)[0]
    if group.name=="Computo":
        return HttpResponseRedirect(reverse('peticionescom'))
    elif group.name=="Materiales":
        return HttpResponseRedirect(reverse('peticionesmat'))
    

   

    context = {}
    template = "pendientes/home.html"
    return render(request, template, context)

def group_required(*group_names):
   """ Evalua si el usuario pertenece a alguno de los grupos indicados."""

   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

def list_peticones(request):
    peticiones=list(Peticion.objects.values())
    data={'peticiones':peticiones}
    return JsonResponse(data)

def eliminarPendiente(request,id,confirmacion='confirmar.html'):
    pendiente= get_object_or_404(Peticion,id=id)
    if request.method=='POST':
        pendiente.delete()
        pendientes=Peticion.objects.all()
        return redirect('/')
    return render(request,confirmacion,{'object':pendiente})

def editarPendiente(request, id):
    pendiente2=get_object_or_404(Peticion,id=id)
    form= RequestCreationForm(request.POST, instance=pendiente2)

    if form.is_valid():
        form.save()
        pendientes=Peticion.objects.all()
        return render(request,"home.html",{'pendientes':pendientes})
    

    return render(request,"editarPendiente.html",{'pendiente':pendiente2})

def editar3(request,id,):
    pendientes= get_object_or_404(Peticion,id=id)
    return render(request,"editarpendiente3.html",{'pendientes':pendientes})

def editar_pendiente2(request):
    id=int(request.POST['id'])
    estado =request.POST['Estado']
    
    pendiente=Peticion.objects.get(id=id)
    pendiente.estado=estado
    pendiente.save()

    return redirect('/')
    
@group_required('Computo')
def todascom(request):
    peticionesp=Peticion.objects.filter(estado="Pendiente")
    peticionese=Peticion.objects.filter(estado="En Proceso")
    peticionesf=Peticion.objects.filter(estado="Finalizada")

    return render(request,'peticionescom.html',{"peticionesf":peticionesf,"peticionese":peticionese,"peticionesp":peticionesp})

@group_required('Materiales')
def todasmat(request):
    peticionesp=Peticion.objects.filter(estado="Pendiente")
    peticionese=Peticion.objects.filter(estado="En Proceso")
    peticionesf=Peticion.objects.filter(estado="Finalizada")

    return render(request,'peticionesmat.html',{"peticionesf":peticionesf,"peticionese":peticionese,"peticionesp":peticionesp})        


def show_products(request):
    products = Peticion.objects.all()

    context={
        'products':products
    }
    return render(request,'pdf-covert/showInfo.html',context)

def pdf_report_create(request):
    products=Peticion.objects.all()

    template_path = 'pdf-covert/pdfReport.html'

    context = {'products': products}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="products_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response   


def pdf_report_create_id(request,id):
    products=Peticion.objects.get(id=id)

    template_path = 'pdf-covert/pdfReport.html'

    context = {'products': products}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="products_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def pdf_report_create_form(request):
    products=Peticion.objects.latest('id')

    template_path = 'pdf-covert/pdfReport.html'

    context = {'products': products}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="products_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response        

def registrar(request):
    if request.method == 'POST':
        form=ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'formCorreo.html')
    form= ComentarioContactoForm()
    return render(request,'select.html',{'form':form})

def contacto(request):
    return render(request,"formCorreo.html")   


def enviar(request):
    pendientes_form=ComentarioContactoForm()
    if request.method == 'POST':
        pendientes_form=ComentarioContactoForm(data=request.POST)

        if pendientes_form.is_valid():
            pendientes_form.save()
            return redirect(reverse('correo')+'?ok')
        else:
            return redirect(reverse('correo')+'?error')

    return render(request,'formCorreo.html',{'form':pendientes_form})

def home_view(request):
    context = {}
    if request.method == "POST":
        form = ComentarioContactoForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("geeks_field")
            obj = ComentarioContactoForm.objects.create(
                                 title = name,
                                 img = img
                                 )
            obj.save()
            print(obj)
    else:
        form = ComentarioContactoForm()
    context['form']= form
    return render(request, "home.html", context)

def upload(request):
	if request.method == "POST":
		form = ComentarioContactoForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
            
		return redirect("home")
	form = ComentarioContactoForm()
	
	return render(request=request, template_name="formCorreo.html", context={'form':form})


def subirCorreo(request):
    form=ComentarioContactoForm()
    if request.method == 'POST':
        form=ComentarioContactoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('correo')+'?ok')
        else:
            return redirect(reverse('correo')+'?error')
    return render(request,'formCorreo.html',{'form':form})    



