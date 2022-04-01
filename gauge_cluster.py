from typing import NoReturn

import cv2
import numpy as np

import buttons as bs
import cruise_control as cc
import drivetrain as dt


def add_cruise_control(frame: np.ndarray, cruise_display_speed: float) -> np.ndarray:
    """
    Adds the cruise control data to the gauge cluster
    :param frame: The current frame of the gauge cluster
    :param cruise_display_speed: Current set speed of the cruise control
    :return: The current frame of the gauge cluster with the cruise control data added
    """
    cv2.putText(frame, str("Cruise Set Speed: " + str(int(cruise_display_speed))), (200, 800),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 255), 2, 2)
    return frame


class gauge_cluster:
    def __init__(self, buttons: bs.buttons, drivetrain: dt.drivetrain, cruise_control: cc.cruise) -> NoReturn:
        """
        Init method for the class
        :param buttons: Button object
        :param drivetrain: Drivetrain object
        :param cruise_control: Cruise control object
        """
        self.buttons = buttons
        self.drive = drivetrain
        self.cruise_control = cruise_control

    def display(self, cruise_display_speed=0.0, cruise_on=False) -> NoReturn:
        """
        Displays the gauge cluster
        :param cruise_display_speed: Current set speed of the cruise control
        :param cruise_on: State of the cruise control (on or off)
        """
        frame = np.zeros(shape=(1920, 1080, 3))
        if self.buttons.enable_button():
            frame = self.add_current_speed(frame)
            if cruise_on:
                frame = add_cruise_control(frame, cruise_display_speed)

        else:
            text = str("Go-Kart is Off")
            cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2, 2)

        cv2.imshow("Gauge Cluster", frame)

    def add_current_speed(self, frame: np.ndarray) -> np.ndarray:
        """
        Adds the current speed to the frame
        :param frame: Frame to add the text too
        :return: The frame with the text added
        """
        text = str(int(self.drive.get_speed() + 0.5)) + " MPH"
        cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, 2)
        return frame
