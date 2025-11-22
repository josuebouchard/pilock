from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory


class ServoLock:
    _servo: AngularServo
    _is_locked: bool = True

    def __init__(self, pin: int = 19):
        self._servo = AngularServo(
            pin=pin,
            min_pulse_width=500e-6,
            max_pulse_width=2450e-6,
            initial_angle=0,
            pin_factory=PiGPIOFactory(),
        )
        self.lock()

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def lock(self):
        self._servo.angle = 75
        self._is_locked = True

    def unlock(self):
        self._servo.angle = 0
        self._is_locked = False

    def detach(self):
        self._servo.detach()

    def toggle(self):
        if self.is_locked:
            self.unlock()
        else:
            self.lock()
