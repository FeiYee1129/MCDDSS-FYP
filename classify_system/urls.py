from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    url(r'^registerS/$', views.registerS, name='registerS'),
    url(r'^registerD/$', views.registerD, name='registerD'),
    url(r'^home/$', views.dashboard, name='dashboard'),
    url(r'^about/$', views.aboutPage, name='about'),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^post_login/$', views.post_login, name='post_login'),
    url(r'^postRegisterS/$', views.postRegisterS, name='postRegisterS'),
    url(r'^postRegisterD/$', views.postRegisterD, name='postRegisterD'),
    url(r'^profile/$', views.viewProfile, name='viewProfile'),
    url(r'^profile/edit/$', views.updateProfile, name='updateProfile'),
    url(r'^patient_list/$', views.listPatient, name='listPatient'),
    url(r'^patient_list/search/$', views.search, name='search'),
    path('patient_list/patient_profile/<str:pid>', views.viewPatient, name='viewPatient'),
    url(r'^patient_list/patient_profile/addScreening/$', views.addScreening, name='addScreening'),
    url(r'^patient_list/patient_profile/edit/$', views.updatePatient, name='updatePatient'),
    url(r'^addPatient/$', views.addPatient, name='addPatient'),
    url(r'^post_addPatient/$', views.post_addPatient, name='post_addPatient'),
    path('patient_list/delete/<str:pid>', views.delete, name="delete"),
    url(r'^showStatistical/$', views.showStatistical, name='showStatistical'),
    url(r'^patient_list/classifier_home/$', views.classifier_home, name='classifier_home'),
    path('patient_list/patient_profile/classifier_home/<str:pid>/<str:dt>', views.classifier, name="classifier"),
]

urlpatterns + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)