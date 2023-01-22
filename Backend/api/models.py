from django.db import models

# Create your models here.

    

# add new projects here
    
class New_Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.project_name

class Note(models.Model):
   
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]

# here we are creating first step of registration form 

class New_registration(models.Model):
    
    STATE = (
        ('AP', 'Andhra Pradesh'),
        ('TS', 'Telangana')
    )
    
    project_name = models.ForeignKey(New_Project, on_delete=models.CASCADE)
    plot_no = models.CharField(max_length=20, unique=False, blank=False, null=False)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    mail_id = models.EmailField(max_length=100, blank=False, null=False)
    mobile_number = models.BigIntegerField(("mobile number"), unique=True, blank=False, null=False)
    survey_no = models.CharField(max_length=50, blank=False, null=False)
    land_extent = models.CharField(max_length=150, blank=False, null=False)
    address = models.CharField(max_length=75, blank=True, null=True)
    community = models.CharField(max_length=75, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    district = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, choices=STATE)
    pincode = models.PositiveSmallIntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.plot_no
    
# here we are creating second step registration form details
    
class Document_details(models.Model):
    project_name = models.ForeignKey(New_Project, on_delete=models.CASCADE)
    plot_no = models.ForeignKey(New_registration, on_delete=models.CASCADE, related_name='plot_nos')
    katha_no = models.CharField(max_length=50)
    passbook_no = models.CharField(max_length=50)
    document_no = models.CharField(max_length=100, unique=True)
    aadhar_no = models.BigIntegerField(unique=True)
    # total_amount = models.PositiveIntegerField()
    # paid_amount = models.PositiveIntegerField(default=0)
    pass_photo = models.ImageField(upload_to='api/images/pass_photos')
    passbook_photo = models.ImageField(upload_to='api/images/passbook_photos')
    note = models.TextField(null=True,help_text='enter text here')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.project_name.project_name
    
class post_image(models.Model):
    post = models.ForeignKey(Document_details, default=None, on_delete=models.CASCADE)
    documents_images = models.ImageField(upload_to='api/images/document_images')
    document_files = models.FileField(upload_to='api/files', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.post.plot_no)
    
class PostImage(models.Model):
    post = models.ForeignKey(Document_details, default=None, on_delete=models.CASCADE)
    document_photos = models.FileField(upload_to = 'api/images/documents')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.post.plot_no)
    
class PlotAvailability(models.Model):
    project_name = models.ForeignKey(New_Project, on_delete=models.CASCADE)
    plot_no = models.CharField(max_length=20, unique=False, blank=False, null=False)
    land_extent = models.CharField(max_length=150, blank=False, null=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.plot_no)
    
class PlotAmount(models.Model):
    project_name = models.ForeignKey(New_Project, on_delete=models.CASCADE)
    plot_no = models.ForeignKey(Document_details, on_delete=models.CASCADE, related_name='plot_nos')
    add_amount = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.plot_no.plot_no)