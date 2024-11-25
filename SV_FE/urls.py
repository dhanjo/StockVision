"""
URL configuration for SV_FE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from SV_App import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('run-script/', views.run_script, name='run_script'),
    path('run-mrf/',views.run_mrf ,name='run_mrf'),
    path('run-TM/',views.run_TM ,name='run_TM'),
    path('run-JS/',views.run_JS ,name='run_JS'),
    path('run-HD/',views.run_HD ,name='run_HD'),    
    path('run-RL/',views.run_RL ,name='run_RL'),
    path('fetch-mrf-data/', views.fetch_mrf_data, name='fetch_mrf_data'),
    path('fetch-rel-data/', views.fetch_rel_data, name='fetch_rel_data'),
    path('fetch-hdfc-data/', views.fetch_hdfc_data, name='fetch_hdfc_data'),
    path('fetch-tata-data/', views.fetch_tata_data, name='fetch_tata_data'),
    path('fetch-jindal-data/', views.fetch_jindal_data, name='fetch_jindal_data'),
]

