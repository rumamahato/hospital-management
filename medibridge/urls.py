"""
URL configuration for medibridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('payments/', include('payments.urls')),

    path('view_doctor/', view_doctor, name='view_doctor'),
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('edit_doctor/<int:pid>/', edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:pid>/', delete_doctor, name='delete_doctor'),

    path('recycle_doctor/<int:pid>/', recycle_doctor, name='recycle_doctor'),
    path('recycle_bin_doctor/', recycle_bin_doctor, name='recycle_bin_doctor'),
    path('restore_doctor/<int:pid>/', restore_doctor, name='restore_doctor'),
    path('delete_doctor_permanent/<int:pid>/', delete_doctor_permanent, name='delete_doctor_permanent'),



    path('add_patient/', add_patient, name='add_patient'),
    path('view_patient/', view_patient, name='view_patient'),
    path('edit_patient/<int:pid>/', edit_patient, name='edit_patient'),
    path('delete_patient/<int:pid>/', delete_patient, name='delete_patient'),

    path('recycle_patient/<int:pid>/', recycle_patient, name='recycle_patient'),
    path('recycle_bin_patient/', recycle_bin_patient, name='recycle_bin_patient'),
    path('restore_patient/<int:pid>/', restore_patient, name='restore_patient'),
    path('delete_patient_permanent/<int:pid>/', delete_patient_permanent, name='delete_patient_permanent'),

  
  

    path('add_appointment/', add_appointment, name='add_appointment'),
    path('view_appointment/', view_appointment, name='view_appointment'),
    path('edit_appointment/<int:pid>/', edit_appointment, name='edit_appointment'),
    path('delete_appointment/<int:pid>/', delete_appointment, name='delete_appointment'),
    path('recycle_appointment/<int:pid>/', recycle_appointment, name='recycle_appointment'),
    
    path('view_appointment/', view_appointment, name='view_appointment'),
    path('recycle_appointment/<int:pid>/', recycle_appointment, name='recycle_appointment'),
    path('recycle_appointment_view/', recycle_appointment_view, name='recycle_appointment_view'),
    path('restore_appointment/<int:pid>/', restore_appointment, name='restore_appointment'),
    path('delete_appointment_permanent/<int:pid>/',delete_appointment_permanent,name='delete_appointment_permanent'),
    
    
    path('add_medical_record/', add_medical_record, name='add_medical_record'),
    path('view_medical_record/',view_medical_record, name='view_medical_record'),
    path('edit_medical_record/<int:id>/', edit_medical_record, name='edit_medical_record'),
    path('delete_medical_record/<int:id>/', delete_medical_record, name='delete_medical_record'),


    # -------- Prescription --------
    path('add_prescription/', add_prescription, name='add_prescription'),
    path('view_prescription/<int:id>/',view_prescription, name='view_prescription'),

]





  




   
    

    


