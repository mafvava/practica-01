
class NodoIoT:
    def __init__(
        self,
        id_dispositivo: str,
        ip: str,
        ubicacion: str
    ) -> None:
        self.id_dispositivo = id_dispositivo
        self.ip = ip
        self.ubicacion = ubicacion
        self.conectado = False

    def conectar(self) -> None:
        self.conectado = True
        print(
            f"[{self.id_dispositivo}] "
            f"Conectado correctamente a la red IoT."
        )

    def enviar_telemetria(self) -> None:
        print(
            f"Dispositivo: {self.id_dispositivo} | "
            f"IP: {self.ip} | "
            f"Ubicación: {self.ubicacion} | "
            f"Conectado: {self.conectado}"
        )
