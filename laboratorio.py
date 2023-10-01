from paciente import Paciente

class Laboratorio:
    def __init__(self):
        self.ordenes_medicamento = []

    def recibir_orden_medicamento(self, paciente):
        self.ordenes_medicamento.append(paciente)