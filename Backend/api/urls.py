from django.urls import path
from . import views
from .views import RegUpdateView, RegDelView, DocUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.forms.widgets import Media
from django.contrib.auth import views as auth_views
app_name = 'api'

urlpatterns = [
    # path('', views.getRoutes, name='routes'),
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('Notes/', views.getNotes, name='notes'),
    path('NewProject/', views.newProject, name='newproject'),
    # path('ProjectList/', views.projectList, name='projectlist'),
    path('NewReg/', views.newRegistration, name='newReg'),
    path('Reg/edit/<int:pk>', views.RegUpdateView.as_view(), name="regupdate"),
    path('<int:pk>/delete/', views.RegDelView.as_view(), name='regdelete'),
    # path('RegLists/', views.newRegistrationList, name='reglists'),
    # path('RegList/<str:pk>', views.registrationList, name='reglist'),
    path('NewDoc/', views.newDocuments, name='newdoc'),
    path('Doc/edit/<int:pk>', views.DocUpdateView.as_view(), name='docupdate'),
    path('user_details/', views.user_details, name='user_details'),
    # path('DocLists/', views.documentsList, name='docslist'),
    # path('DocList/<str:pk>', views.documentList, name='doclist')    
    path('sites/', views.sites, name='sites'),
    path('details/<int:pk>', views.plot_details, name='details'),
    path('ajax/load-plot_nos/', views.load_plot_no, name='ajax_load_plot_no'),
    path('ajax/load-plot-no/', views.load_plot_nos, name='ajax_load_plot_nos'),
    #path('plotAmount/', views.plotAmout, name='plotamount'),
    #path('amount_details/', views.amountDetails, name='Adetails'),
    path('plotAvailablilty/', views.plotAvailability, name='plotavailability')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
