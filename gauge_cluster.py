from typing import *
import buttons as bs
import drivetrain as dt
import cruise_control as cc
import cv2
import numpy as np


class gauge_cluster:
    def __init__(self, buttons: bs.buttons, drivetrain: dt.drivetrain, cruise_control: cc.cruise):
        self.buttons = buttons
        self.drive = drivetrain
        self.cruise_control = cruise_control

    def display(self, cruise_display_speed: float):
        frame = np.zeros(shape=(1920, 1080, 3))
        if self.buttons.enable_button():
            text = str(int(self.drive.get_speed() + 0.5)) + " MPH"
            cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2, 2)
            cv2.putText(frame, str("Cruise Set Speed: " + str(int(cruise_display_speed))), (200, 800),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2, 2)
        else:
            text = str("Off")
            cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2, 2)

        cv2.imshow("Gauge Cluster", frame)

