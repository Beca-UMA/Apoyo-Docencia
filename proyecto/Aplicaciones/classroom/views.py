from unicodedata import numeric
from django.shortcuts import render, redirect

from Aplicaciones.characteristic.models import Characteristic
from .models import Classroom
from .resources import ClassromResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

# Create your views here.
def index(request):
    clases = Classroom.objects.all()

    ## Si se ha importado algún archivo
    if request.method == 'POST':
        classroom_resource = ClassromResource()
        dataset = Dataset()
        new_classroom = request.FILES['myfile']

        if not new_classroom.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'index.html', {"clases": clases})
        imported_data = dataset.load(new_classroom.read(), format='xlsx')
        for data in imported_data:
            print(data)
            if data[0] == None:
                break
            num_class = data[0]
            location = data[1]
            capacity = data[2]
            num_pc = data[3]
            s_o = data[4]
            specification = data[5]
            specialization = ''
            if specification is None:
                specification = 'Not specificated'
            value = Classroom(num_class=num_class, specification=specification,
                            location=location,num_pc=num_pc, s_o=s_o,
                            capacity=capacity,specialization=specialization)
            value.save()
            make_characteristic(value,value.location,False)
            make_characteristic(value,value.s_o,False)
            make_characteristic(value,value.num_pc,True)
            if specification is not 'Not specificated':
                make_characteristic(value,value.specification,False)


    ## Por defecto
    return render(request, "index.html", {"clases": clases})


def make_characteristic(classroom, characteristic, numeric):
    q = Characteristic.objects.filter(name=characteristic)
    if not q.exists():
        c = Characteristic(name=characteristic, numeric=numeric, classroom=classroom)
        c.save()
    else:
        c = Characteristic.objects.get(name=characteristic)
        c.classroom=classroom
        c.save()

def newClassroom(request):
    num_class = request.POST['id_num_class']
    location = request.POST['id_location']
    s_o = request.POST['id_s_o']
    num_pc = request.POST['id_num_pc']
    capacity = request.POST['id_capacity']
    specialization = request.POST['id_specialization']
    specification = request.POST['id_specification']

    Classroom.objects.create(num_class=num_class, specification=specification,location=location,num_pc=num_pc, s_o=s_o, capacity=capacity,specialization=specialization )

    return redirect('/')

def createClassroom(request):
    return render(request, "createClassroom.html")  

def editClassroom(request, num_class, location):
    clase = Classroom.objects.get(num_class=num_class, location=location)
    return render(request, "editClassroom.html", {"clase":clase})

def updateClassroom(request):
    num_class = request.POST['id_num_class']
    location = request.POST['id_location']
    s_o = request.POST['id_s_o']
    num_pc = request.POST['id_num_pc']
    capacity = request.POST['id_capacity']
    specialization = request.POST['id_specialization']
    specification = request.POST['id_specification']

    clase = Classroom.objects.get(num_class=num_class, location=location)
    clase.s_o = s_o
    clase.num_pc = num_pc
    clase.capacity = capacity
    clase.specialization = specialization
    clase.specification = specification
    clase.save()

    return redirect('/')


def removeClassroom(request, num_class, location):

    clase = get_object_or_404(Classroom, num_class=num_class, location=location)
    print(f"CLASE ES:: {clase.__hash__}")
    clase.delete()
    return redirect('/')

def importClassroom(request):
    # TODO
    print('PRUEBAAAAA')
    if request.method == 'POST':
        classroom_resource = ClassromResource()
        dataset = Dataset()
        new_classroom = request.FILES['file']

        if not new_classroom.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'index.html')
        imported_data = dataset.load(new_classroom.read(), format='xlsx')
        for data in imported_data:
            messages.info(request, data)
            value = Classroom.objects.create(data[5],data[1],data[3],data[4],data[0],data[2])
            value.save()

    return redirect(request, "/")

