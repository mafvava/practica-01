from dataclasses import dataclass

from .actuators import ActuatorSystem
from .sensors import SensorSystem


@dataclass
class ReactorState:
    temperature: float
    pressure: float


class Reactor:
    """Modelo dinámico simplificado del proceso."""

    TEMPERATURE_RATE = 1.5
    COOLING_FACTOR = 0.05

    PRESSURE_BASE_CHANGE = 0.02
    RELIEF_EFFECT = 0.5

    def __init__(
        self,
        initial_temperature: float = 25.0,
        initial_pressure: float = 1.0,
    ) -> None:
        self.sensors = SensorSystem(
            initial_temperature=initial_temperature,
            initial_pressure=initial_pressure,
        )

    def step(self, actuators: ActuatorSystem) -> ReactorState:
        """Avanza la simulación un ciclo."""

        pump = actuators.pump.read_output()
        valve = actuators.relief_valve.read_state()

        # Dinámica térmica obligatoria de la práctica.
        delta_temperature = (
            self.TEMPERATURE_RATE
            - self.COOLING_FACTOR * pump
        )

        current_temperature = self.sensors.temperature.read()
        new_temperature = current_temperature + delta_temperature

        # La presión aumenta cuando el sistema se calienta.
        pressure_change = (
            self.PRESSURE_BASE_CHANGE * max(delta_temperature, 0.0)
        )

        # La válvula de alivio reduce la presión.
        if valve == 1:
            pressure_change -= self.RELIEF_EFFECT

        current_pressure = self.sensors.pressure.read()
        new_pressure = current_pressure + pressure_change

        self.sensors.update(
            temperature=new_temperature,
            pressure=new_pressure,
        )

        return self.read_state()

    def read_state(self) -> ReactorState:
        """Obtiene el estado actual del reactor."""

        data = self.sensors.read_all()

        return ReactorState(
            temperature=data.temperature,
            pressure=data.pressure,
        )

    def reset(self) -> None:
        """Regresa el reactor a sus condiciones iniciales."""

        self.sensors.update(
            temperature=25.0,
            pressure=1.0,
        )