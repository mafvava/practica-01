
from nodo_iot import NodoIoT
from nodos import NodoSensor, NodoActuador


def main() -> None:
    # Crear los dispositivos de la red IoT
    sensor_temp = NodoSensor(
        "SEN-001",
        "192.168.1.10",
        "Laboratorio",
        "Temperatura",
        28.5,
        30.0
    )

    actuador_ventilador = NodoActuador(
        "ACT-001",
        "192.168.1.11",
        "Laboratorio",
        "Ventilador",
        180
    )

    sensor_luz = NodoSensor(
        "SEN-002",
        "192.168.1.12",
        "Aula",
        "Luminosidad",
        75.0,
        90.0
    )

    # Lista mixta de dispositivos
    red_iot: list[NodoIoT] = [
        sensor_temp,
        actuador_ventilador,
        sensor_luz
    ]

    # Conectar todos los dispositivos
    print("\n===== INICIALIZANDO RED IoT =====")

    for dispositivo in red_iot:
        dispositivo.conectar()

    # Menú interactivo
    while True:
        print("\n===== SISTEMA MODULAR DE NODOS IoT =====")
        print("1. Mostrar telemetría de todos los nodos")
        print("2. Encender ventilador")
        print("3. Apagar ventilador")
        print("4. Configurar potencia PWM")
        print("5. Cambiar límite de temperatura")
        print("6. Cambiar límite de luminosidad")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            print("\n--- TELEMETRÍA DE LA RED ---")

            # Bucle polimórfico: no identifica el tipo de dispositivo
            for dispositivo in red_iot:
                dispositivo.enviar_telemetria()

        elif opcion == "2":
            actuador_ventilador.encender()

        elif opcion == "3":
            actuador_ventilador.apagar()

        elif opcion == "4":
            try:
                potencia = int(input("Introduce PWM (0-255): "))
                actuador_ventilador.configurar_pwm(potencia)
                print("Potencia PWM actualizada correctamente.")

            except (ValueError, TypeError) as error:
                print(f"Error al configurar PWM: {error}")

        elif opcion == "5":
            try:
                limite = float(
                    input("Nuevo límite de temperatura: ")
                )
                sensor_temp.limite_alerta = limite
                print("Límite de temperatura actualizado.")

            except (ValueError, TypeError) as error:
                print(f"Error al cambiar el límite: {error}")

        elif opcion == "6":
            try:
                limite = float(
                    input("Nuevo límite de luminosidad: ")
                )
                sensor_luz.limite_alerta = limite
                print("Límite de luminosidad actualizado.")

            except (ValueError, TypeError) as error:
                print(f"Error al cambiar el límite: {error}")

        elif opcion == "0":
            print("Cerrando el sistema IoT.")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
