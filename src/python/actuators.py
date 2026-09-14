from dataclasses import dataclass


@dataclass
class ActuatorState:
    pump: float
    relief_valve: int


class CoolingPump:
    MIN_VALUE = 0.0
    MAX_VALUE = 100.0

    def __init__(self, initial_value: float = 0.0) -> None:
        self._value = self._clamp(initial_value)

    def set_output(self, value: float) -> None:
        self._value = self._clamp(value)

    def read_output(self) -> float:
        return self._value

    @classmethod
    def _clamp(cls, value: float) -> float:
        return max(cls.MIN_VALUE, min(cls.MAX_VALUE, value))


class ReliefValve:
    CLOSED = 0
    OPEN = 1

    def __init__(self, initial_state: int = CLOSED) -> None:
        self._state = self._validate(initial_state)

    def open(self) -> None:
        self._state = self.OPEN

    def close(self) -> None:
        self._state = self.CLOSED

    def set_state(self, state: int) -> None:
        self._state = self._validate(state)

    def read_state(self) -> int:
        return self._state

    @classmethod
    def _validate(cls, state: int) -> int:
        if state not in (cls.CLOSED, cls.OPEN):
            raise ValueError("La válvula solamente puede estar en 0 o 1.")
        return state


class ActuatorSystem:
    def __init__(
        self,
        initial_pump: float = 0.0,
        initial_valve: int = ReliefValve.CLOSED,
    ) -> None:
        self.pump = CoolingPump(initial_pump)
        self.relief_valve = ReliefValve(initial_valve)

    def set_pump(self, value: float) -> None:
        self.pump.set_output(value)

    def open_valve(self) -> None:
        self.relief_valve.open()

    def close_valve(self) -> None:
        self.relief_valve.close()

    def read_all(self) -> ActuatorState:
        return ActuatorState(
            pump=self.pump.read_output(),
            relief_valve=self.relief_valve.read_state(),
        )