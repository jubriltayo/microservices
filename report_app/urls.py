from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.generate_report, name='generate_report'),
    path('export/csv/', views.export_to_csv, name='export_to_csv'),
    path('export/excel/', views.export_to_excel, name='export_to_excel'),
]
