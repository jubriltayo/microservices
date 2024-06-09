from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas as pd
from io import BytesIO
from .models import Report


def generate_report(request):
    reports = Report.objects.all()
    return render(request, 'report_list.html', {'reports': reports})

def export_to_csv(request):
    reports = Report.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Content', 'Created At'])

    for report in reports:
        writer.writerow([report.title, report.content, report.created_at])
    
    return response

def export_to_excel(request):
    reports = Report.objects.all()
    data = {
        'Title': [report.title for report in reports],
        'Content': [report.content for report in reports],
        'Created At': [report.created_at.replace(tzinfo=None) for report in reports],
    }

    df = pd.DataFrame(data)

    # use BytesIO buffer to write the excel file 
    # This is necessary bcos without it pandas overwrites the 
    # header's Content-Dispositon and filename = 'download.xlsx'
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')

    # set buffer position to the beginning
    buffer.seek(0)

    # create HTTP response with correct content type 
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Dispostion'] = 'attachment; filename="reports.xlsx"'

    return response