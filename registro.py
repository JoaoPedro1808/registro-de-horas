import threading
import sys
import gspread
import datetime as dt
import time
from abc import ABC, abstractmethod
from oauth2client.service_account import ServiceAccountCredentials


def animacaoCarregar(pararEvento):
    sys.stdout.write("Conectando ao Google Cloud")

    pontos = [".", "..", "...", "   "]

    while not pararEvento.is_set():
        for ponto in pontos:
            if pararEvento.is_set():
                break
            sys.stdout.write(f"\rConectando com o Google Cloud{ponto}\r")
            sys.stdout.flush()
            time.sleep(0.4)

class RegistroHorarios(ABC):
    @abstractmethod
    def salvar(self, tipo: str, horario: dt.datetime):
        pass
    
    @abstractmethod
    def buscarHorarios(self):
        pass

class AcessoAoSheets(RegistroHorarios):
    def __init__(self, planilhaNome):
        paraConexao = threading.Event()
        animacao = threading.Thread(target=animacaoCarregar, args=(paraConexao,))

        animacao.start()

        escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        try:
            credencias = ServiceAccountCredentials.from_json_keyfile_name("credencias.json", escopo)
            self.client = gspread.authorize(credencias)
            self.sheet = self.client.open(planilhaNome).sheet1

            paraConexao.set()
            animacao.join()

        except Exception as e:
            print("Não foi possivel se conectar ao google sheets, verifique se a algum erro com o nome de digitação:", {e})
            exit()

        self.mapaColunas = {
            "Entrada": "B",
            "Entrada ao intervalo": "C",
            "Saida do intervalo": "D",
            "Saida": "E"
        }

    def salvar(self, tipo, horario):
        proximaLinha = len(self.sheet.col_values(1)) + 1

        hora = horario.strftime("%H:%M")
        data = horario.strftime("%d/%m/%y")
        colunaTipo = self.mapaColunas.get(tipo, "F")

        self.sheet.update_acell(f"A{proximaLinha}", data)
        self.sheet.update_acell(f"{colunaTipo}{proximaLinha}", hora)

        print(f"{tipo} registrado na {proximaLinha}")
    
    def buscarHorarios(self):
        registro = self.sheet.get_all_records()
        horariosFormatado = []

        for r in registro:
            if r.get("Entrada"):
                horario = f"{r["hora"]}"
                formatacao = dt.datetime.strftime(horario, "%H:%M")
                horariosFormatado.append({"Tipo": "Entrada", "Horario": formatacao})
        
        return horariosFormatado
                
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
        time.sleep(2)
    
def menu():
    NomePlanilha = "teste"

    repositorio = AcessoAoSheets(NomePlanilha)
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
        print("0 - Saida do sistema")
        print("=" * 50)

        opcaoEscolhida = input("Escreva uma opção: ")

        if opcaoEscolhida == "0":
            print("Saindo do programa...")
            break

        if opcaoEscolhida in opcoes:
            opcoes[opcaoEscolhida]()
        else:
            print("Opção invalida, tente novamente.")

if __name__ == "__main__":
    menu()