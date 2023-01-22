from .models import Note, New_Project, New_registration, Document_details, PlotAmount
from django import forms
from django.forms import fields

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        
class NewProjectForm(forms.ModelForm):
    class Meta:
        model = New_Project
        fields = ['project_name']
        
class NewRegistrationForm(forms.ModelForm):
    class Meta:
        model = New_registration
        fields = ['project_name', 'plot_no', 'first_name', 'last_name', 'mail_id', 'mobile_number', 'survey_no', 'land_extent', 'address','community', 'city', 'district', 'state', 'pincode']
        


class NewDocumentForm(forms.ModelForm):
    class Meta:
        model = Document_details
        fields = ['project_name', 'plot_no', 'katha_no', 'passbook_no', 'aadhar_no', 'document_no', 'pass_photo', 'passbook_photo', 'note']
        
class DocumentImageForm(NewDocumentForm):
    document_photos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta(NewDocumentForm.Meta):
        fields = (NewDocumentForm.Meta.fields + ['document_photos',])
        
class PlotAmountForm(forms.ModelForm):
    class Meta:
        model = PlotAmount
        fields = '__all__'