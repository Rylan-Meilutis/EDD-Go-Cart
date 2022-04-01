from typing import NoReturn

import buttons as bs
import cruise_control as cc
import drivetrain
import gauge_cluster as gc


def main() -> NoReturn:
    """
    Main method of the Go-Kart
    """
    dt = drivetrain.drivetrain()
    buttons = bs.buttons()
    cruise_control = cc.cruise(buttons, dt)
    gauge_cluster = gc.gauge_cluster(buttons, dt, cruise_control)

    def drive() -> NoReturn:
        """
        The main drive function for the go-kart
        """
        if buttons.brake_pedal() < -10:
            dt.brake(buttons.brake_pedal())
            dt.drive(0)
        elif buttons.accelerator() > 10:
            dt.brake(0)
            dt.drive(buttons.accelerator())

    while True:
        cruise_display_speed = 0
        if buttons.enable_button():
            cruise_control.cruise_control_toggle(buttons.enable_button())
            cruise_speed = 0
            if cruise_control.cruise_toggle:
                if cruise_control.enable_cruise_button_press:
                    cruise_speed = dt.get_cruise_speed()
                    cruise_display_speed = dt.get_speed()
                cruise_control.cruise(cruise_speed)
            else:
                drive()
        gauge_cluster.display(cruise_display_speed, cruise_control.cruise_toggle)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting cuz of keyboard interrupt")
        exit(69420)
