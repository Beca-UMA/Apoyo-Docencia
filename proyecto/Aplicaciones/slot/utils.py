import operator
from datetime import datetime, timedelta, time
from doctest import master
from http.client import CONFLICT
from telnetlib import SE
from urllib.request import Request
from webbrowser import Opera
import json

from requests import TooManyRedirects, request
from Aplicaciones.classroom.models import Classroom
from Aplicaciones.request_class.models import RequestClass
from proyecto.settings import BASE_DIR, STATIC_URL
from .models import Slot

CONFLICTS = []
MAX_STRIKES  = float('inf')

def main():
    # PREPROCESS
    all_matches = matches()
    # Ordenar de menos posibilidades para elegir a más posibilidades para elegir
    sorted_matches = sorted(all_matches , key=take_second)
    solution = {}
    uc = unique_codes()
    for k in uc:
        solution[k] = None
    strikes = 0

    # INFERENCE
    if CONFLICTS:
        return CONFLICTS
    else:    
        strikes,solution=assign(solution, sorted_matches, strikes, "Preferente", None, None)
        print(f"SOLUCION: {solution}, CONFLICTOS: {strikes}")
    # POSTPROCESS
    for code, assignation in solution.items():
        r = RequestClass.objects.get(code=code,preference=assignation["preference"])
        c = Classroom.objects.get(num_class=assignation["class"])
        s = Slot(schedule=str(assignation["schedule"]), request=r, classroom=c)
        s.save()
    solution["conflictos"] = strikes

    with open(str(STATIC_URL)+"asignacion.json", "w") as file:
        json.dump(solution, file)



def take_second(elem):
    return len(elem.values()) 


def unique_codes():
    codes = RequestClass.objects.values_list('code', flat=True)
    return list(dict.fromkeys(codes))


def real_targets(request):
    real_targets = []
    possible_tagets = Classroom.objects.filter(capacity__gte = request.num_alum)
    # print(f"REQUEST:::{request}, possible_targets:::{possible_tagets}")
    for t in possible_tagets.iterator():
        if not request.specification in ['No specificated', 'Cualquiera' ]:
            if t.specification != request.specification:
                continue
        if request.s_o != 'Indiferente':
            if t.s_o != request.s_o:
                continue
        if 'Cualquier' not in request.location:
            if t.location != request.location:
                continue
        real_targets.append(t)
    if len(real_targets) == 0:
        CONFLICTS.append(f"El request con código {request.code} no se puede asignar a ningun aula ya que ninguna cumple sus requisitos")
    return real_targets
    

def matches():
    uc = unique_codes() # Conjunto candidatos
    matches = [] # Diccionario con una asignación de clase con las peticiones que puede satisfacer
    for code in uc:
        q = RequestClass.objects.filter(code=code)
        for r in q.iterator():
            rts = real_targets(r) # Lista de clases con las mismas características
            match = {}
            match[r.code] = rts
            matches.append(match)
            break
    return matches


def assign(solution, matches, strikes, preference, count, classroom):
    # solution-> {1125:{"franja":1,"clase":"lab_01"},...}
    # matches-> [1125:["lab_01", "lab_02", "lab_03",...], 1126:["lab_02"], ...]
    # strikes-> nº de conflictos en la solucion
    # preference-> "Preferente" o "Alternativo"
    # count-> Posición en la lista de matches que habrá que hacer la elección
    # classroom-> Classroom.class

    if count != None:
        target = matches[count] # Codigo de la reserva para la siguiente elección
        for code in target:
            request = RequestClass.objects.get(code = code, preference=preference)
            solution, conflict = add_choice(solution, matches, request, classroom)

        is_empty = [{x:v} for x,v in solution.items() if v==None]
        if len(is_empty) == 0:
            # Ya se han asignado todas las peticiones
            return conflict, solution

        global MAX_STRIKES
        if strikes >= MAX_STRIKES:
            return float('inf'), solution
        
        strikes += conflict
    else:
        # Primera iteración
        count = -1

    min_strikes_preferente = float('inf')
    min_strikes_alternativo = float('inf')
    best_preferente = {}
    best_alternativo = {}
    strikes_preferente = None
    strikes_alternativo = None
    _, classrooms = list(matches[count+1].items())[0]
    for classroom in classrooms:
        # PREFERENTE
        strikes_preferente, preferente = assign(solution.copy(), matches, strikes, "Preferente", count+1, classroom)
        if strikes_preferente < min_strikes_preferente:
            best_preferente = preferente.copy()
            min_strikes_preferente = strikes_preferente

        #ALTERNATIVO
        strikes_alternativo, alternativo = assign(solution.copy(), matches, strikes, "Alternativo", count+1, classroom)
        if strikes_alternativo < min_strikes_alternativo:
            best_alternativo = alternativo.copy()
            min_strikes_alternativo = strikes_alternativo

    min_strikes = min(min_strikes_preferente, min_strikes_alternativo)
    if min_strikes<MAX_STRIKES:
        MAX_STRIKES=min_strikes
    # ME DA ERROR DE REFERENCED BEFORE ASIGMENT EN LA LINEA 96 SI DESCOMENTO ESTO
    if min_strikes == min_strikes_preferente:
        return min_strikes_preferente, best_preferente
    else:
        return min_strikes_alternativo, best_alternativo


def add_choice(solution, matches, request, classroom):
    # Añadir la elección a la solución, donde en solución tendrá que estar como clave 
    # el código de la reserva y como valor -> franja:1 y si es una franja mas larga por 
    # examen poner -> franja:[1,2]. Tener en cuenta que si se reserva dos franjas no puedas reservar la [3,4]
    # y por ultimo en la elección seleccionar la clase
    # print(f"\tADD CHOICE {request}---> SOLUTION: {solution}, CLASSROOM: {classroom}")
    schedule = get_schedule(request)
    all_conflict = conflict(solution, schedule, request, classroom)
    solution[request.code] = {
        "schedule":schedule,
        "preference": request.preference,
        "start_hour":str(request.start_hour),
        "end_hour":str(request.end_hour),
        "class":classroom.num_class,
        "start_date":str(request.start_date),
        "end_date":str(request.end_date),
        "day":request.alternative_day
    }
    return solution, all_conflict


def conflict(solution, schedule, request, classroom) -> int:
    # Comprobar en la solucion si hay conflictos entre la shcedule y la clase elegida entre las elecciones
    # de la solucion y devolver un numero de veces que ha habido conflictos con otros horarios
    conflict = 0
    for code, assignment in solution.items():
        if assignment != None and assignment["class"] == classroom.num_class and len(set(schedule) & set(assignment["schedule"])):
            latest_start = max(assignment["start_date"], request.start_date)
            earliest_end = min(assignment["end_date"], request.end_date)
            delta = (earliest_end - latest_start).days + 1
            overlap = max(0, delta)
            conflict += overlap

    return conflict


def get_schedule(request):
    # Con el request, dar una lista con la franja horaria dependiendo de la hora de entrada y la hora de salida.
    # Las franjas horarias son: 
    # 1 -> 8:30 / 10:30
    # 2 -> 10:30 / 12:30
    # 3 -> 12:3O / 14:30
    # 4 -> 15:30 / 17:30
    # 5 -> 17:30 / 19:30
    # 6 -> 19:30 / 21:3O
    result = []
    schedule =  time(8, 30, 0)
    schedule_found = False
    strip = 1
    while not schedule_found:
        next_schedule = schedule.replace(hour=schedule.hour+2)
        if request.start_hour >= schedule and request.start_hour <= next_schedule:
            result.append(strip)


        if request.end_hour >= schedule and request.end_hour <= next_schedule:
            result.append(strip)
            schedule_found = True
        schedule = next_schedule
        strip += 1
    return unique_list(result)


def unique_list(lista):
    list_set = set(lista)
    return (list(list_set))





