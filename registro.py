import datetime as dt
import time
from abc import ABC, abstractmethod

class RegistroHorarios(ABC):
    @abstractmethod
    def salvar(self, tipo: str, horario: dt.datetime):
        pass
    
    @abstractmethod
    def buscarHorarios(self):
        pass

class MemoriaArquivo(RegistroHorarios):
    def __init__(self):
        self.horarios = []

    def salvar(self, tipo, horario):
        self.horarios.append({"Tipo": tipo, "Horario": horario})

    def buscarHorarios(self):
        return self.horarios
        
class GestorPontos:
    def __init__(self, registro: RegistroHorarios):
        self.registro = registro

    def registrarEntrada(self):
        self.registro.salvar("Entrada", dt.datetime.now())

    def registrarEntradaIntervalo(self):
        self.registro.salvar("Entrada ao intervalo", dt.datetime.now())

    def registrarSaidaIntervalo(self):
        self.registro.salvar("Saida do intervalo", dt.datetime.now())

    def registrarSaida(self):
        self.registro.salvar("Saída", dt.datetime.now())

    def gerarRelatorio(self):
        horarios = self.registro.buscarHorarios()

        print("Relatorio dos Horarios")
        print("=" * 30)

        for registro in horarios:
            hora_formatada = registro["Horario"].strftime("%H:%M")
            print(f"{registro['Tipo']:.<25} {hora_formatada}")

        print("=" * 30)
        time.sleep(10)
    
def menu():
    repositorio = MemoriaArquivo()
    gestor = GestorPontos(repositorio)

    opcoes = {
        "1": gestor.registrarEntrada,
        "2": gestor.registrarEntradaIntervalo,
        "3": gestor.registrarSaidaIntervalo,
        "4": gestor.registrarSaida,
        "5": gestor.gerarRelatorio
    }

    while True:
        print("=" * 50)
        print("Sistema de pontos do João Pedro Santana")
        print("1 - Registrar entrada")
        print("2 - Registrar entrada ao intervalo")
        print("3 - Registrar saida do intervalo")
        print("4 - Registrar saida")
        print("5 - Relatorio de horarios")
        print("=" * 50)

        opcaoEscolhida = input("Escreva uma opção: ")

        if opcaoEscolhida in opcoes:
            opcoes[opcaoEscolhida]()
        else:
            print("Opção invalida, tente novamente.")

if __name__ == "__main__":
    menu()