from typing import *
import simple_pid as pid
import buttons as bs
import drivetrain


class cruise:
    def __init__(self, buttons: bs.buttons, drive: drivetrain.drivetrain) -> NoReturn:
        self.cruise_kp = 0.8
        self.cruise_ki = 0.0
        self.cruise_kd = 0.0
        self.cruise_pid = pid.PID(self.cruise_kp, self.cruise_ki, self.cruise_kp)
        self.buttons = buttons
        self.drive = drive
        self.cruise_toggle = False
        self.cruise_press = False
        self.enable_cruise_button_press = False

    def cruise_control_toggle(self, button: bool) -> NoReturn:
        if button:
            if not self.cruise_press:
                self.cruise_toggle = not self.cruise_toggle
                self.enable_cruise_button_press = True
            else:
                self.enable_cruise_button_press = False
        else:
            self.enable_cruise_button_press = False
            self.cruise_press = False

        if self.buttons.brake_pedal() > 0.05:
            self.cruise_toggle = False
            self.cruise_press = False
            self.enable_cruise_button_press = False

    def cruise(self, speed: float) -> NoReturn:
        self.cruise_pid.auto_mode = True
        set_point = self.cruise_pid(speed)
        if set_point < 0:
            if abs(set_point - self.drive.get_cruise_speed()) > 100:
                self.drive.brake(0.25)
        else:
            manual_speed = self.buttons.accelerator()
            if set_point >= manual_speed * 5676 / 10 * 62.5:
                self.drive.drive(set_point)
            else:
                self.drive.drive(manual_speed)
