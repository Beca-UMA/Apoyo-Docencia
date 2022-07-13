from re import S
from django.shortcuts import render, redirect

from Aplicaciones.teacher.models import Teacher
from .models import  RequestClass
from .resources import RequestClassResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
from Aplicaciones.teacher.models import Teacher
from Aplicaciones.small_group.models import SmallGroup
from Aplicaciones.period.models import Period
from datetime import datetime

# Create your views here.
def index(request):
    requests_classes = RequestClass.objects.all()

    ## Si se ha importado algún archivo
    if request.method == 'POST':
        request_resource = RequestClassResource()
        dataset = Dataset()
        new_request = request.FILES['myfile']

        if not new_request.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'index_requests.html', {"requests": requests_classes})
        imported_data = dataset.load(new_request.read(), format='xlsx')

        for data in imported_data:
            print(data)
            id = data[0]
            typ = data[1]
            preference = data[2]
            if typ == "Cancelación solicitud":
                list_request_class = RequestClass.objects.filter(code=preference)
                for r in list_request_class:
                    r.delete()
            else:
                name_period = data[3]
                degree = data[4]
                subject = data[5]
                grade = data[6]
                letter = data[7]
                code = data[8] + "-" + subject[0] # A1-P
                name_teacher = data[9]
                name_sender = data[10]
                phone = data[11]
                email = data[12]
                department = data[13]
                start_date = datetime.strptime(data[14], '%d/%m/%Y')
                end_date = datetime.strptime(data[15], '%d/%m/%Y')
                alternative_day = data[16]
                start_hour = data[17]
                end_hour = data[18]
                location = data[19]
                specification = data[20]
                if specification is None:
                    specification = 'No specificated'
                num_alum = data[21]
                s_o = data[22]
                specialization = data[23]

                # Buscamos al profesor que la va a impartir y quien la reclama
                teachers = Teacher.objects.all()
                q = Teacher.objects.filter(email=email)
                if not q.exists():
                    sender = Teacher(name=name_sender, phone=phone, email=email,department=department)
                    sender.save() 
                else:
                    sender = Teacher.objects.get(email=email)
                teacher = Teacher.objects.get(name=name_teacher)

                # Buscamos o creamos al subgrupo
                
                q = SmallGroup.objects.filter(code = code)
                if not q.exists():
                    small_group = SmallGroup(subject=subject, grade=grade, letter=letter, code=code, degree=degree)
                    small_group.save() #Lo guarda y si no lo actualiza
                else:
                    small_group = SmallGroup.objects.get(code=code)

                # Buscamos o creamos el periodo
                year = data[14][-4:]
                
                q = Period.objects.filter(year=year, typ=name_period)
                if not q.exists():
                    period = Period(year=year,typ=name_period)
                    period.save() #Lo guarda y si no lo actualiza
                else:
                    period = Period.objects.get(year=year, typ=name_period)



                q = RequestClass.objects.filter(code=id, typ=typ, preference=preference)
                if not q.exists():
                    value = RequestClass( code=id, typ=typ, preference=preference, location=location,
                                    specification=specification, num_alum=num_alum, s_o=s_o,
                                    specialization=specialization, start_date=start_date, end_date= end_date,
                                    alternative_day=alternative_day, start_hour=start_hour, end_hour=end_hour,
                                    imparter=teacher, sender=sender, per=period, s_g=small_group
                    )       
                    value.save()
                else:
                    value = RequestClass.objects.get(code=id, typ=typ, preference=preference)
                    value.name_period = data[3]
                    value.degree = data[4]
                    value.subject = data[5]
                    value.grade = data[6]
                    value.letter = data[7]
                    # value.code2 = data[8] + "-" + subject[0] # A1-P
                    # value.name_teacher = data[9]
                    # value.name_sender = data[10]
                    # value.phone = data[11]
                    # value.email = data[12]
                    value.department = data[13]
                    value.start_date = datetime.strptime(data[14], '%d/%m/%Y')
                    value.end_date = datetime.strptime(data[15], '%d/%m/%Y')
                    value.alternative_day = data[16]
                    value.start_hour = data[17]
                    value.end_hour = data[18]
                    value.location = data[19]
                    value.specification = data[20]
                    if value.specification is None:
                        value.specification = 'No specificated'
                    value.num_alum = data[21]
                    value.s_o = data[22]
                    value.specialization = data[23]
                    value.save()
                
                print(f"VALOR:::::: {teacher.id}")
                print(f"VALOR:::::: {sender.id}")
                print(f"VALOR:::::: {period.id}")
                print(f"VALOR:::::: {small_group.id}")
                

    ## Por defecto
    return render(request, "index_requests.html", {"requests": requests_classes})



def createRequestClass(request):
    return render(request, "createRequest.html")  

def showRequest(request,key):
    r = RequestClass.objects.get(key=key)
    return render(request, "showRequest.html", {"request":r}) 

def editRequest(request, key):
    request_class = RequestClass.objects.get(key=key)
    print(f"TIPO::::::::::::::.{type(request_class.start_hour)}")
    return render(request, "editRequest.html", {"request":request_class})

def updateRequest(request):
    id = request.POST.get('code_request')
    typ = request.POST.get('typ')
    preference = request.POST.get('preference')
    if typ == "Cancelación solicitud":
        list_request_class = RequestClass.objects.filter(id=preference)
        for r in list_request_class:
            r.delete()
        return redirect('/requests/')
    else:
        degree = request.POST.get('degree')
        name_period = request.POST.get('name_period')
        subject = request.POST.get('subject')
        grade = request.POST.get('grade')
        letter = request.POST.get('letter')
        code_group = request.POST.get('group')
        name_teacher = request.POST.get('name_teacher')
        name_sender = request.POST.get('name_sender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        department = request.POST.get('department')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        alternative_day = request.POST.get('alternative_day')
        start_hour = request.POST.get('start_hour')
        end_hour = request.POST.get('end_hour')
        location = request.POST.get('location')
        specification = request.POST.get('specification')
        if specification is None:
            specification = 'No specificated'
        num_alum = request.POST.get('num_alum')
        s_o = request.POST.get('s_o')
        specialization = request.POST.get('specialization')


        value = RequestClass.objects.get(code=id, typ=typ, preference=preference)
        # Buscamos al profesor que la va a impartir y quien la reclama
        q = Teacher.objects.filter(name=name_teacher)
        if not q.exists():
            imparter = Teacher(name=name_sender, phone=phone, email=email,department=department)
            imparter.save() 
            value.imparter = imparter

        # Buscamos o creamos al subgrupo
        
        q = SmallGroup.objects.filter(letter=letter, code=code_group, subject=subject)
        if not q.exists():
            small_group = SmallGroup(subject=subject, grade=grade, letter=letter, code=code_group, degree=degree)
            small_group.save() #Lo guarda y si no lo actualiza
            value.s_g = small_group
        else:
            s = SmallGroup.objects.get(code = code_group)
            value.sg = s

        # Buscamos o creamos el periodo
        year = start_date[:4]
        
        q = Period.objects.filter(year=year, typ=name_period)
        if not q.exists():
            period = Period(year=year,typ=name_period)
            period.save() #Lo guarda y si no lo actualiza
            value.per = period
        else:
            p = Period.objects.get(year=year, typ=name_period)
            value.per = p

        

        value.start_date = start_date
        value.end_date = end_date
        value.alternative_day = alternative_day
        value.start_hour = start_hour
        value.end_hour = end_hour
        value.location = location
        value.specification = specification
        if value.specification is None:
            value.specification = 'No specificated'
        value.num_alum = num_alum
        value.s_o = s_o
        value.specialization = specialization
        value.save()
        return redirect('/requests/')


def removeRequest(request, key):
    request_class = get_object_or_404(RequestClass, key=key)
    request_class.delete()
    return redirect('/requests/')

def importRequest(request):
    None


def newRequestClass(request):
    id = request.POST['id']
    typ = request.POST['typ']
    preference = request.POST['preference']
    if typ == "Cancelación solicitud":
        list_request_class = RequestClass.objects.filter(id=preference)
        for r in list_request_class:
            r.delete()
        return redirect('/')
    else:
        degree = request.POST['degree']
        name_period = request.POST['name_period']
        subject = request.POST['subject']
        grade = request.POST['grade']
        letter = request.POST['letter']
        code = request.POST['code'] + "-" + subject[0] # A1-P
        name_teacher = request.POST['name_teacher']
        name_sender = request.POST['name_sender']
        phone = request.POST['phone']
        email = request.POST['email']
        department = request.POST['department']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        alternative_day = request.POST['alternative_day']
        start_hour = request.POST['start_hour']
        end_hour = request.POST['end_hour']
        location = request.POST['location']
        specification = request.POST['specification']
        if specification is None:
            specification = 'No specificated'
        num_alum = request.POST['num_alum']
        s_o = request.POST['s_o']
        specialization = request.POST['specialization']

        # Buscamos al profesor que la va a impartir y quien la reclama
        teacher = Teacher.objects.get(name=name_teacher)
        sender = Teacher(name=name_sender, phone=phone, email=email,department=department)
        sender.save() #Lo guarda y si no lo actualiza

        # Buscamos o creamos al subgrupo
        small_group = SmallGroup(subject=subject, grade=grade, letter=letter, code=code, degree=degree)
        small_group.save() #Lo guarda y si no lo actualiza

        # Buscamos o creamos el periodo
        year = start_date[-4:]
        period = Period(year=year,typ=name_period)
        period.save() #Lo guarda y si no lo actualiza

        RequestClass.objects.create(id=id, typ=typ, preference=preference, location=location,
                                        specification=specification, num_alum=num_alum, s_o=s_o,
                                        specialization=specialization, start_date=start_date, end_date= end_date,
                                        alternative_day=alternative_day, start_hour=start_hour, end_hour=end_hour,
                                        teacher=teacher, sender=sender, period=period)
        return redirect('/')