import datetime as dt
import sys

horarios = []

def registrarEntrada():
    print("Começando a trabalhar")
    horarioEntrada = dt.datetime.now()
    horarios.append({"Entrada registrada": horarioEntrada})
    print("=" * 30)
    print("Horario registrado")
    print("=" * 30)
    menu()

def registrarEntradaIntervalo():
    print("Começando o intervalo")
    horarioInicioIntervalo = dt.datetime.now()
    horarios.append({"Entrada registrada": horarioInicioIntervalo})
    print("=" * 30)
    print("Horario registrado")
    print("=" * 30)
    menu() 

def registrarVoltaIntervalo():
    print("Voltando a trabalhar")
    horarioEntrada = dt.datetime.now()
    horarios.append({"Entrada registrada": horarioEntrada})
    print("=" * 30)
    print("Horario registrado")
    print("=" * 30)
    menu()

def registrarSaida():
    print("Saindo do trabalho")
    horarioEntrada = dt.datetime.now()
    horarios.append({"Entrada registrada": horarioEntrada})
    print("=" * 30)
    print("Horario registrado")
    print("=" * 30)
    relatorioHorario()
    sys.exit()

def relatorioHorario():
    print("Relatorio de horario diario")

    for hora in horarios:
        horaFormatada = hora["Entrada registrada"].strftime("%H:%M")
        print(horaFormatada)

    print("=" * 30)
    print("Encerrando o dia")
    
def menu():
    while True:
        print("Registro de horarios diario")
        print("Escolha uma das opções abaixo")
        print("1 - Registrar entrada")
        print("2 - Registrar inicio de intervalo")
        print("3 - Registrar fim de intervalo")
        print("4 - Registrar saida")

        opcao = int(input("Digite a opção aqui: "))

        match opcao:
            case 1:
                registrarEntrada()
            case 2:
                registrarEntradaIntervalo()
            case 3:
                registrarVoltaIntervalo()
            case 4:
                registrarSaida()
            case _:
                print("Comando desconecido")

if __name__ == "__main__":
    menu()
