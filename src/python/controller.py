from enum import Enum

from .actuators import ActuatorSystem
from .reactor import Reactor, ReactorState


class ControlMode(Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatico"
    TEST = "pruebas"


class Controller:
    """Control principal del sistema."""

    TEMPERATURE_LIMIT = 85.0
    PRESSURE_LIMIT = 12.0

    TEMPERATURE_SETPOINT = 60.0
    BASE_PUMP = 30.0
    KP = 2.0

    def __init__(self) -> None:
        self.reactor = Reactor()
        self.actuators = ActuatorSystem()
        self.mode = ControlMode.MANUAL
        self.test_temperature = False
        self.test_pressure = False

    def set_mode(self, mode: ControlMode) -> None:
        self.mode = mode

    def set_manual_pump(self, value: float) -> None:
        self.actuators.set_pump(value)

    def open_relief_valve(self) -> None:
        self.actuators.open_valve()

    def close_relief_valve(self) -> None:
        self.actuators.close_valve()

    def update(self) -> ReactorState:
        """Ejecuta un ciclo de control."""

        self._apply_test_faults()

        state = self.reactor.read_state()

        if self._safety_interlock_active(state):
            self._apply_safety_interlock()
        elif self.mode == ControlMode.AUTOMATIC:
            self._automatic_control(state)

        return self.reactor.step(self.actuators)

    def _safety_interlock_active(self, state: ReactorState) -> bool:
        return (
            state.temperature > self.TEMPERATURE_LIMIT
            or state.pressure > self.PRESSURE_LIMIT
        )

    def _apply_safety_interlock(self) -> None:
        self.actuators.set_pump(100.0)
        self.actuators.open_valve()

    def _automatic_control(self, state: ReactorState) -> None:
        error = state.temperature - self.TEMPERATURE_SETPOINT

        pump = self.BASE_PUMP + (self.KP * error)

        self.actuators.set_pump(pump)

        if state.pressure > 10.0:
            self.actuators.open_valve()
        else:
            self.actuators.close_valve()

    def _apply_test_faults(self) -> None:
        state = self.reactor.read_state()

        temperature = state.temperature
        pressure = state.pressure

        if self.test_temperature:
            temperature = 90.0

        if self.test_pressure:
            pressure = 13.0

        self.reactor.sensors.update(
            temperature=temperature,
            pressure=pressure,
        )

    def activate_temperature_fault(self) -> None:
        self.test_temperature = True

    def activate_pressure_fault(self) -> None:
        self.test_pressure = True

    def reset_test_faults(self) -> None:
        self.test_temperature = False
        self.test_pressure = False

    def reset(self) -> None:
        self.reactor.reset()
        self.actuators = ActuatorSystem()
        self.mode = ControlMode.MANUAL
        self.reset_test_faults()

    def get_state(self) -> ReactorState:
        return self.reactor.read_state()

    def get_actuators(self):
        return self.actuators.read_all()