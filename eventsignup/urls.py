from django.urls import path

from . import views
app_name='eventsignup'
urlpatterns = [
    # näytä tervetuloa ja ohjaa sisäänkirjautumiseen
    path('', views.index, name='index'),
    # uuden tapahtuman lisääminen
    path('event/new/', views.new, name='new'),
    # sivupaneelin "nippelitieto"
    path('event/<int:uid>/stats/', views.stats, name='stats'),
     # tapahtuman info
    path('event/<int:uid>/info/', views.info, name='info'),
    # tapahtumaan osallistujan ilmoittautumislomake
    path('event/<int:uid/signup/', views.signup, name='signup'),
    # Arkistoi tapahtuman
    path('event/<int:uid/archive/', views.archive, name='archive'),

]