from dataclasses import dataclass


@dataclass
class SensorData:
    temperature: float
    pressure: float


class TemperatureSensor:
    MIN_VALUE = 0.0
    MAX_VALUE = 150.0

    def __init__(self, initial_value: float = 25.0) -> None:
        self._value = self._clamp(initial_value)

    def read(self) -> float:
        return self._value

    def update(self, value: float) -> None:
        self._value = self._clamp(value)

    @classmethod
    def _clamp(cls, value: float) -> float:
        return max(cls.MIN_VALUE, min(cls.MAX_VALUE, value))


class PressureSensor:
    MIN_VALUE = 0.0
    MAX_VALUE = 15.0

    def __init__(self, initial_value: float = 1.0) -> None:
        self._value = self._clamp(initial_value)

    def read(self) -> float:
        return self._value

    def update(self, value: float) -> None:
        self._value = self._clamp(value)

    @classmethod
    def _clamp(cls, value: float) -> float:
        return max(cls.MIN_VALUE, min(cls.MAX_VALUE, value))


class SensorSystem:
    def __init__(
        self,
        initial_temperature: float = 25.0,
        initial_pressure: float = 1.0,
    ) -> None:
        self.temperature = TemperatureSensor(initial_temperature)
        self.pressure = PressureSensor(initial_pressure)

    def read_all(self) -> SensorData:
        return SensorData(
            temperature=self.temperature.read(),
            pressure=self.pressure.read(),
        )

    def update(
        self,
        temperature: float,
        pressure: float,
    ) -> None:
        self.temperature.update(temperature)
        self.pressure.update(pressure)