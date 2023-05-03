from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('technicalhome/', views.technicalhome, name='technicalhome'),
    path('marketinghome/', views.marketinghome, name='marketinghome'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('technicalregister/', views.technicalregister_user, name='technicalregister'),
    path('lead/<int:pk>', views.customer_lead, name='lead'),
    path('technical_update_lead/<int:pk>', views.technical_update_lead, name='technical_update_lead'),
    path('adminlead/<int:pk>', views.adminlead, name='adminlead'),
    path('delete_lead/<int:pk>', views.delete_lead, name='delete_lead'),
    path('admin_delete_lead/<int:pk>', views.admin_delete_lead, name='admin_delete_lead'),
    path('add_lead/', views.add_lead, name='add_lead'),
    path('update_lead/<int:pk>', views.update_lead, name='update_lead'),
    path('technical_lead/<int:pk>', views.technical_lead, name='technical_lead'),
    path('admin_update_lead/<int:pk>', views.admin_update_lead, name='admin_update_lead'),

]
