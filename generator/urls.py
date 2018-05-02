from django.urls import path

from . import views

urlpatterns = [
    path('pdfkit/', views.test_pdfkit, name='test_pdfkit'),
    path('', views.test_reportlab, name='test_reportlab')
]
