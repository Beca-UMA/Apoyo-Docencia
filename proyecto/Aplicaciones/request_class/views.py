from genericpath import exists
import random as rand
from re import S
from django.shortcuts import render, redirect
from Aplicaciones.classroom.views import make_characteristic

from Aplicaciones.teacher.models import Teacher
from Aplicaciones.slot.models import Slot
from Aplicaciones.characteristic.models import Characteristic
from .models import RequestClass
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
import Aplicaciones.slot.utils as utils
from datetime import datetime

# Create your views here.


def index(request):
    requests_classes = RequestClass.objects.all()

    # Si se ha importado algún archivo
    if request.method == 'POST' and request.FILES:
        request_resource = RequestClassResource()
        dataset = Dataset()
        new_request = request.FILES['myfile']

        if not new_request.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'index_requests.html', {"requests": requests_classes, "format": True})
        imported_data = dataset.load(new_request.read(), format='xlsx')
        num = 0
        
        for data in imported_data:
            id = data[0]
            typ = data[1]
            preference = data[2]
            if typ == "Cancelación solicitud":
                list_request_class = RequestClass.objects.filter(
                      code=preference)
                for r in list_request_class:
                    r.delete()
            else:
                name_period = data[3]
                degree = data[4]
                subject = data[5]
                grade = data[6]
                letter = data[7]
                code = data[8] + "-" + subject[0]  # A1-P
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
                    specification = 'No especificado'
                num_alum = data[21]
                s_o = data[22]
                specialization = data[23]

                    # Buscamos al profesor que la va a impartir y quien la reclama
                q = Teacher.objects.filter(email=email)
                if not q.exists():
                    sender = Teacher(name=name_sender, phone=phone,
                                         email=email, department=department)
                    sender.save()
                else:
                    sender = Teacher.objects.get(email=email)
                    teacher = Teacher.objects.get(name=name_teacher)

                    # Buscamos o creamos al subgrupo
                q = SmallGroup.objects.filter(code=code)
                if not q.exists():
                    small_group = SmallGroup(
                        subject=subject, grade=grade, letter=letter, code=code, degree=degree)
                    small_group.save()  # Lo guarda y si no lo actualiza
                else:
                    small_group = SmallGroup.objects.get(code=code)

                    # Buscamos o creamos el periodo
                year = data[14][-4]

                q = Period.objects.filter(year=year, typ=name_period)
                if not q.exists():
                    period = Period(year=year, typ=name_period)
                    period.save()  # Lo guarda y si no lo actualiza
                else:
                    period = Period.objects.get(year=year, typ=name_period)

                    value = RequestClass(code=id, typ=typ, preference=preference, location=location,
                                         specification=specification, num_alum=num_alum, s_o=s_o,
                                         specialization=specialization, start_date=start_date, end_date=end_date,
                                         alternative_day=alternative_day, start_hour=start_hour, end_hour=end_hour,
                                         imparter=teacher, sender=sender, per=period, s_g=small_group
                                         )
                    value.save()
                num = num+1
        return render(request, 'index_requests.html', {"requests": requests_classes, "success": True, "num": num})

    if request.method == 'POST' and not request.FILES:
        return render(request, 'index_requests.html', {"requests": requests_classes, "missing": True})

    # Por defecto
    return render(request, "index_requests.html", {"requests": requests_classes})


def asignationRequest(request):
    Slot.objects.all().delete()
    utils.main()
    return redirect("/slots")


def make_characteristic(request, characteristic, numeric):
    if numeric == True:
        q = Characteristic.objects.filter(name__gte=characteristic)
        if not q.exists():
            c = Characteristic(name=characteristic,
                               numeric=numeric, applicnat=request)
            c.save()
        else:
            for charc in q.iterator():
                charc.applicant = request
                charc.save()

    else:
        q = Characteristic.objects.filter(name=characteristic)
        if not q.exists():
            c = Characteristic(name=characteristic,
                               numeric=numeric, applicnat=request)
            c.save()
        else:
            c = Characteristic.objects.get(name=characteristic)
            c.applicant = request
            c.save()


def createRequestClass(request):
    while True:
        id = rand.randint(1000, 9999)
        r = RequestClass.objects.filter(code=id)
        if not r.exists():
            break
    return render(request, "createRequest.html", {"id": id})


def showRequest(request, key):
    r = RequestClass.objects.get(key=key)
    return render(request, "showRequest.html", {"request": r})


def editRequest(request, key):
    request_class = RequestClass.objects.get(key=key)

    return render(request, "editRequest.html", {"r": request_class, request_class.s_o + "_sel": "selected",
                                                request_class.s_g.degree[-3] + "_sel": "selected", request_class.alternative_day[0:2] + "_sel": "selected"})


def updateRequest(request):
    id = request.POST.get('code_request')
    typ = request.POST.get('typ')
    preference = request.POST.get('preference')
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
        specification = 'No especificado'
    num_alum = request.POST.get('num_alum')
    s_o = request.POST.get('s_o')
    specialization = request.POST.get('specialization')

    value = RequestClass.objects.get(
        code=id, typ=typ, preference=preference, alternative_day=alternative_day)
    # Buscamos al profesor que la va a impartir y quien la reclama
    q = Teacher.objects.filter(name=name_teacher)
    if not q.exists():
        imparter = Teacher(name=name_sender, phone=phone,
                           email=email, department=department)
        imparter.save()
        value.imparter = imparter

        # Buscamos o creamos al subgrupo

    q = SmallGroup.objects.filter(
        letter=letter, code=code_group, subject=subject)
    if not q.exists():
        small_group = SmallGroup(
            subject=subject, grade=grade, letter=letter, code=code_group, degree=degree)
        small_group.save()  # Lo guarda y si no lo actualiza
        value.s_g = small_group
    else:
        s = SmallGroup.objects.get(code=code_group)
        value.sg = s

        # Buscamos o creamos el periodo
    year = start_date[-4]

    q = Period.objects.filter(year=year, typ=name_period)
    if not q.exists():
        period = Period(year=year, typ=name_period)
        period.save()  # Lo guarda y si no lo actualiza
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
        value.specification = 'No especificado'
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
    preference = "Preferente"
    degree = request.POST['degree']
    name_period = request.POST['name_period']
    subject = request.POST['subject']
    grade = request.POST['grade']
    letter = request.POST['letter']
    code = request.POST['code'] + "-" + subject[0]  # A1-P
    name_teacher = request.POST['name_teacher']
    name_sender = request.POST['name_sender']
    phone = request.POST['phone']
    email = request.POST['email']
    department = request.POST['department']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    alternative_day = request.POST['pref_day']
    start_hour = request.POST['start_hour']
    end_hour = request.POST['end_hour']
    location = request.POST['location']
    specification = request.POST['specification']
    if specification is None:
        specification = 'No especificado'
    num_alum = request.POST['num_alum']
    s_o = request.POST['s_o']
    specialization = request.POST['specialization']

    imp = Teacher.objects.filter(name=name_teacher)
    if not imp.exists():
        imparter = Teacher(name=name_sender, phone=phone,
                               email=email, department=department)
        imparter.save()
    else:
        for i in imp.iterator():
            imparter = i

    send = Teacher.objects.filter(name=name_sender)
    if not send.exists():
        sender = Teacher(name=name_sender, phone=phone,
                         email=email, department=department)
        sender.save()
    else:
        for i in send.iterator():
            sender = i

    q = SmallGroup.objects.filter(code=code)
    if not q.exists():
        small_group = SmallGroup(
                        subject=subject, grade=grade, letter=letter, code=code, degree=degree)
        small_group.save()  # Lo guarda y si no lo actualiza
    else:
        small_group = SmallGroup.objects.get(code=code)

        # Buscamos o creamos el periodo
    year = start_date[-4]
    period = Period(year=year, typ=name_period)
    period.save()  # Lo guarda y si no lo actualiza

    RequestClass.objects.create(code=id, typ=typ, preference=preference, location=location,
                                    specification=specification, num_alum=num_alum, s_o=s_o,
                                    specialization=specialization, start_date=start_date, end_date=end_date,
                                    alternative_day=alternative_day, start_hour=start_hour, end_hour=end_hour,
                                    imparter=imparter, sender=sender, per=period, s_g=small_group)

    if request.POST['start_date_alt']:
        id = request.POST['id']
        typ = request.POST['typ']
        preference = "Alternativo"
        degree = request.POST['degree']
        name_period = request.POST['name_period']
        subject = request.POST['subject']
        grade = request.POST['grade']
        letter = request.POST['letter']
        code = request.POST['code'] + "-" + subject[0]  # A1-P
        name_teacher = request.POST['name_teacher']
        name_sender = request.POST['name_sender']
        phone = request.POST['phone']
        email = request.POST['email']
        department = request.POST['department']
        start_date = request.POST['start_date_alt']
        end_date = request.POST['end_date_alt']
        alternative_day = request.POST['alternative_day']
        start_hour = request.POST['start_hour_alt']
        end_hour = request.POST['end_hour_alt']
        location = request.POST['location']
        specification = request.POST['specification']
        if specification is None:
            specification = 'No especificado'
        num_alum = request.POST['num_alum']
        s_o = request.POST['s_o']
        specialization = request.POST['specialization']

        imp = Teacher.objects.filter(name=name_teacher)
        if not imp.exists():
            imparter = Teacher(name=name_sender, phone=phone,
                                email=email, department=department)
            imparter.save()
        else:
            for i in imp.iterator():
                imparter = i

        send = Teacher.objects.filter(name=name_sender)
        if not send.exists():
            sender = Teacher(name=name_sender, phone=phone,
                            email=email, department=department)
            sender.save()
        else:
            for i in send.iterator():
                sender = i

            # Buscamos o creamos al subgrupo
        small_group = SmallGroup(
                subject=subject, grade=grade, letter=letter, code=code, degree=degree)
        small_group.save()  # Lo guarda y si no lo actualiza

            # Buscamos o creamos el periodo
        year = start_date[-4]
        q = Period.objects.filter(year=year, typ=name_period)
        if not q.exists():
            period = Period(year=year, typ=name_period)
            period.save()  # Lo guarda y si no lo actualiza
        else:
            period = Period.objects.get(year=year, typ=name_period)

        RequestClass.objects.create(code=id, typ=typ, preference=preference, location=location,
                                        specification=specification, num_alum=num_alum, s_o=s_o,
                                        specialization=specialization, start_date=start_date, end_date=end_date,
                                        alternative_day=alternative_day, start_hour=start_hour, end_hour=end_hour,
                                        imparter=imparter, sender=sender, per=period, s_g=small_group)

    return redirect('/requests/')

def deleteRequests(request):
    RequestClass.objects.all().delete()
    return redirect("/requests")

def search(request):
    if request.POST['search']:
        id = request.POST['search']
        requests_classes = RequestClass.objects.filter(code=id)
        return render(request, 'index_requests.html', {"requests": requests_classes, "search":id})
    else:
        requests_classes = RequestClass.objects.all()
        return render(request, 'index_requests.html', {"requests": requests_classes})