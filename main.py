from typing import *
import drivetrain
import buttons as bs
import cruise_control as cc
import gauge_cluster as gc


drive = drivetrain.drivetrain()
buttons = bs.buttons()
cruise_control = cc.cruise(buttons, drive)
gauge_cluster = gc.gauge_cluster(buttons, drive, cruise_control)


def drive() -> NoReturn:
    if buttons.brake_pedal() < -10:
        drive.brake(buttons.brake_pedal())
        drive.drive(0)
    elif buttons.accelerator() > 10:
        drive.brake(0)
        drive.drive(buttons.accelerator())


def main() -> NoReturn:
    while True:
        cruise_display_speed = 0
        if buttons.enable_button():

            cruise_control.cruise_control_toggle(buttons.enable_button())
            cruise_speed = 0
            if cruise_control.cruise_toggle:
                if cruise_control.enable_cruise_button_press:
                    cruise_speed = drive.get_cruise_speed()
                    cruise_display_speed = drive.get_speed()
                cruise_control.cruise(cruise_speed)
        gauge_cluster.display(cruise_display_speed)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting cuz of keyboard interrupt")
        exit(69420)
