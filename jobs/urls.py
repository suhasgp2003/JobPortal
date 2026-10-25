from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_list, name='job_list'),  
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('create/', views.create_job, name='create_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('<int:job_id>/apply/', views.apply_to_job, name='apply_job'),
    path('applications/<int:job_id>/', views.view_applications, name='applications'),



]
