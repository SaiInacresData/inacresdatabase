from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from .models import Note, New_registration, Document_details, post_image, New_Project, PostImage, PlotAmount, PlotAvailability
from .serializers import NoteSerializer, NewRegistrationSerializer, NewDocumentSerializer, NewProjectSerializer
# Create your views here.
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from api import forms
from .forms import NoteForm, NewProjectForm, NewRegistrationForm, NewDocumentForm, DocumentImageForm, PlotAmountForm
from django.db.models import Q
from django.utils.decorators import method_decorator

@login_required
def index(request):
    return render(request, "index.html")

# def getNotes(request):
#     Notes = Note.objects.all()
#     return render(request, 'notes.html', {'data':Notes})

#creating new projects
@login_required
def newProject(request):
    if request.method == 'POST':
        form = NewProjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Plot Account Was Successfully Created.',
                             extra_tags='alert alert-success')
            form = NewProjectForm() 
        else:
            print(form.errors)
            messages.warning(request, 'Sorry, Something went wrong!', extra_tags='alert alert-warning')
    else:
        form = NewProjectForm() 
    return render(request, 'newproject.html', {'form': form})

# creating the new registration form 
@login_required
def newRegistration(request):
    if request.method == 'POST':
        form = NewRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Plot Account Was Successfully Created.',
                             extra_tags='alert alert-success')
            form= NewRegistrationForm()
        else:
            print(form.errors)
            messages.warning(request, 'Sorry, Something went wrong!', extra_tags='alert alert-warning')                     
    else:
        form= NewRegistrationForm()
    return render(request, 'newregistration.html', {'form': form})
#

class RegUpdateView(LoginRequiredMixin,UpdateView):
    model = New_registration
    fields = "__all__"
    template_name = 'reg_update_view.html'
    success_url = '/'
    
class RegDelView(LoginRequiredMixin, DeleteView):
    model = New_registration
    success_url ="/"
    template_name = "reg_delete_view.html"

#user details list
@login_required
def user_details(request):
    plot = PlotAvailability.objects.all()
    pro = New_Project.objects.all()
    query = Document_details.objects.all()
    return render(request, 'user_details.html', {"query": query, 'pro': pro, 'plot': plot})
    
# # getting all registration details
# @login_required
# def newRegistrationList(request):
#     registrations = New_registration.objects.all()
#     return render(request, "registration_list.html", {'data': registrations})
    
#  # getting the list of single registraion details   
# def registrationList(request, pk):
#     registration = New_registration.objects.get(id=pk)
#     return render(request, "registration_pk.html", {'data': registration})

    
# creating the new document form
@login_required
def newDocuments(request):
    if request.method =='POST':
        form = DocumentImageForm(request.POST or None, request.FILES)
        images = request.FILES.getlist('document_photos')
        if form.is_valid():
            # project_name = form.cleaned_data.get('project_name')
            # plot_no = form.cleaned_data.get('plot_no')
            # katha_no = form.cleaned_data.get('katha_no')
            # new_passbook_no = form.cleaned_data.get('new_passbook_no')
            # document_no = form.cleaned_data.get('document_no')
            # aadhar_no = form.cleaned_data.get('aadhar_no')
            # pass_photo = form.cleaned_data.get('pass_photo')
            # passbook_photo = form.cleaned_data.get('passbook_photo')
            # Note = form.cleaned_data.get('Note')
            # object = Document_details(
            #     project_name=project_name,
            #     plot_no=plot_no,
            #     katha_no=katha_no,
            #     new_passbook_no=new_passbook_no,                  
            #     document_no=document_no,
            #     aadhar_no=aadhar_no,
            #     pass_photo=pass_photo,
            #     passbook_photo=passbook_photo,
            #     Note=Note,
            # )
            obj = form.save()
            for i in images:
                data = PostImage(post=obj, document_photos=i)
                data.save()
            form = DocumentImageForm()
            """    
            variable = Extent_sites(post=object, project=object.project_name,variable_plot=object.plot_no, checked = True)
            variable.save()
            """
            messages.success(request, 'Thank you! Plot Account Was Successfully Created.',
                             extra_tags='alert alert-success')           
        else:
            print(form.errors)
            messages.warning(request, 'Sorry, Something went wrong!', extra_tags='alert alert-warning')                     
            
    else:
        form = DocumentImageForm()
    return render(request, 'newdocuments.html', {'form': form})

class DocUpdateView(UpdateView):
    model = Document_details
    form_class = NewDocumentForm
    template_name = 'doc_update_view.html'
    success_url = '/'

def load_plot_no(request):
    project_name_id = request.GET.get('projectId')
    plot_nos = New_registration.objects.raw('select * from api_new_registration where api_new_registration.project_name_id = %s', [project_name_id])
    return render(request, 'dropdown_list_options.html',  {'plot_nos': plot_nos})
 
@login_required   
def sites(request):
    QuerySet = ''
    query = request.GET.get('q', None)
    if query:
        first_name = query.split(' ')[0]
        last_name  = query.split(' ')[0]
        QuerySet = Document_details.objects.filter(Q(plot_no__plot_no__icontains=query) | Q(plot_no__mobile_number__icontains=query) 
                    | Q(plot_no__mail_id__icontains=query) | Q(project_name__project_name__icontains=query)
                    | Q(plot_no__first_name__icontains=first_name) | Q(plot_no__last_name__icontains=last_name)
                    | Q(plot_no__first_name__icontains=last_name) | Q(plot_no__last_name__icontains=first_name))
    return render(request, 'sites.html', {'QuerySet': QuerySet})

@login_required
def plot_details(request, pk):
    #query = New_registration.objects.filter(pk=pk)
    query = Document_details.objects.filter(pk=pk)
    query1 = PostImage.objects.filter(post__in=query)
    
    return render(request, 'details.html', {'query': query, 'query1':query1, 'media_url':settings.MEDIA_URL})

# 

def load_plot_nos(request):
    project_name_id = request.GET.get('projectId')
    plot_nos = Document_details.objects.raw('select * from api_document_details where api_document_details.project_name_id = %s', [project_name_id])
    return render(request, 'dropdown_list_options1.html',  {'plot_nos': plot_nos})


@login_required
def plotAvailability(request):
    return render(request, 'plot_availability.html')

# @api_view(['GET'])
# def getRoutes(request):
#     routes = []    
#     return Response(routes)

#@api_view(['GET'])
# def getNotes(request):
#     Notes = Note.objects.all()
#     serializer = NoteSerializer(Notes, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def newProject(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = NewProjectSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# getting projects list
# @api_view(['GET'])
# def projectList(request):
#     projects = New_Project.objects.all()
#     serializer = NewProjectSerializer(projects, many=True)
#     return Response(serializer.data)


#@csrf_exempt
# @api_view(['POST'])
# def newRegistration(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = NewRegistrationSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400) 

# @api_view(['GET'])
# def newRegistrationList(request):
#     registrations = New_registration.objects.all()
#     serializer = NewRegistrationSerializer(registrations, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def newDocuments(request):
#     if request.method == "POST":
#         data = JSONParser().parse(request, request.FILES)
#         serializer = NewDocumentSerializer(data=data)
#         files = request.FILES.getlist('document_files')
#         images = request.IMAGES.getlist('documents_images')
#         if serializer.is_valid():
#             serializer.save()
#             for f, i in files, images:
#                 data = post_image(post=serializer, documents_images=i, document_files=f)
#                 data.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
    
    
# @api_view(['GET'])
# def registrationList(request, pk):
#     registration = New_registration.objects.get(id=pk)
#     serializer = NewRegistrationSerializer(registration, many=False)
#     return Response(serializer.data)


#getting all documents details
# @api_view(['GET'])
# def documentsList(request):
#     documents = Document_details.objects.all()
#     serializer = NewDocumentSerializer(documents, many=True)
#     return Response(serializer.data)

# #getting the list of single document
# @api_view(['GET'])
# def documentList(request, pk):
#     document = Document_details.objects.get(id=pk)
#     serializer = NewDocumentSerializer(document, many=False)
#     return Response(serializer.data)


# @login_required
# def plotAmout(request):
#     if request.method == 'POST':
#         form = PlotAmountForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Thank you! Plot Account Was Successfully Created.',
#                              extra_tags='alert alert-success')
#         else:
#             print(form.errors)
#             messages.warning(request, 'Sorry, Something went wrong!', extra_tags='alert alert-warning') 
#     else:
#         form = PlotAmountForm()
#     return render(request, 'plotamount.html', {'form': form})

# @login_required
# def amountDetails(request):
#     PlotAmount.objects.filter(id=1).delete()
#     QuerySet = ''
#     query = request.GET.get('q', None)
#     if query:
#         first_name = query.split(' ')[0]
#         last_name  = query.split(' ')[0]
#         QuerySet = PlotAmount.objects.filter(Q(plot_no__plot_no__plot_no__icontains=query) |  Q(project_name__project_name__icontains=query)
#                     | Q(plot_no__plot_no__first_name__icontains=first_name) | Q(plot_no__plot_no__last_name__icontains=last_name)
#                     | Q(plot_no__plot_no__first_name__icontains=last_name) | Q(plot_no__plot_no__last_name__icontains=first_name))
#         # QuerySet = Document_details.objects.filter(Q(plot_no__plot_no__plot_no__icontains=query) | Q(plot_no__plot_no__mobile_number__icontains=query) 
#         #             | Q(plot_no__plot_no__mail_id__icontains=query) | Q(plot_no__project_name__project_name__icontains=query)
#         #             | Q(plot_no__plot_no__first_name__icontains=first_name) | Q(plot_no__plot_no__last_name__icontains=last_name)
#         #             | Q(plot_no__plot_no__first_name__icontains=last_name) | Q(plot_no__plot_no__last_name__icontains=first_name))
#     # queries = PlotAmount.objects.raw('select * from api_plotamount where api_plotamount.plot_no = %s', [QuerySet])
#     # queries = PlotAmount.objects.filter(id='QuerySet.id')
#     query = PlotAmount.objects.all()
#     return render(request, 'amount_details.html', {'QuerySet': QuerySet})