import os
import time

from .controller import ControlMode, Controller


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def show_hmi(controller: Controller, message: str = "") -> None:
    state = controller.get_state()
    actuators = controller.get_actuators()

    if (
        state.temperature > controller.TEMPERATURE_LIMIT
        or state.pressure > controller.PRESSURE_LIMIT
    ):
        status = "INTERLOCK DE SEGURIDAD"
    else:
        status = "OPERACION NORMAL"

    print("=" * 58)
    print("           SISTEMA DE CONTROL - REACTOR")
    print("=" * 58)
    print(f" Modo:                 {controller.mode.value.upper()}")
    print()
    print(f" Temperatura:          {state.temperature:7.2f} °C")
    print(f" Presion:              {state.pressure:7.2f} bar")
    print()
    print(f" Bomba:                {actuators.pump:7.2f} %")
    print(
        " Valvula de alivio:    "
        f"{'ABIERTA' if actuators.relief_valve else 'CERRADA'}"
    )
    print()
    print(f" Estado:               {status}")
    print("=" * 58)

    if message:
        print()
        print(f"> {message}")

    print()


def print_help() -> None:
    print("Comandos disponibles:")
    print()
    print("  modo manual")
    print("  modo automatico")
    print("  modo pruebas")
    print()
    print("  bomba <0-100>")
    print("  valvula abrir")
    print("  valvula cerrar")
    print()
    print("  leer caudal")
    print("  leer manometro")
    print()
    print("  fallo temperatura")
    print("  fallo presion")
    print("  reset")
    print("  ayuda")
    print("  salir")
    print()


def process_command(
    controller: Controller,
    command: str,
) -> tuple[bool, str]:
    command = command.strip().lower()

    if command == "salir":
        return False, "Cerrando el sistema."

    if command == "ayuda":
        print_help()
        input("Presiona ENTER para continuar...")
        return True, ""

    if command == "modo manual":
        controller.set_mode(ControlMode.MANUAL)
        return True, "Modo manual seleccionado."

    if command == "modo automatico":
        controller.set_mode(ControlMode.AUTOMATIC)
        return True, "Modo automatico seleccionado."

    if command == "modo pruebas":
        controller.set_mode(ControlMode.TEST)
        return True, "Modo de pruebas seleccionado."

    if command.startswith("bomba "):
        if controller.mode != ControlMode.MANUAL:
            return True, "La bomba manual solo puede modificarse en modo manual."

        try:
            value = float(command.split(maxsplit=1)[1])
        except ValueError:
            return True, "Valor de bomba no valido."

        controller.set_manual_pump(value)

        return (
            True,
            f"Bomba ajustada a {controller.get_actuators().pump:.1f}%.",
        )

    if command == "valvula abrir":
        if controller.mode != ControlMode.MANUAL:
            return True, "La valvula manual solo puede modificarse en modo manual."

        controller.open_relief_valve()
        return True, "Valvula de alivio abierta."

    if command == "valvula cerrar":
        if controller.mode != ControlMode.MANUAL:
            return True, "La valvula manual solo puede modificarse en modo manual."

        controller.close_relief_valve()
        return True, "Valvula de alivio cerrada."

    if command == "leer caudal":
        pump = controller.get_actuators().pump

        print(f"\nCaudal de refrigerante simulado: {pump:.1f}%")
        input("\nPresiona ENTER para continuar...")

        return True, ""

    if command == "leer manometro":
        pressure = controller.get_state().pressure

        print(f"\nLectura del manometro: {pressure:.2f} bar")
        input("\nPresiona ENTER para continuar...")

        return True, ""

    if command == "fallo temperatura":
        controller.activate_temperature_fault()
        return True, "Fallo de temperatura inyectado: 90 °C."

    if command == "fallo presion":
        controller.activate_pressure_fault()
        return True, "Fallo de presion inyectado: 13 bar."

    if command == "reset":
        controller.reset()
        return True, "Sistema reiniciado."

    return True, "Comando no reconocido. Escribe 'ayuda'."


def automatic_loop(controller: Controller) -> None:
    while controller.mode == ControlMode.AUTOMATIC:
        controller.update()

        clear_screen()
        show_hmi(
            controller,
            "Control automatico en ejecucion. "
            "Presiona ENTER para regresar al menu.",
        )

        time.sleep(0.5)

        if os.name == "nt":
            import msvcrt

            if msvcrt.kbhit():
                key = msvcrt.getwch()

                if key == "\r":
                    controller.set_mode(ControlMode.MANUAL)
                    break


def main() -> None:
    controller = Controller()
    message = "Sistema iniciado."

    while True:
        clear_screen()
        show_hmi(controller, message)

        if controller.mode == ControlMode.AUTOMATIC:
            automatic_loop(controller)
            message = "Control automatico detenido."
            continue

        print("Escribe 'ayuda' para consultar los comandos.")

        command = input("\nComando > ")

        running, message = process_command(controller, command)

        if not running:
            clear_screen()
            print("Sistema finalizado.")
            break

        if controller.mode == ControlMode.TEST:
            controller.update()

        time.sleep(0.1)


if __name__ == "__main__":
    main()