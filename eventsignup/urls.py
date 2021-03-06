from django.urls import path


from . import views
app_name = 'eventsignup'
urlpatterns = [
    # näytä tervetuloa ja ohjaa sisäänkirjautumiseen
    path('', views.index, name='index'),
    # hallintakonsoli
    path('management', views.management, name='management'),
    # kiitossivu
    path('thanks/<int:type>', views.thanks, name='thanks'),
    path('thanks', views.thanks, name='thanks'),
    # Ilmoittautuminen epäonnistui (koska max osallistujia jo) sivu
    path('failed', views.failed, name='failed'),
    # uuden tapahtuman lisäyslomake & dropdown menu
    path('event/add/<str:type>', views.add, name='add'),
    path('event/add/', views.formtype, name='formtype'),
    # sivupaneelin "nippelitieto"
    path('event/<int:uid>/stats/', views.stats, name='stats'),
    # preview uuden tapahtuman luomisen jälkeen
    path('event/<int:uid>/preview/<str:type>', views.preview, name='preview'),
    path('event/<int:uid>/preview/', views.preview, name='preview'),
    # tapahtuman info
    path('event/<int:uid>/view/<str:type>', views.info, name='view'),
    path('event/<int:uid>/view/', views.info, name='view'),
    # tapahtuman muokkaus
    path('event/<int:uid>/edit/', views.edit, name='edit'),
    # tapahtuman osallistujalistan muokkaus
    path('event/<int:uid>/edit/<str:type>/', views.edit, name='edit'),
    # tapahtumaan osallistujan ilmoittautumislomake
    path('event/<int:uid>/signup/', views.signup, name='signup'),
    # Poistaa (=Arkistoi) tapahtuman
    path('event/<int:uid>/delete/', views.archive, name='archive'),
    # osallistujalistan exporttaus
    path('event/<int:uid>/export/', views.export, name='export'),
    # Näyttää tietosuojainfon
    path('privacy', views.privacy, name='privacy'),

]
