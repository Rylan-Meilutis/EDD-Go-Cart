from typing import *
import gpiozero as gpio


class buttons:
    def __init__(self) -> NoReturn:
        self.accelerator_dev = gpio.AnalogInputDevice(0)
        self.brake_pedal_dev = gpio.AnalogInputDevice(1)
        self.enable_button_dev = gpio.Button(3)
        self.enable_cruise_button_dev = gpio.Button(4)
        self.accelerator = 0
        self.brake_pedal = 0
        self.enable_button = False
        self.enable_cruise_button = False

    def accelerator(self) -> float:
        return self.accelerator_dev.value()

    def brake_pedal(self) -> float:
        return self.brake_pedal_dev.value()

    def enable_button(self) -> bool:
        return True if self.enable_button_dev.value() == 1 else False

    def enable_cruise_button(self) -> bool:
        return True if self.enable_cruise_button_dev.value() == 1 else False
