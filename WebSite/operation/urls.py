from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$',views.main,name='main'),
    url(r'^refresh/',views.refresh,name='refresh'),
    url(r'^command/',views.command,name='command'),
    url(r'^analogcommand/',views.analogcommand,name='analogcommand'),
    url(r'^exportcsv/',views.exportcsv,name='exportcsv')
]