from django.shortcuts import render
from . models import Table
from django.http import HttpResponse
from django.contrib import messages
import csv
import json
import pandas as pd
# Create your views here.
def hi(request):
    return render(request,'home/main.html')

def input(request):
    if request.method == 'POST' and request.FILES.get('filename'):
        name = request.POST["First Name"]
        doc_name = request.FILES["filename"]
        file_data = doc_name.read().decode("utf-8")
        lines = file_data.split("\n")[1:-1]
        heading = file_data.split("\n")[:1]
        head = heading[0].split(",")
        for line in lines:
            fields = line.split(",")
            if fields:
                d={}
                for i in range(len(fields)):
                    if head[i].lower()[:-1] == 'password':
                        d[head[i]] = encode(fields[i][:-1])
                    else:
                        d[head[i]] = fields[i]
                table = Table.objects.create(Name="krithik",data=d)

    return render(request,'home/main.html')

def export(request):
    if request.method=='POST':
        name = request.POST["Name"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Yourfile.csv"'
        writer = csv.writer(response)
        count = 0
        queryset = Table.objects.filter(Name=name)
        for obj in queryset:
            for field in obj._meta.fields:
                if obj._meta.get_field(field.name).get_internal_type() == 'JSONField':
                    detail = json.dumps(getattr(obj, field.name))
                    detail_parsed = json.loads(str(detail))
                    keys = []
                    values = []
                    for key, value in detail_parsed.items():
                        if key.lower()[:-1] == 'password':
                            keys.append(key)
                            values.append(decode(value))
                        else:
                            keys.append(key)
                            values.append(value)
                    if count == 0:
                        writer.writerow(keys)
                        count += 1
                    writer.writerow(values)
    return response

def encode(passw):
    return "".join([chr(ord(i) + len(passw)) for i in passw])

def decode(password):
    return "".join([chr(ord(i) - len(password)) for i in password])




