from typing import NoReturn

import gpiozero as gpio


class buttons:
    def __init__(self) -> NoReturn:
        """
        Init method for the class
        """
        self.__accelerator_dev = gpio.AnalogInputDevice(0)
        self.__brake_pedal_dev = gpio.AnalogInputDevice(1)
        self.__enable_button_dev = gpio.Button(3)
        self.__enable_cruise_button_dev = gpio.Button(4)

    def accelerator(self) -> float:
        """
        Gets the current pedal position
        :return: The position of the pedal (0-1)
        """
        return self.__accelerator_dev.value()

    def brake_pedal(self) -> float:
        """
        Gets the current pedal position
        :return: The position of the pedal (0-1)
        """
        return self.__brake_pedal_dev.value()

    def enable_button(self) -> bool:
        """
        Gets the current state of the button
        :return: True if the button is pressed
        """
        return True if self.__enable_button_dev.value() == 1 else False

    def enable_cruise_button(self) -> bool:
        """
        Gets the current state of the button
        :return: True if the button is pressed
        """
        return True if self.__enable_cruise_button_dev.value() == 1 else False
