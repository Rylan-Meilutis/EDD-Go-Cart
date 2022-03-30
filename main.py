from typing import *
from ctre import *
import cv2
import numpy as np

# import RPi.GPIO as gpio

pot_range = 10000
brake_actuator = TalonSRX(3)
falcon1 = TalonFX(1)
falcon2 = TalonFX(2)
falcon3 = TalonFX(3)
falcon4 = TalonFX(4)
falcon5 = TalonFX(5)
falcon6 = TalonFX(6)


def config() -> NoReturn:
    falcon1.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
    falcon2.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
    falcon3.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
    falcon4.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
    falcon5.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
    falcon6.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor)
    brake_actuator.configSelectedFeedbackSensor(FeedbackDevice.Analog, 0)


def run_motors(speed: float, control_mode=TalonFXControlMode.PercentOutput) -> NoReturn:
    falcon1.set(control_mode, speed)
    falcon2.set(control_mode, speed)
    falcon3.set(control_mode, speed)
    falcon4.set(control_mode, speed)
    falcon5.set(control_mode, speed)
    falcon6.set(control_mode, speed)


def stop_motors(speed: float, control_mode=TalonFXControlMode.PercentOutput) -> NoReturn:
    falcon1.set(control_mode, 0)
    falcon2.set(control_mode, 0)
    falcon3.set(control_mode, 0)
    falcon4.set(control_mode, 0)
    falcon5.set(control_mode, 0)
    falcon6.set(control_mode, 0)


def main() -> NoReturn:
    while True:
        text = str(int(get_speed() + 0.5)) + " MPH"
        frame = np.zeros(shape=(1920, 1080, 3))
        cv2.putText(frame, text, (420, 800), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, 2)
        cv2.imshow("Speedometer", frame)
        pot_pos = brake_actuator.getSelectedSensorPosition(0)
        if pot_pos > 10:
            run_motors(pot_pos / pot_range)

            brake_actuator.set(TalonSRXControlMode.PercentOutput, 0)
        elif pot_pos < -10:
            brake_actuator.set(TalonSRXControlMode.PercentOutput, pot_pos / pot_range)


def get_speed() -> float:
    return ((falcon1.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
           ((falcon2.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
           ((falcon3.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
           ((falcon4.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
           ((falcon5.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) + \
           ((falcon6.getSelectedSensorVelocity() * 10 / 2048 * 60) * 8 / 1056) / 6


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting cuz of keyboard interrupt")
        exit(69420)
