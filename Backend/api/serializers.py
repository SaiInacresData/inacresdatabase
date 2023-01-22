from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Note, New_Project, New_registration, Document_details

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        
class NewProjectSerializer(ModelSerializer):
    class Meta:
        model = New_Project
        fields = ['project_name']
        
class NewRegistrationSerializer(ModelSerializer):
    project_name = serializers.SlugRelatedField(slug_field='project_name', read_only=True)
    class Meta:
        model = New_registration
        fields = ['project_name', 'plot_no', 'first_name', 'last_name', 'mail_id', 'mobile_number', 'survey_no', 'land_extent', 'address','community', 'city', 'district', 'state', 'pincode']
        

class NewDocumentSerializer(ModelSerializer):
    
    class Meta:
        model = Document_details
        fields = ['project_name', 'plot_no', 'katha_no', 'passbook_no', 'aadhar_no', 'document_no', 'pass_photo', 'passbook_photo', 'note']

class DocumentImageSerializer(NewDocumentSerializer):
    documents_images = serializers.ListField(child=serializers.ImageField(max_length=100000, use_url=False))
    document_files = serializers.ListField(child=serializers.FileField(max_length=100000, use_url=False))
    def create(self, validated_data):
        documents_images = validated_data.pop('documents_images')
        document_files = validated_data.pop('document_files')
        for image, files in documents_images, document_files:
            f = Document_details.objects.create(documents_images=image,document_files=files, **validated_data)
        return f
   
    
    class Meta(NewDocumentSerializer.Meta):
        fields = [NewDocumentSerializer.Meta.fields + ['documents_images','document_files',]]
        
