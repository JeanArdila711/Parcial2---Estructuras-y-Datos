from paciente import Paciente
from laboratorio import Laboratorio

class ColaFIFO:
    def __init__(self):
        self.items = []

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        
    def esta_vacia(self):
        return len(self.items) == 0
    
    def tamano(self):
        return len(self.items)
    
    def contar_elementos(self):
        return len(self.items)

class SistemaUrgencias:
    def __init__(self):
        self.pacientes = {
            'Codigo Azul': ColaFIFO(),
            'Estabilidad Urgente': ColaFIFO(),
            'Urgencias Normales': ColaFIFO(),
            'Urgencias Leves': ColaFIFO()
        }

        self.contadores_pacientes = {
            'Codigo Azul': 0,
            'Estabilidad Urgente': 0,
            'Urgencias Normales': 0,
            'Urgencias Leves': 0
        }

        self.laboratorio = Laboratorio()

    def ingresar_paciente(self):
        nombre = input("Ingrese el nombre del paciente: ")
        print("Codigos de triaje disponibles:")
        print("1. Codigo Azul")
        print("2. Estabilidad Urgente")
        print("3. Urgencias Normales")
        print("4. Urgencias Leves")
        codigo_triage = input("Seleccione el codigo de triaje (1/2/3/4): ")

        if codigo_triage == "1":
            codigo_triage = "Codigo Azul"
        elif codigo_triage == "2":
            codigo_triage = "Estabilidad Urgente"
        elif codigo_triage == "3":
            codigo_triage = "Urgencias Normales"
        elif codigo_triage == "4":
            codigo_triage = "Urgencias Leves"
        else:
            print("Codigo de triaje no valido. Se asginara 'Urgencias Leves' por defecto. ")   
            codigo_triage = "Urgencias Leves"

        paciente = Paciente(nombre, codigo_triage)
        if codigo_triage in self.pacientes:
            self.pacientes[codigo_triage].encolar(paciente)
            self.contadores_pacientes[codigo_triage] += 1

    def atender_pacientes(self, paciente):
        paciente.estado_medico.append("Examen medico")
        paciente.estado_medico.append("Pruebas diagnosticas")
        paciente.estado_medico.append("Procedimiento curativos")
        paciente.estado_medico.append("Estabilizacion y Monitoreo signos vitales")

        print(f"El paciente {paciente.nombre} ha sido atendido y estabilizado. ")
        
        if paciente.codigo_triaje == "Codigo Azul":
            paciente.salida = "Alta"
        elif paciente.codigo_triaje == "Estabilidad Urgente":
            paciente.salida = "Remitido para Hospitalización"
        elif paciente.codigo_triaje == "Urgencias Normales":
            paciente.salida = "Alta con medicamento"
        else:
            paciente.salida = "Alta Voluntaria"

    def dar_alta_paciente(self, paciente):
        if paciente.salida == "Alta":
            self.pacientes[paciente.codigo_triaje].desencolar()
            print(f"{paciente.nombre} fue dado de alta.")
        elif paciente.salida == "Alta con medicamento":
            self.laboratorio.recibir_orden_medicamento(paciente)
            self.pacientes[paciente.codigo_triaje].desencolar()
            print(f"{paciente.nombre} fue dado de alta con medicamento pendiente.")
        elif paciente.salida == "Alta Voluntaria":
            self.pacientes[paciente.codigo_triaje].desencolar()
            print(f"{paciente.nombre} decidio retirarse voluntariamente antes de recibir la atención médica completa recomendada.")
        elif paciente.salida == "Remitido para Hospitalización":
            self.pacientes[paciente.codigo_triaje].desencolar()
            print(f"{paciente.nombre} fue remitido para hospitalizacion.")
        elif paciente.salida == "Remitido a Medico Especialista":
            self.pacientes[paciente.codigo_triaje].desencolar()
            print(f"{paciente.nombre} fue remitido a un medico especialista.")
        elif paciente.salida == "Morgue":
            self.pacientes[paciente.codigo_triaje].desencolar()
            print(f"{paciente.nombre} lamentablemente fallecio y fue trasladado a la morgue.")

    def generar_informe(self):
        with open("informe_urgencias.txt", "w") as archivo:
            total_pacientes = sum(cola.contar_elementos() for cola in self.pacientes.values())
            archivo.write(f"Numero total de pacientes ingresados: {total_pacientes}\n")

            for categoria in self.pacientes.keys():
                cola = self.pacientes[categoria]
                cantidad_salidas = sum(1 for paciente in cola.items if paciente.salida != "")
                tipos_salidas = set(paciente.salida for paciente in cola.items if paciente.salida != "")

                archivo.write(f"Categoria de triaje: {categoria}\n")
                archivo.write(f"Numero de pacientes ingresados: {self.contadores_pacientes[categoria]}\n")
                archivo.write(f"Numero de pacientes con salidas distintas: {cantidad_salidas}\n")
                archivo.write(f"Tipos de salidas para esta categoria: {', '.join(tipos_salidas)}\n")
                archivo.write("\n")

if __name__ == "__main__":
    sistema = SistemaUrgencias()

    num_pacientes = int(input("Ingrese el numero de pacientes a ingresar: "))
    for _ in range(num_pacientes):
        sistema.ingresar_paciente()

    for categoria in sistema.pacientes.keys():
        cola_atencion = sistema.pacientes[categoria]
        while not cola_atencion.esta_vacia():
            paciente = cola_atencion.desencolar()
            sistema.atender_pacientes(paciente)
            sistema.dar_alta_paciente(paciente)

    sistema.generar_informe()
