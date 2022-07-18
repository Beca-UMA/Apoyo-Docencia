from doctest import master
from http.client import CONFLICT
from telnetlib import SE

from requests import TooManyRedirects
from Aplicaciones.classroom.models import Classroom
from Aplicaciones.request_class.models import RequestClass
from .models import Slot

COMFLICTS = []
MAX_STRIKES = 3

def unique_codes():
    codes = RequestClass.objects.values_list('code')
    return list(dict.fromkeys(codes))


def real_targets(request):
    real_targets = []
    possible_tagets = Classroom.objects.filter(num_pc__gte = request.num_alum)
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
        CONFLICT.append(f"El request con código {request.code} no se puede asignar a ningun aula ya que ninguna cumple sus requisitos")
    return real_targets
    
def matches():
    unique_codes = unique_codes() # Conjunto candidatos
    matches = [] # Diccionario con una asignación de clase con las peticiones que puede satisfacer
    for code in unique_codes:
        q = RequestClass.objects.filter(code=code)
        for r in q.iterator():
            real_targets = real_targets(r) # Lista de clases con las mismas características
            match = {}
            match[r.code] = real_targets
            matches.append(match)
            break

def preprocess():
    matches = matches()

    # Ordenar de menos posibilidades para elegir a más posibilidades para elegir
    sorted_matches = sorted(matches, key=lambda x:x[1])
    solution = {}
    for k in unique_codes:
        solution[k] = None

    strikes = 0

    assign(solution, sorted_matches, strikes)

    # COSAS QUE HACER
    # 2. LAS FRANJAS HORARIAS DE LOS SLOT SON 6: 1,2,3 MAÑANA Y 4,5,6 TARDE
    # 3. LOS EXAMENES/MASTER (CREO QUE LOS MASTER TAMBIEN) OCUPAN DOS FRANJAS
    # ASI QUE NO PUEDEN RESERVAR LAS FRANJAS 3 NI 6
    # 4. EL ALGORITMO TIENE COMO FUNCION DE CORTE EL NUMERO DE CONFLICTOS,
    # SI EN ALGUNA RAMA SUPERA (POR UN PONER) 5 CONFLICTOS SE CORTA ESA RAMA Y SE VA A LA SIGUIENE.
    # 5. LAS RAMAS SE EXPANDEN TIPO:
    # PET1_PREFERENT -> ASIGNAR_CLASE(), PET2_PREFERENT -> ASIGNAR_CLASE() {SI SE DA CONFLICTOS DE HORARIO, SE
    # SUMA 1 CONFLICTO Y SE SIGUE, ASIGNANDO AHORA LA PET3}


def assign(solution, matches, strikes, preference, count, classroom):
    # solution-> {1125:{"franja":1,"clase":"lab_01"},...}
    # matches-> [1125:["lab_01", "lab_02", "lab_03",...], 1126:["lab_02"], ...]
    # strikes-> nº de conflictos en la solucion
    # preference-> "Preferente" o "Alternativo"
    # count-> Posición en la lista de matches que habrá que hacer la elección
    # classroom-> Classroom.class

    target = matches[count] # Codigo de la reserva para la siguiente elección
    request = RequestClass.objects.get(code = target.keys()[0], preference=preference)
    solution, conflict = add_choice(solution, matches, request, classroom)
    
    is_empty = [{x:v} for x,v in solution.items() if v==None]
    if len(is_empty) == 0:
        # Ya se han asignado todas las peticiones
        return strikes, solution

    if strikes == MAX_STRIKES:
        return None, solution
    if conflict:
        strikes += 1

    q = RequestClass.objects.filter(code__in = target.keys())
    choice_preferente = None
    choice_alternativo = None
    for r in q.iterator():
        if r.preference =='Preferente':
            choice_preferente = r
        else:
            choice_alternativo = r

    min_strikes_preferente = float('inf')
    min_strikes_alternativo = float('inf')
    preferente = {}
    alternativo = {}
    for _,classroom in matches[count].items():
        strikes_preferente, preferente = assign(solution, matches, strikes, "Preferente", count+1, classroom)
        if strikes_preferente < min_strikes_preferente:
            preferente = preferente
        strikes_alternativo, alternativo = assign(solution, matches, strikes, "Alternativo", count+1, classroom)
        if strikes_alternativo < min_strikes_alternativo:
            alternativo = alternativo
    min_strikes = min(strikes_preferente, strikes_alternativo)
    if min_strikes == strikes_preferente:
        return strikes_preferente, preferente
    else:
        return strikes_alternativo, alternativo


def add_choice(solution, matches, request, classroom) -> tuple (dict, bool):
    # Añadir la elección a la solución, donde en solución tendrá que estar como clave 
    # el código de la reserva y como valor -> franja:1 y si es una franja mas larga por 
    # examen poner -> franja:[1,2]. Tener en cuenta que si se reserva dos franjas no puedas reservar la [3,4]
    # y por ultimo en la elección seleccionar la clase
    None

def conflict(solution, classroom, schedule) -> bool:
    # Comprobar en la solucion si hay conflictos entre la shcedule y la clase elegida entre las elecciones
    # de la solucion
    None 
