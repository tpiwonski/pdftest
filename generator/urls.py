from django.urls import path

from . import views

urlpatterns = [
    path('pdfkit/', views.test, name='test_pdfkit'),
    path('', views.test_reportlab, name='test_reportlab')
]
