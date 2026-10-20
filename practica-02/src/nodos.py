
from math import isfinite

from nodo_iot import NodoIoT


class NodoSensor(NodoIoT):
    def __init__(
        self,
        id_dispositivo: str,
        ip: str,
        ubicacion: str,
        tipo_sensor: str,
        lectura: float,
        limite_alerta: float
    ) -> None:
        super().__init__(id_dispositivo, ip, ubicacion)

        self.tipo_sensor = tipo_sensor
        self.lectura = lectura
        self.__limite_alerta = 0.0
        self.limite_alerta = limite_alerta

    @property
    def limite_alerta(self) -> float:
        return self.__limite_alerta

    @limite_alerta.setter
    def limite_alerta(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("El límite debe ser un número real.")

        if not isfinite(valor):
            raise ValueError("El límite debe ser un número finito.")

        self.__limite_alerta = float(valor)

    def enviar_telemetria(self) -> None:
        estado = (
            "ALERTA"
            if self.lectura >= self.__limite_alerta
            else "NORMAL"
        )

        print(
            f"[SENSOR] {self.id_dispositivo} | "
            f"Tipo: {self.tipo_sensor} | "
            f"Lectura: {self.lectura:.2f} | "
            f"Límite: {self.__limite_alerta:.2f} | "
            f"Estado: {estado} | "
            f"Conectado: {self.conectado}"
        )


class NodoActuador(NodoIoT):
    def __init__(
        self,
        id_dispositivo: str,
        ip: str,
        ubicacion: str,
        tipo_actuador: str,
        potencia_pwm: int = 0
    ) -> None:
        super().__init__(id_dispositivo, ip, ubicacion)

        self.tipo_actuador = tipo_actuador
        self.__estado_activo = False
        self.__potencia_pwm = 0

        self.configurar_pwm(potencia_pwm)

    @property
    def estado_activo(self) -> bool:
        return self.__estado_activo

    @property
    def potencia_pwm(self) -> int:
        return self.__potencia_pwm

    def configurar_pwm(self, potencia: int) -> None:
        if isinstance(potencia, bool) or not isinstance(potencia, int):
            raise TypeError("La potencia PWM debe ser un entero.")

        if not 0 <= potencia <= 255:
            raise ValueError("La potencia PWM debe estar entre 0 y 255.")

        self.__potencia_pwm = potencia

    def encender(self) -> None:
        self.__estado_activo = True
        print(f"[ACTUADOR] {self.id_dispositivo} encendido.")

    def apagar(self) -> None:
        self.__estado_activo = False
        print(f"[ACTUADOR] {self.id_dispositivo} apagado.")

    def enviar_telemetria(self) -> None:
        estado = "ENCENDIDO" if self.__estado_activo else "APAGADO"

        print(
            f"[ACTUADOR] {self.id_dispositivo} | "
            f"Tipo: {self.tipo_actuador} | "
            f"Estado: {estado} | "
            f"PWM: {self.__potencia_pwm}/255 | "
            f"Conectado: {self.conectado}"
        )
