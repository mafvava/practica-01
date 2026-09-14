from src.python.actuators import ActuatorSystem
from src.python.controller import ControlMode, Controller
from src.python.reactor import Reactor


def test_reactor_initial_state() -> None:
    reactor = Reactor()

    state = reactor.read_state()

    assert state.temperature == 25.0
    assert state.pressure == 1.0


def test_temperature_equation_without_cooling() -> None:
    reactor = Reactor()
    actuators = ActuatorSystem()

    state = reactor.step(actuators)

    assert state.temperature == 26.5


def test_temperature_equation_with_100_percent_pump() -> None:
    reactor = Reactor()
    actuators = ActuatorSystem()

    actuators.set_pump(100.0)

    state = reactor.step(actuators)

    assert state.temperature == 21.5


def test_temperature_stability_at_30_percent_pump() -> None:
    reactor = Reactor()
    actuators = ActuatorSystem()

    actuators.set_pump(30.0)

    initial_state = reactor.read_state()
    state = reactor.step(actuators)

    assert state.temperature == initial_state.temperature


def test_pump_limits() -> None:
    actuators = ActuatorSystem()

    actuators.set_pump(150.0)
    assert actuators.read_all().pump == 100.0

    actuators.set_pump(-20.0)
    assert actuators.read_all().pump == 0.0


def test_relief_valve_states() -> None:
    actuators = ActuatorSystem()

    assert actuators.read_all().relief_valve == 0

    actuators.open_valve()
    assert actuators.read_all().relief_valve == 1

    actuators.close_valve()
    assert actuators.read_all().relief_valve == 0


def test_temperature_safety_interlock() -> None:
    controller = Controller()

    controller.activate_temperature_fault()
    controller.update()

    actuators = controller.get_actuators()

    assert actuators.pump == 100.0
    assert actuators.relief_valve == 1


def test_pressure_safety_interlock() -> None:
    controller = Controller()

    controller.activate_pressure_fault()
    controller.update()

    actuators = controller.get_actuators()

    assert actuators.pump == 100.0
    assert actuators.relief_valve == 1


def test_automatic_mode() -> None:
    controller = Controller()

    controller.set_mode(ControlMode.AUTOMATIC)

    state_before = controller.get_state()
    controller.update()
    actuators = controller.get_actuators()

    assert state_before.temperature == 25.0
    assert actuators.pump == 0.0