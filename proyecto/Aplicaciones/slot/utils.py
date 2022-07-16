from doctest import master
from http.client import CONFLICT
from telnetlib import SE

from requests import TooManyRedirects
from Aplicaciones.classroom.models import Classroom
from Aplicaciones.request_class.models import RequestClass
from .models import Slot

COMFLICTS = []


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
    match = {} # Diccionario con una asignación de clase con las peticiones que puede satisfacer
    while unique_codes != None:
        q = RequestClass.objects.filter(code=unique_codes[0])
        for r in q.iterator():
            real_targets = real_targets(r) # Lista de clases con las mismas características
            match[r] = real_targets

def preprocess():
    matches = matches()

    # COSAS QUE HACER
    # 1. ORDENAR EL DICCIONARIO DE MATCHES POR EL NUMERO DE POSIBLES AULAS,
    # PRIMERO LAS QUE TIENEN MENOS AULAS POSIBLES, DESPUES LAS QUE MAS
    # 2. LAS FRANJAS HORARIAS DE LOS SLOT SON 6: 1,2,3 MAÑANA Y 4,5,6 TARDE
    # 3. LOS EXAMENES/MASTER (CREO QUE LOS MASTER TAMBIEN) OCUPAN DOS FRANJAS
    # ASI QUE NO PUEDEN RESERVAR LAS FRANJAS 3 NI 6
    # 4. EL ALGORITMO TIENE COMO FUNCION DE CORTE EL NUMERO DE CONFLICTOS,
    # SI EN ALGUNA RAMA SUPERA (POR UN PONER) 5 CONFLICTOS SE CORTA ESA RAMA Y SE VA A LA SIGUIENE.
    # 5. LAS RAMAS SE EXPANDEN TIPO:
    # PET1_PREFERENT -> ASIGNAR_CLASE(), PET2_PREFERENT -> ASIGNAR_CLASE() {SI SE DA CONFLICTOS DE HORARIO, SE
    # SUMA 1 CONFLICTO Y SE SIGUE, ASIGNANDO AHORA LA PET3}



