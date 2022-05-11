import csv


class Classroom:
    def __init__(self, specification, location, num_pc, s_o, num_class, capacity, specialization=''):
        self.specification = specification
        self.location = location
        self.num_pc = num_pc
        self.s_o = s_o
        self.specialization = specialization
        self.num_class = num_class
        self.capacity = capacity
    

    def set_specification(self, specification):
        self.specification = specification


    def set_location(self, location):
        self.location = location


    def set_num_pc(self, num_pc):
        self.num_pc = num_pc


    def set_s_o(self, s_o):
        self._s_o = s_o


    def set_specialization(self, specialization):
        self.specialization = specialization


    def set_num_class(self, num_class):
        self.num_class = num_class

    
    def set_capacity(self, capacity):
        self.capacity = capacity
    

def import_class_from_csv(file):
    reader = csv.DictReader(file, delimiter=';')
    list_clases = []
    for row in reader:
        num_class = row['Laboratorio']
        location = row['Sede']
        capacity = row['Aforo']
        num_pc = row['Equipos']
        s_o = row['Sistema Operativo']
        specification = row['Caracteristicas']
        clase = Classroom(specification,location,num_pc,s_o,num_class,capacity)
        list_clases.append(clase)


if __name__ == "__main__":
    with open('/home/ruben/Documentos/laboratorios.csv', newline='') as csvfile:
        import_class_from_csv(csvfile)


