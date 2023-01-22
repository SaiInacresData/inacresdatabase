from .models import New_Project, New_registration, Document_details
from django.shortcuts import get_object_or_404

def add_variable_to_context(request):
    data = New_Project.objects.all()
    #reg = data.new_registration_project_name.all()
    # reg = Document_details.objects.filter(project_name__in=data)
    return {
        'data': data, 
    }