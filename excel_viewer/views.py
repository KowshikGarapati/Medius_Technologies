import os

import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, request
from django.shortcuts import redirect, render



def upload(request):
    #get the uploaded file and save it in database
    if request.method == 'POST':
      uploaded_file = request.FILES['uploaded_file']
      file_storing_system = FileSystemStorage()
      file_storing_system.save(uploaded_file.name, uploaded_file)
      #get name of the file
      filename = uploaded_file.name
      #get the url of the file
      file_url = file_storing_system.url(uploaded_file.name)  
      #know wheather the file is excel or csv
      #if csv file
      if uploaded_file.name.endswith('.csv'):
              df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, filename))

      #if excel file
      elif uploaded_file.name.endswith(('.xls', '.xlsx')):
              df = pd.read_excel(os.path.join(settings.MEDIA_ROOT, filename))

      #if neither csv nor excel file return upload page
      else:
              return HttpResponse(b"Invalid file type. Please upload a CSV or Excel file.")
          # Convert DataFrame to HTML table
      html_table = df.to_html()
          
      return render(request, 'file_uploaded.html', {'html_table': html_table,"tablename":filename})
    
    return render(request, 'upload_file.html')

