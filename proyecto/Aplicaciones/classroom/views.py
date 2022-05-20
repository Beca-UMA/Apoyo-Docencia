from django.shortcuts import render, redirect
from .models import Classroom

# Create your views here.
def index(request):
    clases = Classroom.objects.all()
    return render(request, "index.html", {"clases": clases})

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
    clase = Classroom.objects.get(num_class=num_class, location=location)
    clase.delete()
    return redirect('/')

def importClassroom(request):
    # TODO
    return redirect("/")

