from threading import Thread
from typing import NoReturn

import xbox_controller


class xbox_buttons:
    def __init__(self) -> NoReturn:
        """
        Init method for the class
        """
        thread1 = Thread(target=self.__get_controller_data())
        self.isControllerConnected = 0
        self.__ly = 0
        self.__rx = 0
        self.__btn_x = 0
        self.__btn_a = 0
        self.__enable = False
        self.__press = False
        thread1.start()

    def __get_controller_data(self) -> NoReturn:
        """
        Gets and stores the current state of all tracked __buttons
        """
        while True:
            try:
                events = xbox_controller.get_gamepad()
                self.isControllerConnected = 1

            except xbox_controller.NoDataError:
                events = None
                self.isControllerConnected = 1

            except xbox_controller.UnpluggedError:
                events = None
                self.isControllerConnected = 2

            # Determine if an event occurs then update the states
            if events is not None:
                for event in events:
                    if str(event.code) == "ABS_Y":
                        self.__ly = event.state / 256

                    if str(event.code) == "ABS_RX":
                        self.__rx = event.state / 256

                    if str(event.code) == "BTN_SOUTH":
                        self.__btn_x = event.state

                    if str(event.code) == "BTN_WEST":
                        self.__btn_a = event.state

    def accelerator(self) -> float:
        """
        Gets the current pedal position
        :return: The position of the pedal (0-1)
        """
        return self.__ly if self.__ly > 0 else 0

    def brake_pedal(self) -> float:
        """
        Gets the current pedal position
        :return: The position of the pedal (0-1)
        """
        return self.__ly if self.__ly < 0 else 0

    def x_btn(self) -> bool:
        """
        Gets the current state of the button
        :return: True if the button is pressed
        """
        return True if self.__btn_x == 1 else False

    def a_btn(self) -> bool:
        """
        Gets the current state of the button
        :return: True if the button is pressed
        """
        return True if self.__btn_a == 1 else False

    def a_btn_toggle(self):
        if self.__btn_a:
            if not self.__press:
                self.__press = True
                return True
            else:
                return False
        else:
            return False

    def desired_steering_position(self) -> float:
        """
        Gets the desired steering angle from the xbox controller
        :return: the steering angle of the xbox controller (-1 to 1)
        """
        return self.__rx
